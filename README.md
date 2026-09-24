# How Modern Software Is Built — course module

Five 75-minute sessions on choosing a programming language and the architecture of websites, mobile apps, desktop
programs, and embedded software, written for business students.

## Hosting

Everything needed to host the course is in `dist/`:

- `dist/index.html` — the complete document, self-contained (fonts load from
  Google Fonts; everything else is inline).
- `dist/Web-Architecture-Course.pdf` — PDF export of the same document.

Copy `dist/` to any static web host, or use GitHub Pages: the workflow in
`.github/workflows/pages.yml` publishes `dist/` automatically on every push to
`main`. In the repository settings, under Pages, the source must be set to
"GitHub Actions" (done once).

## Editing

Sources are in `src/` (one file per session, plus styles and appendices).
`build.py` assembles them and generates the table of contents, the keyword
glossary (Appendix A) and the answers appendix (Appendix B):

    python3 build.py          # writes dist/index.html, dist/*.pdf, course.html
    python3 build.py --no-pdf # skip the PDF (the PDF needs Google Chrome)

- To add a keyword, wrap its first mention as
  `<dfn class="kw" id="kw-something" data-def="Short definition.">term</dfn>`.
- To add a review question, add an `<li>` to the session's review box with the
  answer in a trailing `<span class="answer">…</span>`.
- `course.html` is the same content as a page fragment, used for publishing
  as a Claude artifact.

Commit the regenerated `dist/` along with your source changes so the published
site stays in sync.
