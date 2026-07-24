# quant-ai — thin shell; all logic lives in ../teaching-content/shell/book.mk
# No student Box channel for this course: BOX is intentionally empty and
# `make boxsync` is disabled. Set BOX to enable one.
BOX =
include ../teaching-content/shell/book.mk

# --- course-specific targets (not in book.mk) ---
# One part per module in the sidebar: the assembler emits flat chapters, so a
# post-assemble rewrite nests the Demos and Featured Research pages as
# collapsible sections. Runs between assemble and jupyter-book build.
.PHONY: restructure-toc
restructure-toc: assemble
	$(PY) scripts/restructure_toc.py
build: restructure-toc
