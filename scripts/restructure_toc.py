#!/usr/bin/env python3
"""Post-assemble TOC restructure for quant-ai.

The shared assembler emits every manifest item as a flat chapter. This book
wants each module as one part whose Demos and Featured Research chapters
collapse their pages as sections. Runs after `make assemble` (see Makefile);
docs/_toc.yml stays generated and gitignored.
"""
import sys
from pathlib import Path

TOC = Path(__file__).resolve().parents[1] / "docs" / "_toc.yml"

# Main chapters are derived, not listed: every file before the Demos landing
# (manifest order) is a chapter, so a newly authored chapter flows through
# without touching this script.
DEMOS_LANDING = "discussions/quant_ai/Demos"
RESEARCH_LANDING = "discussions/quant_ai/Featured Research"

def parse_generated(text):
    files = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('- file: "'):
            files.append(line[len('- file: "'):-1])
    return files

def main():
    files = parse_generated(TOC.read_text())
    for f in (DEMOS_LANDING, RESEARCH_LANDING):
        if f not in files:
            sys.exit(f"restructure_toc: expected file missing from generated toc: {f}")
    mains = files[:files.index(DEMOS_LANDING)]
    demos = files[files.index(DEMOS_LANDING) + 1:files.index(RESEARCH_LANDING)]
    research = files[files.index(RESEARCH_LANDING) + 1:]
    if not (mains and demos and research):
        sys.exit("restructure_toc: unexpected empty group; check content.yml order")
    L = ["format: jb-book", "root: index", "parts:",
         "- caption: Generative Scenario Analysis", "  chapters:"]
    for f in mains:
        L += [f'  - file: "{f}"']
    L += [f'  - file: "{DEMOS_LANDING}"', "    sections:"]
    for f in demos:
        L += [f'    - file: "{f}"']
    L += [f'  - file: "{RESEARCH_LANDING}"', "    sections:"]
    for f in research:
        L += [f'    - file: "{f}"']
    TOC.write_text("\n".join(L) + "\n")
    print(f"restructure_toc: 1 part, {len(mains)+2} chapters, "
          f"{len(demos)} demo + {len(research)} research sections")

if __name__ == "__main__":
    main()
