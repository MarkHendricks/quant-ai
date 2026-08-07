# CLAUDE.md — quant-ai (thin shell)

@../teaching-content/shell/CLAUDE.md

## Course-specific
- No student Box channel; `make boxsync` disabled (BOX empty in Makefile)
- (env, exam workflow, and other course notes go here)

## quant-ai specifics

- One `content.yml` chapter block per MODULE. The sidebar TOC is
  post-processed: `scripts/restructure_toc.py` (a `build` prerequisite) turns
  each block into a part with six collapsible groups — Background,
  Investigations, Further Analysis, Ongoing Work, Technical Appendix,
  Research. The grouping is DECLARED in that script's `STRUCTURE` table, not
  inferred from page names. Adding, renaming, or retiring a page therefore
  takes two edits — `content.yml` selects it, `STRUCTURE` places it — and the
  script fails the build, naming the path, if the two disagree in either
  direction. (It used to infer the split from `Demos`/`Featured Research`
  landing pages; when the 2026-08-06 route restructure retired the `Demos`
  pages the inference stopped matching and both parts would have rendered
  flat. Declaring the structure is what makes that failure loud.)
- **The root page is a PORT, not an original.** `docs/index.md` is the source
  book's reviewed results landing (`ai-models` `index.md`), byte for byte below
  the H1 except that every route gains the canonical `quant_ai/` directory and
  the two investigation stems land under their ruled labels. When the book's
  landing changes, **re-port it** — do not hand-edit here, and do not author a
  parallel summary, or the deployed landing and the reviewed landing drift
  apart silently. Its navy part band and porch are styled by
  `docs/_static/landing.css`, keyed to the section ids Sphinx generates from
  the two H2 part titles; `custom.css` stays variables-only, which is what
  `check_shell.py` expects.
- Part order and part captions come from `content.yml`'s chapter blocks and
  mirror the book's own part order. Three surfaces read them and must move
  together: the chapter blocks, `STRUCTURE` in `scripts/restructure_toc.py`
  (keyed on the caption), and the landing's two H2s plus the `landing.css`
  selectors keyed on their generated ids.
- **Indexing is ON.** The URL was shared on 2026-08-07, so `_noindex: .` is
  commented out under `sphinx.local_extensions` in `docs/_config.yml`. Do not
  restore the noindex extension unless Mark explicitly moves the book back to
  staging. The original rationale and verification command remain in
  `docs/_noindex.py`.
- Local builds assemble from the ../teaching-content WORKING TREE, which may
  be stale or on another session's branch. To build at the pin:
  `make build CONTENT=<worktree-at-pinned-sha>`. CI always builds at the pin.
- New M5 content flows: author in ai-models book/ -> run
  book/port_to_canonical.py -> land on teaching-content main (worktree if
  the shared checkout is busy) -> `make pin` here -> push (CI deploys).
