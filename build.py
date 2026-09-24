#!/usr/bin/env python3
"""Assemble the course document from the source chunks in src/.

Generates: the table of contents, the keyword glossary (Appendix A) from every
<dfn class="kw"> in the text, and the answers appendix (Appendix B) from the
review-question boxes. Writes:

  course.html        - page fragment (what the Claude Artifact tool publishes)
  dist/index.html    - standalone page for self-hosting (GitHub Pages)
  dist/slides/*.html - one HTML slide deck per session (from slides/session*.py)
  dist/slides/*.pptx - PowerPoint export of each deck (needs .venv with python-pptx; skip with --no-pptx)
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
SITE = "https://y-rosenthal.github.io/how-modern-software-is-built/"
sys.path.insert(0, os.path.join(ROOT, "slides"))
import render as slides_render  # noqa: E402

parts = sorted(glob.glob(os.path.join(SRC, "*.html")))
doc = "\n".join(open(p, encoding="utf-8").read() for p in parts)

# ---------------------------------------------------------------- figure ids
# Every <figure> inside a section wrapper gets id="fig-<section>-<n>" so the
# slide decks can embed the same diagram.
def _number_figures(doc):
    chunks = re.split(r'(<section id="s\d-\d-wrap">)', doc)
    out, sec = [], None
    for chunk in chunks:
        m = re.match(r'<section id="(s\d-\d)-wrap">', chunk)
        if m:
            sec = m.group(1)
            out.append(chunk)
            continue
        if sec:
            k = [0]
            def repl(_m):
                k[0] += 1
                return f'<figure id="fig-{sec}-{k[0]}">'
            chunk = re.sub(r"<figure>", repl, chunk)
        out.append(chunk)
    return "".join(out)

doc = _number_figures(doc)

# ---------------------------------------------------------------- slide buttons
def _add_slide_buttons(doc, base):
    """Add Slides buttons next to every section heading and session header.
    `base` is the prefix for deck links ("" for the site, SITE for the artifact)."""
    def h3(m):
        sid = m.group(1)
        n = sid[1]
        return (m.group(0)[:-5] +
                f' <a class="slides-btn" href="{base}slides/session-{n}.html#{sid}" title="Open this section as slides">Slides</a></h3>')
    doc = re.sub(r'<h3 id="(s\d-\d)">.*?</h3>', h3, doc, flags=re.S)
    def eyebrow(m):
        n = m.group(1)
        return (f'<div class="eyebrow">Session {n} · 75 minutes'
                f' <a class="slides-btn" href="{base}slides/session-{n}.html" title="Open this session as slides">Slides</a>'
                f' <a class="slides-btn alt" href="{base}slides/session-{n}.pptx" title="Download this session as a PowerPoint file">PowerPoint</a></div>')
    doc = re.sub(r'<div class="eyebrow">Session (\d) · 75 minutes</div>', eyebrow, doc)
    return doc

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

# Fragment used to publish the page as a Claude artifact (absolute deck links).
open(os.path.join(ROOT, "course.html"), "w", encoding="utf-8").write(_add_slide_buttons(doc, SITE))

# Standalone page for self-hosting (GitHub Pages serves dist/index.html).
def _standalone(fragment):
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}</style>\n"
        "</head>\n<body>\n" + fragment + "\n</body>\n</html>\n"
    )

site_doc = _add_slide_buttons(doc, "")
index_path = os.path.join(DIST, "index.html")
open(index_path, "w", encoding="utf-8").write(_standalone(site_doc))

# ---------------------------------------------------------------- slide decks
SLIDES_DIR = os.path.join(DIST, "slides")
os.makedirs(SLIDES_DIR, exist_ok=True)
head_css = slides_render.head_css_from(open(os.path.join(SRC, "00-head.html"), encoding="utf-8").read())
figures = slides_render.extract_figures(doc)
sessions = slides_render.load_sessions()
n_slides = 0
for session in sessions:
    deck = slides_render.render_deck(session, figures, head_css, book_href="../", pptx_href=f"session-{session['n']}.pptx")
    open(os.path.join(SLIDES_DIR, f"session-{session['n']}.html"), "w", encoding="utf-8").write(_standalone(deck))
    n_slides += 1 + sum(len(sec["slides"]) for sec in session["sections"])
# every book section must have slides, and every deck section must exist in the book
book_sections = set(re.findall(r'<h3 id="(s\d-\d)">', doc))
deck_sections = {sec["id"] for se in sessions for sec in se["sections"]}
if book_sections != deck_sections:
    sys.exit(f"section mismatch between book and slides: {sorted(book_sections ^ deck_sections)}")

# ---------------------------------------------------------------- figure PNGs + PowerPoint
import hashlib, json, shutil, subprocess
chrome = next((c for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c)), None)
FIG_CACHE = os.path.join(ROOT, "build", "figs")
os.makedirs(FIG_CACHE, exist_ok=True)
fig_pngs = {}
if chrome and "--no-pptx" not in sys.argv:
    for fid, fhtml in figures.items():
        m = re.search(r'viewBox="0 0 (\d+) (\d+)"', fhtml)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (720, 300)
        digest = hashlib.md5((fhtml + head_css).encode()).hexdigest()[:12]
        png = os.path.join(FIG_CACHE, f"{fid}-{digest}.png")
        fig_pngs[fid] = png
        if os.path.exists(png):
            continue
        wrapper = os.path.join(FIG_CACHE, f"{fid}.html")
        open(wrapper, "w", encoding="utf-8").write(
            "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>" + head_css +
            f"body{{margin:0;padding:0;background:#fff}}figure{{margin:0;border:0;padding:16px;border-radius:0;background:#fff}}"
            f"figcaption{{display:none}}.scroll{{overflow:visible}}figure svg{{width:{w}px;height:{h}px;max-width:none}}"
            "</style></head><body>" + fhtml + "</body></html>")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                        "--force-device-scale-factor=2", f"--window-size={w + 32},{h + 32}",
                        f"--screenshot={png}", f"file://{wrapper}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
venv_py = os.path.join(ROOT, ".venv", "bin", "python")
pptx_note = "pptx skipped"
if "--no-pptx" not in sys.argv and os.path.exists(venv_py):
    spec = {"site": SITE, "figures": fig_pngs, "out_dir": SLIDES_DIR, "sessions": sessions}
    spec_path = os.path.join(ROOT, "build", "pptx-spec.json")
    json.dump(spec, open(spec_path, "w"), indent=1)
    r = subprocess.run([venv_py, os.path.join(ROOT, "slides", "render_pptx.py"), spec_path], capture_output=True, text=True)
    pptx_note = "pptx written" if r.returncode == 0 else "pptx FAILED: " + r.stderr.strip().splitlines()[-1]
elif "--no-pptx" not in sys.argv:
    pptx_note = "pptx skipped (no .venv with python-pptx; see README)"

# PDF export, if a Chrome/Chromium binary is available.
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
      f"~{words} words, {len(doc)//1024} KB -> dist/index.html; {len(sessions)} decks, {n_slides} slides; {pptx_note}; {pdf_note}")
