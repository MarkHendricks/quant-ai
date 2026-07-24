# CLAUDE.md — quant-ai (thin shell)

@../teaching-content/shell/CLAUDE.md

## Course-specific
- No student Box channel; `make boxsync` disabled (BOX empty in Makefile)
- (env, exam workflow, and other course notes go here)

## quant-ai specifics

- The sidebar TOC is post-processed: `scripts/restructure_toc.py` (a `build`
  prerequisite) folds the assembler's flat chapters into one part per module
  with collapsible Demos and Featured Research sections. To add a chapter,
  add its item in `content.yml` BEFORE the Demos landing item; it becomes a
  top-level chapter automatically. Demos/research pages go after their
  landing item and become collapsed sections.
- Local builds assemble from the ../teaching-content WORKING TREE, which may
  be stale or on another session's branch. To build at the pin:
  `make build CONTENT=<worktree-at-pinned-sha>`. CI always builds at the pin.
- New M5 content flows: author in ai-models book/ -> run
  book/port_to_canonical.py -> land on teaching-content main (worktree if
  the shared checkout is busy) -> `make pin` here -> push (CI deploys).
