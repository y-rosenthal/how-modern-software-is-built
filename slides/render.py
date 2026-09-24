"""Render the slide decks (HTML) from the SESSION dicts in slides/session*.py.

Used by build.py. Each deck is a single self-contained HTML page with one
<section class="slide"> per slide. The first slide of every book section has
the section's id (e.g. "s1-3"), so the book can link to slides/session-1.html#s1-3
and every slide carries a "Book" button back to ../#s1-3.
"""
import html
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load_sessions():
    sessions = []
    for n in range(1, 10):
        p = os.path.join(HERE, f"session{n}.py")
        if not os.path.exists(p):
            break
        spec = importlib.util.spec_from_file_location(f"session{n}", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sessions.append(mod.SESSION)
    return sessions


def slide_ids(session):
    """Yield (section_id, slide_index, slide_id) for every slide of a session."""
    for sec in session["sections"]:
        for k, _ in enumerate(sec["slides"]):
            yield sec["id"], k, (sec["id"] if k == 0 else f"{sec['id']}-{chr(97 + k)}")


DECK_CSS = """
html,body{height:100%}
body{margin:0;padding:0;overflow:hidden;background:var(--ground);color:var(--ink);font-family:var(--font-body)}
.deck{position:relative;height:100%;width:100%}
.slide{position:absolute;inset:0;display:none;flex-direction:column;padding:2.4vh 5vw 8vh;box-sizing:border-box}
.slide.active{display:flex}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:1rem;font-family:var(--font-display);font-size:clamp(12px,1.7vh,17px);color:var(--ink-2);margin-bottom:1.2vh}
.topbar .crumb{letter-spacing:0.08em;text-transform:uppercase;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.btn{font-family:var(--font-display);font-weight:700;font-size:clamp(12px,1.7vh,16px);letter-spacing:0.04em;text-decoration:none;color:var(--accent-ink);border:1.5px solid var(--accent);background:var(--surface);padding:0.3em 0.9em;border-radius:999px;white-space:nowrap}
.btn:hover{background:var(--accent-soft)}
.btn.primary{background:var(--accent);color:#fff}
.btn.primary:hover{background:var(--accent-ink)}
.slide h2{font-family:var(--font-display);font-weight:800;font-size:clamp(26px,5.4vh,58px);line-height:1.1;letter-spacing:-0.01em;margin:0 0 2.4vh;text-wrap:balance;max-width:28ch}
.slide ul{margin:0;padding-left:1.1em;font-size:clamp(17px,3.3vh,34px);line-height:1.35;max-width:38ch}
.slide li{margin-bottom:1.6vh}
.slide li b{font-weight:600;color:var(--accent-ink)}
.slide code{font-family:var(--font-mono);font-size:0.85em;background:var(--code-bg);padding:0.05em 0.3em;border-radius:4px}
.slide pre{margin:0 0 2vh;background:var(--code-bg);border:1px solid var(--line);border-radius:10px;padding:1.6vh 2vw;font-family:var(--font-mono);font-size:clamp(13px,2.5vh,25px);line-height:1.4;overflow:auto;max-height:52vh}
.slide .fig{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin:0 0 1.5vh}
.slide figure{margin:0;padding:1.5vh 1.5vw;background:var(--surface);border:1px solid var(--line);border-radius:12px;max-width:100%;max-height:100%;display:flex;flex-direction:column;align-items:center;box-sizing:border-box}
.slide figure .scroll{overflow:visible;min-height:0;display:flex;justify-content:center;width:100%}
.slide figure svg{max-width:100%;display:block;color:var(--ink);font-family:var(--font-display)}
.slide figcaption{display:none}
.slide .with-fig ul{font-size:clamp(15px,2.6vh,26px);max-width:none;display:flex;flex-wrap:wrap;gap:0 3vw;list-style:disc}
.slide .with-fig li{margin-bottom:0.6vh;flex:1 1 40%}
.slide table{border-collapse:collapse;font-size:clamp(14px,2.6vh,25px);line-height:1.3;background:var(--surface);border:1px solid var(--line);margin-bottom:2vh;max-width:100%}
.slide th,.slide td{text-align:left;padding:0.9vh 1.4vw;border-top:1px solid var(--line);vertical-align:top}
.slide th{background:var(--surface-2);font-family:var(--font-display);font-size:0.72em;letter-spacing:0.08em;text-transform:uppercase;color:var(--ink-2);border-top:0}
.slide .tbl-scroll{overflow:auto;min-height:0;margin-bottom:2vh}
.slide .takeaway{margin-top:auto;border-left:5px solid var(--accent);background:var(--surface);padding:1.2vh 1.6vw;font-family:var(--font-display);font-weight:600;font-size:clamp(15px,2.7vh,26px);line-height:1.35;border-radius:0 10px 10px 0}
.slide.title{justify-content:center;padding-bottom:10vh}
.slide.title .eyebrow{font-family:var(--font-display);font-size:clamp(13px,2vh,18px);font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--accent-ink);margin-bottom:1.5vh}
.slide.title h1{font-family:var(--font-display);font-weight:800;font-size:clamp(34px,7.5vh,84px);line-height:1.05;letter-spacing:-0.015em;margin:0 0 2vh;max-width:22ch;text-wrap:balance}
.slide.title .sub{font-size:clamp(17px,3vh,30px);color:var(--ink-2);max-width:50ch;margin:0 0 3vh}
.slide.title ol{columns:2;column-gap:4vw;font-family:var(--font-display);font-size:clamp(14px,2.3vh,22px);line-height:1.5;margin:0 0 3vh;padding-left:1.4em;max-width:80ch}
.slide.title ol a{color:var(--ink);text-decoration:none}
.slide.title ol a:hover{color:var(--accent-ink);text-decoration:underline}
.slide.title .links{display:flex;gap:1rem;flex-wrap:wrap}
.bottombar{position:fixed;left:0;right:0;bottom:0;height:6vh;min-height:40px;display:flex;align-items:center;justify-content:space-between;padding:0 5vw calc(0px + env(safe-area-inset-bottom,0px));font-family:var(--font-display);font-size:clamp(12px,1.7vh,16px);color:var(--ink-2);background:var(--ground);border-top:1px solid var(--line);box-sizing:border-box}
.bottombar .nav{display:flex;gap:0.5rem;align-items:center}
.bottombar button{font:inherit;font-weight:700;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:0.3em 0.9em;cursor:pointer}
.bottombar button:hover{border-color:var(--accent);color:var(--accent-ink)}
.bottombar button:focus-visible,.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.progress{position:fixed;left:0;bottom:calc(6vh + env(safe-area-inset-bottom,0px));height:3px;background:var(--accent);width:0;transition:width .2s}
@media (prefers-reduced-motion: reduce){.progress{transition:none}}
.hint{font-size:0.9em;opacity:0.8}
@media (max-width:700px){.slide{padding:2vh 4vw 9vh}.slide.title ol{columns:1}.slide .with-fig li{flex-basis:100%}.hint{display:none}}
"""

DECK_JS = """
(function(){
  var slides=Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var i=0, counter=document.getElementById('counter'), bar=document.getElementById('progress');
  function show(n, push){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach(function(s,k){s.classList.toggle('active',k===i);});
    counter.textContent=(i+1)+' / '+slides.length;
    bar.style.width=((i+1)/slides.length*100)+'%';
    if(push!==false){try{history.replaceState(null,'','#'+slides[i].id);}catch(e){}}
    document.title=slides[i].getAttribute('data-title')+' · '+DECK_TITLE;
  }
  function fromHash(){
    var h=location.hash.replace('#','');
    var k=-1; slides.forEach(function(s,idx){if(s.id===h)k=idx;});
    show(k<0?0:k,false);
  }
  window.next=function(){show(i+1);};
  window.prev=function(){show(i-1);};
  document.addEventListener('keydown',function(e){
    if(e.target && (e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA'))return;
    switch(e.key){
      case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': e.preventDefault(); show(i+1); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp': e.preventDefault(); show(i-1); break;
      case 'Home': e.preventDefault(); show(0); break;
      case 'End': e.preventDefault(); show(slides.length-1); break;
      case 'f': case 'F': toggleFull(); break;
    }
  });
  function toggleFull(){
    try{
      if(document.fullscreenElement){document.exitFullscreen();}
      else if(document.documentElement.requestFullscreen){document.documentElement.requestFullscreen().catch(function(){});}
    }catch(e){}
  }
  document.getElementById('fullbtn').addEventListener('click',toggleFull);
  document.getElementById('prevbtn').addEventListener('click',function(){show(i-1);});
  document.getElementById('nextbtn').addEventListener('click',function(){show(i+1);});
  window.addEventListener('hashchange',fromHash);
  fromHash();
})();
"""


def _bullets(items):
    return "<ul>" + "".join(f"<li>{b}</li>" for b in items) + "</ul>"


def _table(t):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in t["head"])
    rows = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
    return f'<div class="tbl-scroll"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def render_deck(session, figures, head_css, book_href="../", pptx_href=None):
    """Return the HTML of one session's deck. `figures` maps fig id -> <figure> html."""
    n = session["n"]
    title = session["title"]
    out = []
    out.append(f"<title>Session {n} Slides</title>")
    out.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap">')
    out.append("<style>" + head_css + DECK_CSS + "</style>")
    out.append('<div class="deck">')

    # title slide
    toc = "".join(
        f'<li><a href="#{sec["id"]}">{html.escape(sec["title"])}</a></li>' for sec in session["sections"]
    )
    links = f'<a class="btn primary" href="{book_href}#session-{n}">Open the book chapter</a>'
    if pptx_href:
        links += f' <a class="btn" href="{pptx_href}">Download as PowerPoint</a>'
    out.append(
        f'<section class="slide title active" id="title" data-title="Session {n}">'
        f'<div class="eyebrow">Session {n} · 75 minutes · slides</div>'
        f"<h1>{html.escape(title)}</h1>"
        f'<p class="sub">{html.escape(session.get("subtitle", ""))}</p>'
        f"<ol>{toc}</ol>"
        f'<div class="links">{links}</div>'
        f'<p class="hint">Arrow keys or space to move, F for full screen. Every slide has a Book button back to the full text.</p>'
        "</section>"
    )

    for sec in session["sections"]:
        sec_slides = sec["slides"]
        for k, sl in enumerate(sec_slides):
            sid = sec["id"] if k == 0 else f"{sec['id']}-{chr(97 + k)}"
            body = []
            cls = "slide"
            has_fig = "fig" in sl
            if has_fig:
                cls += " with-fig"
                fig_html = figures.get("fig-" + sl["fig"])
                if fig_html is None:
                    raise SystemExit(f"slide references unknown figure fig-{sl['fig']}")
            body.append(f"<h2>{sl['title']}</h2>")
            if "code" in sl:
                body.append(f"<pre>{html.escape(sl['code'])}</pre>")
            if "table" in sl:
                body.append(_table(sl["table"]))
            if has_fig:
                vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', fig_html)
                w, h = (int(vb.group(1)), int(vb.group(2))) if vb else (720, 300)
                avail = 50 if sl.get("bullets") else 66  # vh available for the drawing
                sized = fig_html.replace(
                    "<svg ", f'<svg style="width:min(88vw,{avail * w / h:.1f}vh);height:auto;aspect-ratio:{w}/{h}" ', 1)
                body.append(f'<div class="fig">{sized}</div>')
            if sl.get("bullets"):
                body.append(_bullets(sl["bullets"]))
            if sl.get("takeaway"):
                body.append(f'<div class="takeaway">{sl["takeaway"]}</div>')
            crumb = f"Session {n} · {html.escape(sec['title'])}" + (f" · {k + 1}/{len(sec_slides)}" if len(sec_slides) > 1 else "")
            out.append(
                f'<section class="{cls}" id="{sid}" data-title="{html.escape(sec["title"])}">'
                f'<div class="topbar"><span class="crumb">{crumb}</span>'
                f'<a class="btn" href="{book_href}#{sec["id"]}" title="Open this section in the full text">Book ↗</a></div>'
                + "".join(body)
                + "</section>"
            )

    out.append("</div>")
    out.append('<div class="progress" id="progress"></div>')
    out.append(
        '<div class="bottombar"><span id="counter">1 / 1</span>'
        f'<span class="hint">{html.escape(title)}</span>'
        '<span class="nav"><button id="prevbtn" type="button" aria-label="Previous slide">‹ Prev</button>'
        '<button id="nextbtn" type="button" aria-label="Next slide">Next ›</button>'
        '<button id="fullbtn" type="button" aria-label="Toggle full screen">Full screen</button></span></div>'
    )
    out.append("<script>var DECK_TITLE=" + json.dumps(f"Session {n} Slides") + ";" + DECK_JS + "</script>")
    return "\n".join(out)


def extract_figures(doc):
    """Map figure id -> figure html for every <figure id="fig-..."> in the assembled book."""
    figs = {}
    for m in re.finditer(r'<figure id="(fig-[^"]+)">(.*?)</figure>', doc, re.S):
        inner = m.group(2)
        # make marker ids unique per deck by leaving them; each deck embeds each figure once
        figs[m.group(1)] = f'<figure id="{m.group(1)}-slide">{inner}</figure>'
    return figs


def head_css_from(head_html):
    m = re.search(r"<style>(.*?)</style>", head_html, re.S)
    return m.group(1) if m else ""
