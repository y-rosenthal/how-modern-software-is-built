# How Modern Software Is Built (in 2026) — course module

Five 75-minute sessions on choosing a programming language and the architecture of websites, mobile apps, desktop
programs, and embedded software, written for business students.

## Hosting

Everything needed to host the course is in `dist/`:

- `dist/index.html` — the complete document, self-contained (fonts load from
  Google Fonts; everything else is inline).
- `dist/Web-Architecture-Course.pdf` — PDF export of the same document.
- `dist/slides/session-N.html` — one slide deck per session. Every section
  heading in the book has a Slides button that opens the matching slide, and
  every slide has a Book button back to the section.
- `dist/slides/session-N.pptx` — the same decks as PowerPoint files.

Copy `dist/` to any static web host, or use GitHub Pages: the workflow in
`.github/workflows/pages.yml` publishes `dist/` automatically on every push to
`main`. In the repository settings, under Pages, the source must be set to
"GitHub Actions" (done once).

## Editing

Sources are in `src/` (one file per session, plus styles and appendices).
`build.py` assembles them and generates the table of contents, the keyword
glossary (Appendix A) and the answers appendix (Appendix B):

    python3 build.py           # writes dist/index.html, dist/slides/*, dist/*.pdf, course.html
    python3 build.py --no-pdf  # skip the PDF (the PDF needs Google Chrome)
    python3 build.py --no-pptx # skip the PowerPoint files

The PowerPoint export needs the `python-pptx` package in a project venv
(one-time setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`)
and Google Chrome to render the diagrams to images. Without them the build still
produces the site and the HTML decks.

Slide content lives in `slides/session1.py` … `slides/session5.py`: one entry
per book section, each with a few slides of bullets, a table, a code snippet,
or a diagram reused from the book (`"fig": "s4-4-2"` refers to the second
figure in section 4.4). The build fails if a book section has no slides.

- To add a keyword, wrap its first mention as
  `<dfn class="kw" id="kw-something" data-def="Short definition.">term</dfn>`.
- To add a review question, add an `<li>` to the session's review box with the
  answer in a trailing `<span class="answer">…</span>`.
- `course.html` is the same content as a page fragment, used for publishing
  as a Claude artifact.

Commit the regenerated `dist/` along with your source changes so the published
site stays in sync.
