# CLAUDE.md — quant-ai (thin shell)

@../teaching-content/shell/CLAUDE.md

## Course-specific
- No student Box channel; `make boxsync` disabled (BOX empty in Makefile)
- (env, exam workflow, and other course notes go here)

## quant-ai specifics

- One `content.yml` chapter block per MODULE (the M5 block is the model).
  The sidebar TOC is post-processed: `scripts/restructure_toc.py` (a `build`
  prerequisite) turns each block into a part whose Demos and Featured
  Research chapters collapse their pages as sections, keyed on the first
  items whose basenames start with "Demos" and "Featured Research". To add a
  chapter, put its item BEFORE the module's Demos landing; demo/research
  pages go after their landing item. A new module = a new chapter block with
  its own "Demos ..."/"Featured Research ..." landing pages (basenames must
  start with those words); a block without landings renders flat.
- Local builds assemble from the ../teaching-content WORKING TREE, which may
  be stale or on another session's branch. To build at the pin:
  `make build CONTENT=<worktree-at-pinned-sha>`. CI always builds at the pin.
- New M5 content flows: author in ai-models book/ -> run
  book/port_to_canonical.py -> land on teaching-content main (worktree if
  the shared checkout is busy) -> `make pin` here -> push (CI deploys).
