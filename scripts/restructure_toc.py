#!/usr/bin/env python3
"""Post-assemble TOC restructure for quant-ai.

The shared assembler emits every manifest item as a flat chapter. This book
wants each module (one manifest chapter block = one generated part) to render
as: part caption, top-level chapters, then collapsible Demos and Featured
Research chapters holding their pages as sections.

Per part, the split is inferred from landing pages by basename: the first
file whose basename starts with "Demos" starts the demo sections; the first
whose basename starts with "Featured Research" starts the research sections.
A part with neither is left flat. New chapters flow through automatically:
anything before the Demos landing stays top-level.

Runs after `make assemble` (see Makefile); docs/_toc.yml stays generated and
gitignored.
"""
import sys
from pathlib import Path

TOC = Path(__file__).resolve().parents[1] / "docs" / "_toc.yml"


def parse_parts(text):
    parts, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- caption:"):
            cur = {"caption": s[len("- caption:"):].strip(), "files": []}
            parts.append(cur)
        elif s.startswith('- file: "') and cur is not None:
            cur["files"].append(s[len('- file: "'):-1])
    return parts


def basename(f):
    return f.rsplit("/", 1)[-1]


def restructure(part):
    files = part["files"]
    demos_i = next((i for i, f in enumerate(files)
                    if basename(f).startswith("Demos")), None)
    research_i = next((i for i, f in enumerate(files)
                       if basename(f).startswith("Featured Research")), None)
    L = [f"- caption: {part['caption']}", "  chapters:"]
    if demos_i is None or research_i is None or not demos_i < research_i:
        for f in files:
            L.append(f'  - file: "{f}"')
        return L, f"{part['caption']}: flat ({len(files)} chapters)"
    mains = files[:demos_i]
    demos = files[demos_i + 1:research_i]
    research = files[research_i + 1:]
    if not (mains and demos and research):
        sys.exit(f"restructure_toc: empty group in part {part['caption']!r}; "
                 "check content.yml order")
    for f in mains:
        L.append(f'  - file: "{f}"')
    L += [f'  - file: "{files[demos_i]}"', "    sections:"]
    for f in demos:
        L.append(f'    - file: "{f}"')
    L += [f'  - file: "{files[research_i]}"', "    sections:"]
    for f in research:
        L.append(f'    - file: "{f}"')
    return L, (f"{part['caption']}: {len(mains)} chapters, "
               f"{len(demos)} demo + {len(research)} research sections")


def main():
    parts = parse_parts(TOC.read_text())
    if not parts:
        sys.exit("restructure_toc: no parts found in generated toc")
    L = ["format: jb-book", "root: index", "parts:"]
    reports = []
    for part in parts:
        lines, report = restructure(part)
        L += lines
        reports.append(report)
    TOC.write_text("\n".join(L) + "\n")
    for r in reports:
        print(f"restructure_toc: {r}")


if __name__ == "__main__":
    main()
