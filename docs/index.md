---
title: "Quant AI"
---

<!-- The root page is the reviewed results landing, ported from the source
     book's index.md at ai-models d2f6f85d. It is that file byte for byte
     below the H1, except that every route gains the canonical quant_ai/
     directory and the two investigation stems land under their ruled
     labels (M026). Do not author a parallel summary here: re-port instead,
     so the deployed landing and the reviewed landing cannot drift.

     The navy part band and the pale porch beneath it are styled by
     _static/landing.css, keyed to the section ids Sphinx generates from
     the two H2 part titles. Renaming a part title changes those ids and
     the selectors have to follow. -->

# Quant AI

## Time-Series Foundation Models

:::{div} part-porch
Five experiments ask whether released forecasting models improve on classical volatility
forecasts.

[Background](discussions/quant_ai/Background.md) · [Investigations](discussions/quant_ai/Investigations.md) · [Further Analysis](discussions/quant_ai/Further%20Analysis.md) · [Research](discussions/quant_ai/Research.md)
:::

Every scored origin follows the latest public release among the 4 scored zero-shot
models; later-added comparators are shown as context.

- Five experiments. Every one is zero-shot except Investigation 3.
- The five forecast objects differ, so no two results are combined and there is no overall win rate.
- Each is read against the published record, collected in [Research](discussions/quant_ai/Research.md).

| Investigation | Forecast object |
|---|---|
| [1. Across Five Markets](discussions/quant_ai/Investigation%201%20-%20Across%20Five%20Markets.md) | Next-session realized volatility, regular session, issued daily; ES, NQ, TY, CL, GC |
| [2. Across Horizons and Benchmarks](discussions/quant_ai/Comparator%20Choice%20and%20Forecast%20Horizon.md) | Realized volatility 1, 5 and 22 sessions ahead; 26-future panel |
| [3. With Local Adaptation](discussions/quant_ai/Held-Out%20Adaptation.md) | Realized-volatility quantiles on futures excluded from fitting |
| [4. With Covariates](discussions/quant_ai/Covariates%20and%20Portfolio%20Volatility.md) | Forward five-session volatility of a nine-sector basket, issued weekly |
| [5. At Intraday Frequencies](discussions/quant_ai/Clock%20and%20Calendar%20Information.md) | Hourly futures and equity realized volatility, and a frozen event grid |

:::{div} part-jump
[Jump to Generative Scenario Analysis ↓](#generative-scenario-analysis)
:::

### Finding 1. Zero-shot captures most of the classical gain

Pooled q50 MAE on 881 daily one-session origins across ES, NQ, TY, CL and GC:

| Forecast | MAE, vol points | Error reduction on no-change |
|---|---:|---:|
| No-change | 4.05 | reference |
| Four zero-shot models | 3.55 to 3.58 | 11.7% to 12.5% |
| Validation-selected classical | 3.51 | 13.4% |

- The models capture **87% to 93%** of the classical forecast's improvement and stay **1.1% to 2.0%** above its MAE.
- The comparator is HAR or log-HAR, chosen per market on an earlier 252-origin grid.
- Scoring against no-change measures skill at forecasting the change, not persistence.

[The pool](discussions/quant_ai/Investigation%201%20-%20Across%20Five%20Markets.md#what-the-pool-says)

### Finding 2. Comparator construction changes the verdict

Chronos-2 at 120M, one session ahead on the 26-future panel, as a share of each
comparator's loss:

| Classical comparator | Ratio |
|---|---:|
| One-standard-error simplicity floor | 0.846 |
| Pre-evaluation validation winner | 0.992 |
| Ex-post hindsight oracle | 1.022 |

[Investigation 2](discussions/quant_ai/Comparator%20Choice%20and%20Forecast%20Horizon.md)

### Finding 3. LoRA fine-tuning gains are small and uneven

A rank-8 adapter against zero-shot, panel-average loss under isolated inference, each
range across five seeds:

| Horizon | Loss reduction |
|---|---:|
| 1 session | 0.21% to 0.63% |
| 5 sessions | 0.94% to 1.10% |
| 22 sessions | 0.86% to 1.26% |

- The adapter is fitted on 11 futures and scored on 15 different ones.
- **7 to 13 of 15** held-out futures improve, depending on horizon, inference mode and fit.
- Full fine-tuning of every base parameter does not beat the adapter.

[Investigation 3](discussions/quant_ai/Held-Out%20Adaptation.md#a-held-out-futures-lora-test)

### Finding 4. Covariates move the center and collapse the band

Chronos-2 on the nine-sector basket, post-release:

| Forecast | MAE, vol points | q10-q90 coverage |
|---|---:|---:|
| Classical target EWMA | 2.86 | no band |
| Chronos-2, with sector legs and VIX | 2.99 | 22.9% |
| Chronos-2, target history only | 3.31 | 74.3% |

- Nominal coverage is 80%. Covariates improve the median and leave the quantiles unusable as bands.
- The classical arm is a point forecast, which is why it has no coverage to report.

[Investigation 4](discussions/quant_ai/Covariates%20and%20Portfolio%20Volatility.md#basket-volatility-with-covariates)

### Finding 5. Clock and event state narrow the intraday deficit

Chronos-2 q50 MAE as a share of the preselected validation winner's, lower favoring the
model:

| Intraday look | Block | Before | After |
|---|---|---:|---:|
| Futures around a scheduled release | 10 min | 1.424 | 1.186 |
| Equities at the session open | 1 hr | 1.444 | 1.047 |

- Both stay above 1 throughout, so neither look reaches a model win.
- Before and after name a different move in each row: on the futures grid, the blocks before a release against one block after it; on the equity panel, an implicit session clock against an explicit fixed grid.

[Investigation 5](discussions/quant_ai/Clock%20and%20Calendar%20Information.md#information-enters-the-history)

### Where the rest of the record sits

| To read | Start at |
|---|---|
| What the models are, and how one turns a series into a forecast | [Background](discussions/quant_ai/Background.md) |
| The same instruments on another target or cadence, and what might explain the split across markets | [Further Analysis](discussions/quant_ai/Further%20Analysis.md) |
| The targets, frequencies and model families worth trying next | [Ongoing Work](discussions/quant_ai/Ongoing%20Work.md) |
| Selected research and the full paper index | [Research](discussions/quant_ai/Research.md), then the [Research Appendix](discussions/quant_ai/Research%20Appendix.md) |
| The constructions behind the evidence, as runnable notebooks | [Technical Appendix](discussions/quant_ai/Technical%20Appendix.md) |

## Generative Scenario Analysis

:::{div} part-porch
Eight scenario engines on one market object, scored three ways: the tail bands
they imply, the hedge they choose, and the five-day paths they generate.

[Background](discussions/quant_ai/Background%20-%20Scenarios.md) · [Investigations](discussions/quant_ai/Investigations%20-%20Scenarios.md) · [Further Analysis](discussions/quant_ai/Further%20Analysis%20-%20Scenarios.md) · [Research](discussions/quant_ai/The%20Research%20Record.md)
:::

| Investigation | Generated object and loss |
|---|---|
| [1. One-Day Surfaces](discussions/quant_ai/Investigation%201%20-%20One-Day%20Surfaces.md) | Next-day 114-coordinate volatility surface, scored on 95% and 99% tail coverage and on four structural gates |
| [2. Hedging](discussions/quant_ai/Hedging.ipynb) | The same draws, scored on hedging error for a fixed book of options |
| [3. Multi-Day Paths](discussions/quant_ai/Multi-Day%20Paths.ipynb) | Cumulative five-day surface moves, scored on path distribution and coverage |

### Finding 1. Repairing the surface does not move the tail

| Repair check | Result |
|---|---:|
| COVID draws moved | GARCH 38%; VolGAN 82% |
| Calendar and smile-shape pass after projection | 100% for both engines |
| Coverage counts after projection | Unchanged in all five episodes |
| Draws beyond the realized 99th percentile | VAE 0.0%; history 1.0% |

- The VAE has the strongest structural measures in this comparison and smooths out the upper tail.
- No engine clears both the structural gates and the coverage count on the same draws.

[The projection repair](discussions/quant_ai/Investigation%201%20-%20One-Day%20Surfaces.md#the-projection-repair)

### Finding 2. Conditioning leaves 2.2 effective days at COVID

| Conditioning diagnostic | Result |
|---|---:|
| Days matching the state | 42 of 2,741 |
| Effective sample at COVID | 2.2 days |
| Hard matches after removing COVID | 27 days |
| Nearest days to the 2026-03-30 state | 0 of 40 from 2020 |

COVID upper-95% breach days:

| Engine | One day | Five days |
|---|---:|---:|
| Hard replay | 4 of 15 | 5 of 15 |
| Kernel | 7 of 15 | 14 of 15 |
| Iterated VolGAN | 3 of 15 | 7 of 15 |
| Unconditional engines | 4 of 15 | 4 of 15 |

- Independent stress history would overturn this reading. A wider bandwidth changes weights, not analogues.

[How much history the state actually holds](discussions/quant_ai/Investigation%201%20-%20One-Day%20Surfaces.md#how-much-history-the-state-actually-holds)

### Finding 3. Black-76 delta beats every scenario hedge at COVID

Median absolute hedge error, index points:

| Episode | Black-76 delta | Scenario hedge | Days scenario beats delta |
|---|---:|---:|---:|
| COVID | 19 | 21 to 67 | No engine more than 6 of 15 |
| 2022 cycle | 8.4 | Kernel 7.8 | 10 of 17 |

- The comparator is the analytic Black-76 delta read directly from the marks.

[Investigation 2](discussions/quant_ai/Hedging.ipynb)

### Finding 4. Hedged does not mean covered

COVID band results, days of 15:

| Engine or band | Days |
|---|---:|
| GARCH, loss-side breach | 3 |
| Unconditional engines, loss-side breach | 4 to 5 |
| Kernel, loss-side breach | 10 |
| VolGAN, gain-side breach | 11 |
| VolGAN 95th percentile below zero | 14 |

- GARCH's lower breach count comes with the widest bands.
- The hedge residual distribution still needs to be scored as carefully as the hedge ratio.

[Investigation 2](discussions/quant_ai/Hedging.ipynb)

### Finding 5. Independent replay overstates five-day dispersion

| Five-day quantity | Result |
|---|---:|
| Realized variance ratio, ex-COVID | 0.83 |
| Independent-replay variance ratio | 1.02 |
| Stationary-bootstrap variance ratio | 0.90 |
| Lag-1 autocorrelation of daily changes | -0.07 |
| COVID upper-95% breaches, independent replay | 4 of 15 |
| COVID upper-95% breaches, stationary bootstrap | 4 of 15 |

- Independent replay overstates five-day dispersion. The block bootstrap inherits the mean reversion.
- The closer unconditional fit does not resolve the conditional miss.

[Investigation 3](discussions/quant_ai/Multi-Day%20Paths.ipynb)

### Where the rest of the record sits

| To read | Start at |
|---|---|
| What a scenario engine is, what it generates here, and the checks a generated surface has to clear | [Background](discussions/quant_ai/Background%20-%20Scenarios.md) |
| The engine roster behind the investigations, and why the failures happen | [Further Analysis](discussions/quant_ai/Further%20Analysis%20-%20Scenarios.md) |
| The decisions, horizons and frequencies worth testing next | [Ongoing Work](discussions/quant_ai/Ongoing%20Work%20-%20Scenarios.md) |
| Selected research and the full paper index | [Research](discussions/quant_ai/The%20Research%20Record.md), then the [Research Appendix](discussions/quant_ai/Research%20Appendix%20-%20Scenarios.md) |
| The full definitions behind the compact statements the evidence pages carry | [Technical Appendix](discussions/quant_ai/Technical%20Appendix%20-%20Scenarios.md) |

---

*Updated August 2026*

Mark Hendricks

[hendricks@uchicago.edu](mailto:hendricks@uchicago.edu)

---
