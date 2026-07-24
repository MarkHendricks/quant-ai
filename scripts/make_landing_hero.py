#!/usr/bin/env python3
"""Illustrative landing-page hero: one realized path, many generated futures.

Pure illustration (simulated, no data, no axis numbers): the generative-
scenario idea in one panel. Writes docs/_static/landing_hero.png.
Run: ~/Projects/ai-models/.venv-occ-poc/bin/python scripts/make_landing_hero.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

rng = np.random.default_rng(90210)

n_hist, n_fut, n_paths = 150, 90, 35
kappa, mu, sig = 0.06, 0.22, 0.021

# realized history: mean-reverting vol-like path with one stress spike
h = np.empty(n_hist)
h[0] = 0.21
for t in range(1, n_hist):
    jump = 0.10 if t == 95 else 0.0
    h[t] = h[t-1] + kappa * (mu - h[t-1]) + sig * rng.standard_normal() + jump
h = np.convolve(h, np.ones(3) / 3, mode="same")
h[-1] = h[-2]  # smooth endpoint

# generated futures: same dynamics sampled forward from the endpoint
fut = np.empty((n_paths, n_fut + 1))
fut[:, 0] = h[-1]
for t in range(1, n_fut + 1):
    fut[:, t] = (fut[:, t-1] + kappa * (mu - fut[:, t-1])
                 + sig * rng.standard_normal(n_paths))
smooth = np.ones(5) / 5
fut = np.apply_along_axis(lambda r: np.convolve(r, smooth, mode="same"), 1, fut)
fut[:, 0] = h[-1]
fut[:, -1] = fut[:, -2]

xh = np.arange(n_hist)
xf = np.arange(n_hist - 1, n_hist + n_fut)

fig, ax = plt.subplots(figsize=(8.2, 4.3))
for i in range(n_paths):
    ax.plot(xf, fut[i], color="#6b93c9", lw=1.1, alpha=0.22, zorder=2)
for i in rng.choice(n_paths, 2, replace=False):
    ax.plot(xf, fut[i], color="#5b84b8", lw=1.6, alpha=0.8, zorder=3)
ax.plot(xh, h, color="#1f4e79", lw=3.0, zorder=4, solid_capstyle="round")
ax.axvline(n_hist - 1, color="#8a97a8", lw=1.0, ls=(0, (4, 4)), alpha=0.6, zorder=1)

ax.set_xlim(0, n_hist + n_fut - 2)
lo = min(h.min(), fut.min()) - 0.02
hi = max(h.max(), fut.max()) + 0.02
ax.set_ylim(lo, hi)
ax.axis("off")
fig.tight_layout(pad=0.4)
out = Path(__file__).resolve().parents[1] / "docs" / "_static" / "landing_hero.png"
fig.savefig(out, dpi=160, facecolor="white")
print("wrote", out)
