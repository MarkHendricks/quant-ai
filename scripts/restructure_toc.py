#!/usr/bin/env python3
"""Post-assemble TOC restructure for quant-ai.

The shared assembler emits every manifest item as a flat chapter. Both modules
in this book read as six groups — Background, Investigations, Further Analysis,
Ongoing Work, Technical Appendix, Research — each opening on its own landing
page, with the investigations and the engine comparison carrying a further
level. This script rewrites the generated flat `docs/_toc.yml` into that shape.

The structure is declared in STRUCTURE below rather than inferred. The earlier
version read the split off `Demos` and `Featured Research` landing pages by
basename; the 2026-08-06 route restructure retired both `Demos` pages, so the
inference stopped matching and each part silently rendered flat — a whole
sidebar lost with no error. Declaring the structure makes that class of drift
loud: STRUCTURE and the assembled page set are compared exactly, in both
directions, and any disagreement fails the build.

Adding, renaming, or retiring a page therefore takes two edits — `content.yml`
selects it, STRUCTURE places it — and skipping either one stops the build with
the offending path named.

Titles: the assembler derives each sidebar label from the page's filename stem,
which is why canonical destinations carry public names. A `title` in STRUCTURE
overrides that label for the sidebar only, for the cases where the group already
supplies the context the filename cannot (the investigation sequence, the group
landing pages whose canonical stems carry a disambiguating suffix).

Runs after `make assemble` (see Makefile); docs/_toc.yml stays generated and
gitignored.
"""
import sys
from pathlib import Path

TOC = Path(__file__).resolve().parents[1] / "docs" / "_toc.yml"

D = "discussions/quant_ai/"
R = "discussions/quant_ai/research/"


def page(path, title=None, children=()):
    return {"file": path, "title": title, "children": list(children)}


# Part caption -> the six groups, in reading order. Each group is a landing
# page and its sections; a section may carry its own sections.
#
# The captions and their order mirror the source book's own _toc.yml, which is
# the reviewed artifact and the authority for the deployed site. A caption here
# has to match `content.yml`'s chapter title exactly — that is what the
# assembler writes into the flat TOC and what this table is keyed on — and the
# part order is set by the chapter block order there, not by this dict. The
# hero tiles in docs/index.md open the two modules in the same order.
STRUCTURE = {
    "Time-Series Foundation Models": [
        page(D + "Background", None, [
            page(D + "Foundation Models for Forecasting"),
            page(D + "How Time-Series Foundation Models Work"),
        ]),
        page(D + "Investigations", None, [
            page(D + "Investigation 1 - Across Five Markets",
                 "Investigation 1: Across Five Markets"),
            page(D + "Comparator Choice and Forecast Horizon",
                 "Investigation 2: Across Horizons and Benchmarks"),
            page(D + "Held-Out Adaptation",
                 "Investigation 3: With Local Adaptation"),
            page(D + "Covariates and Portfolio Volatility",
                 "Investigation 4: With Covariates"),
            page(D + "Clock and Calendar Information",
                 "Investigation 5: At Intraday Frequencies"),
        ]),
        page(D + "Further Analysis", None, [
            page(D + "Across-Session Volatility"),
            page(D + "The Weekly Five-Market Design"),
            page(D + "What Might Explain the Cross-Market Results"),
        ]),
        page(D + "Ongoing Work"),
        page(D + "Technical Appendix", None, [
            page(D + "Context to Forecast Quantiles"),
            page(D + "Forecast Targets and Baselines"),
            page(D + "The Cross-Asset Panel"),
            page(D + "Calibration"),
            page(D + "The Basket"),
        ]),
        page(D + "Research", None, [
            page(R + "Forecasting Realized Volatility at Scale"),
            page(R + "Leakage and Lineage", "Leakage via Weights"),
            page(R + "What the Benchmarks Measure"),
            page(R + "Adaptation and Financial Specialization"),
            page(R + "Calibration and Richer Information"),
            page(R + "Two Controls from Outside the Panel"),
            page(D + "Research Appendix"),
        ]),
    ],
    "Generative Scenario Analysis": [
        page(D + "Background - Scenarios", "Background", [
            page(D + "Generative Models and Scenario Analysis"),
            page(D + "What a Generative Model Is"),
            page(D + "The Market Object"),
        ]),
        page(D + "Investigations - Scenarios", "Investigations", [
            page(D + "Investigation 1 - One-Day Surfaces",
                 "Investigation 1: One-Day Surfaces", [
                     page(D + "The Conditional Experiment"),
                 ]),
            page(D + "Hedging", "Investigation 2: Hedging", [
                page(D + "GAN Hedging Scenarios"),
            ]),
            page(D + "Multi-Day Paths", "Investigation 3: Multi-Day Paths"),
        ]),
        page(D + "Further Analysis - Scenarios", "Further Analysis", [
            page(D + "Scenario Engines Under Test", None, [
                page(D + "VAE Surface Scenarios"),
                page(D + "Diffusion Surface Forecasts"),
                page(D + "The Families, Compared"),
            ]),
            page(D + "Failure Modes and Next Tests"),
        ]),
        page(D + "Ongoing Work - Scenarios", "Ongoing Work"),
        page(D + "Technical Appendix - Scenarios", "Technical Appendix", [
            page(D + "Constraint Tests"),
        ]),
        page(D + "The Research Record", "Research", [
            page(D + "The Field"),
            page(D + "Synthetic Training Data"),
            page(D + "Research Appendix - Scenarios", "Research Appendix", [
                page(R + "VolGAN"),
                page(R + "Data-Driven Hedging"),
                page(R + "Diffusion IV Forecasting"),
                page(R + "Tail-GAN"),
                page(R + "Generative Models for VaR"),
                page(R + "Neural-SDE Market Models"),
                page(R + "Diffusion Factor Models"),
                page(R + "The Koshiyama Null"),
                page(R + "GenCast Evaluation Pattern"),
                page(R + "Scenario-Generator Validation"),
                page(R + "Arbitrage-Free SVI"),
                page(R + "Multivariate Proper Scoring"),
            ]),
        ]),
    ],
}


def parse_parts(text):
    """Read the assembled flat TOC: [(caption, {file: assembler title})]."""
    parts, cur, last = [], None, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- caption:"):
            cur = (s[len("- caption:"):].strip(), {})
            parts.append(cur)
            last = None
        elif s.startswith('- file: "') and cur is not None:
            last = s[len('- file: "'):-1]
            cur[1][last] = None
        elif s.startswith('title: "') and cur is not None and last:
            cur[1][last] = s[len('title: "'):-1]
    return parts


def walk(nodes):
    for nd in nodes:
        yield nd
        yield from walk(nd["children"])


def emit(nodes, depth, titles, out):
    """Render one level; jb-book nests `sections:` under each entry."""
    pad = "  " * (depth + 1)
    for nd in nodes:
        out.append(f'{pad}- file: "{nd["file"]}"')
        title = nd["title"] or titles.get(nd["file"])
        if title:
            out.append(f'{pad}  title: "{title}"')
        if nd["children"]:
            out.append(f"{pad}  sections:")
            emit(nd["children"], depth + 1, titles, out)


def restructure(caption, titles):
    groups = STRUCTURE.get(caption)
    if groups is None:
        sys.exit(f"restructure_toc: no declared structure for part {caption!r}; "
                 "add it to STRUCTURE or the part would render flat")
    declared = [nd["file"] for nd in walk(groups)]
    dupes = sorted({f for f in declared if declared.count(f) > 1})
    if dupes:
        sys.exit(f"restructure_toc: {caption}: page declared twice: {dupes}")
    assembled = set(titles)
    missing = sorted(set(declared) - assembled)
    extra = sorted(assembled - set(declared))
    if missing or extra:
        sys.exit(
            f"restructure_toc: {caption}: STRUCTURE and the assembled page set "
            f"disagree.\n  declared but not assembled (check content.yml and "
            f"the canonical port): {missing}\n  assembled but not placed (add "
            f"it to STRUCTURE): {extra}")

    out = [f"- caption: {caption}", "  chapters:"]
    emit(groups, 0, titles, out)
    counts = "/".join(str(len(g["children"])) for g in groups)
    return out, (f"{caption}: {len(groups)} groups, {len(declared)} pages "
                 f"(sections per group {counts})")


def main():
    parts = parse_parts(TOC.read_text())
    if not parts:
        sys.exit("restructure_toc: no parts found in generated toc")
    L = ["format: jb-book", "root: index", "parts:"]
    reports = []
    for caption, titles in parts:
        lines, report = restructure(caption, titles)
        L += lines
        reports.append(report)
    TOC.write_text("\n".join(L) + "\n")
    for r in reports:
        print(f"restructure_toc: {r}")


if __name__ == "__main__":
    main()
