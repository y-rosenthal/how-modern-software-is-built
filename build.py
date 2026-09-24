#!/usr/bin/env python3
"""Assemble the course document from the source chunks in src/.

Generates: the table of contents, the keyword glossary (Appendix A) from every
<dfn class="kw"> in the text, and the answers appendix (Appendix B) from the
review-question boxes. Writes:

  course.html        - page fragment (what the Claude Artifact tool publishes)
  dist/index.html    - standalone page for self-hosting (GitHub Pages)
  dist/*.pdf         - PDF export, when Chrome is installed (skip with --no-pdf)
"""
import glob
import html
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

parts = sorted(glob.glob(os.path.join(SRC, "*.html")))
doc = "\n".join(open(p, encoding="utf-8").read() for p in parts)

# ---------------------------------------------------------------- headings
heading_re = re.compile(r'<h([23]) id="([^"]+)">(.*?)</h\1>', re.S)
headings = []  # (pos, level, id, text)
for m in heading_re.finditer(doc):
    text = re.sub(r"<span class=\"time\">.*?</span>", "", m.group(3))
    text = re.sub(r"<[^>]+>", "", text).strip()
    headings.append((m.start(), int(m.group(1)), m.group(2), text))

# session h2s have no id themselves; give them the enclosing section id
session_re = re.compile(r'<section class="(session|appendix)" id="([^"]+)">.*?<h2>(.*?)</h2>', re.S)
sessions = []
for m in session_re.finditer(doc):
    sessions.append((m.start(), m.group(1), m.group(2), re.sub(r"<[^>]+>", "", m.group(3)).strip()))

def section_for(pos):
    """Return (id, label) of the nearest h3 (or session) preceding pos."""
    best = None
    for hpos, level, hid, text in headings:
        if hpos <= pos and level == 3:
            best = (hid, text)
    if best is None:
        for spos, kind, sid, text in sessions:
            if spos <= pos:
                best = (sid, text)
    return best or ("intro", "Introduction")

# ---------------------------------------------------------------- TOC
toc = []
for spos, kind, sid, title in sessions:
    cls = "toc-session" if kind == "session" else "toc-appendix"
    toc.append(f'<li class="{cls}"><a href="#{sid}">{html.escape(title)}</a>')
    if kind == "session":
        # h3s between this session and the next
        nxt = next((s[0] for s in sessions if s[0] > spos), len(doc))
        subs = [h for h in headings if h[1] == 3 and spos < h[0] < nxt]
        if subs:
            toc.append('<ol class="toc-sub">')
            for _, _, hid, text in subs:
                toc.append(f'<li><a href="#{hid}">{html.escape(text)}</a></li>')
            toc.append("</ol>")
    toc.append("</li>")
toc_html = '<div class="toc-label">Sessions</div><ol>' + "\n".join(toc) + "</ol>"
# (inserted after the glossary is built, so heading positions stay valid)

# ---------------------------------------------------------------- glossary
dfn_re = re.compile(r'<dfn class="kw" id="(kw-[^"]+)" data-def="([^"]*)">(.*?)</dfn>', re.S)
entries = []
seen = set()
for m in dfn_re.finditer(doc):
    kid, definition, term = m.group(1), m.group(2), re.sub(r"<[^>]+>", "", m.group(3)).strip()
    if kid in seen:
        sys.exit(f"duplicate keyword id: {kid}")
    seen.add(kid)
    sec_id, sec_label = section_for(m.start())
    entries.append((term, kid, definition, sec_id, sec_label))

def sort_key(e):
    return re.sub(r"[^a-z0-9]", "", e[0].lower())

entries.sort(key=sort_key)
rows = []
letter = None
for term, kid, definition, sec_id, sec_label in entries:
    first = sort_key((term,))[0].upper()
    if first != letter:
        letter = first
        rows.append(f'<tr class="glossary-letter"><td colspan="3">{letter}</td></tr>')
    # definition attribute was HTML-escaped in source (&lt; etc.), keep as-is
    rows.append(
        f'<tr><td><a href="#{kid}">{html.escape(term)}</a></td>'
        f"<td>{definition}</td>"
        f'<td><a href="#{sec_id}">{html.escape(sec_label)}</a></td></tr>'
    )
glossary_html = (
    f'<p class="backlink">{len(entries)} keywords.</p>'
    '<div class="tbl-wrap"><table class="glossary">'
    "<thead><tr><th>Keyword</th><th>Short definition</th><th>Where it is introduced</th></tr></thead>"
    "<tbody>" + "\n".join(rows) + "</tbody></table></div>"
)
doc = doc.replace("<!--GLOSSARY-->", glossary_html)
doc = doc.replace("<!--TOC-->", toc_html)

# ---------------------------------------------------------------- answers
review_re = re.compile(r'<div class="review" id="review-(\d+)">(.*?)</div>\s*(?=<)', re.S)
qa_blocks = []

def strip_answers(mo):
    n, body = mo.group(1), mo.group(2)
    title = re.search(r"<h4>(.*?)</h4>", body, re.S).group(1)
    items = re.findall(r"<li>(.*?)<span class=\"answer\">(.*?)</span></li>", body, re.S)
    if not items:
        sys.exit(f"no answers found in review-{n}")
    qa = [f'<div class="qa" id="answers-{n}"><h4>{title}</h4><ol>']
    for q, a in items:
        qa.append(f'<li><span class="q">{q.strip()}</span><span class="a">{a.strip()}</span></li>')
    qa.append(f'</ol><p class="backlink"><a href="#review-{n}">Back to the Session {n} review box</a></p></div>')
    qa_blocks.append("\n".join(qa))
    cleaned = re.sub(r"<span class=\"answer\">.*?</span>", "", body, flags=re.S)
    return f'<div class="review" id="review-{n}">{cleaned}</div>\n'

doc = review_re.sub(strip_answers, doc)
doc = doc.replace("<!--ANSWERS-->", "\n".join(qa_blocks))

# ---------------------------------------------------------------- checks
ids = set(re.findall(r'\sid="([^"]+)"', doc))
dupes = [i for i in ids if len(re.findall(rf'\sid="{re.escape(i)}"', doc)) > 1]
if dupes:
    sys.exit(f"duplicate ids: {dupes}")
missing = sorted({h for h in re.findall(r'href="#([^"]+)"', doc) if h not in ids})
if missing:
    sys.exit(f"broken internal links: {missing}")

class Balance(HTMLParser):
    VOID = {"br", "img", "link", "meta", "hr", "input", "path", "rect", "circle", "line", "polygon", "polyline"}
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.errors.append((tag, self.getpos(), self.stack[-3:]))

b = Balance()
b.feed(doc)
if b.errors or b.stack:
    print("TAG BALANCE PROBLEMS:", b.errors[:10], b.stack[:10])
    sys.exit(1)

# ---------------------------------------------------------------- outputs
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

# Fragment used to publish the page as a Claude artifact.
open(os.path.join(ROOT, "course.html"), "w", encoding="utf-8").write(doc)

# Standalone page for self-hosting (GitHub Pages serves dist/index.html).
standalone = (
    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    "<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}</style>\n"
    "</head>\n<body>\n" + doc + "\n</body>\n</html>\n"
)
index_path = os.path.join(DIST, "index.html")
open(index_path, "w", encoding="utf-8").write(standalone)

# PDF export, if a Chrome/Chromium binary is available.
import shutil, subprocess
chrome = next((c for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
pdf_path = os.path.join(DIST, "Web-Architecture-Course.pdf")
if chrome and "--no-pdf" not in sys.argv:
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", f"file://{index_path}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    pdf_note = "pdf written" if os.path.exists(pdf_path) else "pdf FAILED"
else:
    pdf_note = "pdf skipped (no chrome found)" if not chrome else "pdf skipped"

words = len(re.sub(r"<[^>]+>", " ", doc).split())
print(f"ok: {len(entries)} keywords, {len(qa_blocks)} review sets, "
      f"{sum(len(re.findall('<li><span class=\"q\">', q)) for q in qa_blocks)} questions, "
      f"~{words} words, {len(doc)//1024} KB -> dist/index.html; {pdf_note}")
