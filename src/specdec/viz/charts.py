"""Five chart families for the speculative-decoder benchmark."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from specdec.types import DecodeResult


def _save(fig: Figure, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def acceptance_vs_k(rows: list[DecodeResult], out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    drafts = sorted({r.draft for r in rows if r.draft is not None and r.K > 0})
    for d in drafts:
        ks = sorted({r.K for r in rows if r.draft == d and r.K > 0})
        ys = [next(r.acceptance_rate for r in rows if r.draft == d and k == r.K) for k in ks]
        ax.plot(ks, ys, marker="o", label=str(d))
    ax.set_xlabel("K (draft length)")
    ax.set_ylabel("acceptance rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("Acceptance rate vs K")
    ax.legend()
    ax.grid(alpha=0.3)
    return _save(fig, out)


def latency_vs_k(rows: list[DecodeResult], out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    drafts = sorted({r.draft for r in rows if r.draft is not None})
    baseline = next((r.elapsed_ms for r in rows if r.K == 0), 0.0)
    ax.axhline(baseline, color="black", linestyle="--", label="baseline (K=0)")
    for d in drafts:
        ks = sorted({r.K for r in rows if r.draft == d and r.K > 0})
        ys = [next(r.elapsed_ms for r in rows if r.draft == d and k == r.K) for k in ks]
        ax.plot(ks, ys, marker="s", label=str(d))
    ax.set_xlabel("K")
    ax.set_ylabel("elapsed (ms)")
    ax.set_title("Latency vs K")
    ax.legend()
    ax.grid(alpha=0.3)
    return _save(fig, out)


def cost_per_token_bar(rows: list[DecodeResult], out: Path) -> Path:
    labels = [f"{r.draft or 'none'}/K={r.K}" for r in rows]
    cpt = [r.cost_usd / max(1, r.n_tokens) * 1e6 for r in rows]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors = ["#7a7a7a" if r.K == 0 else "#3b6fa1" for r in rows]
    x = np.arange(len(labels))
    ax.bar(x, cpt, color=colors)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("USD / token (x 1e6)")
    ax.set_title("Cost per generated token")
    return _save(fig, out)


def speedup_heatmap(rows: list[DecodeResult], out: Path) -> Path:
    drafts = sorted({r.draft for r in rows if r.draft is not None and r.K > 0})
    ks = sorted({r.K for r in rows if r.K > 0})
    baseline = next((r.elapsed_ms for r in rows if r.K == 0), 1.0)
    mat = np.zeros((len(drafts), len(ks)))
    for i, d in enumerate(drafts):
        for j, k in enumerate(ks):
            row = next((r for r in rows if r.draft == d and k == r.K), None)
            if row:
                mat[i, j] = baseline / max(1, row.elapsed_ms)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    im = ax.imshow(mat, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(ks)))
    ax.set_xticklabels([f"K={k}" for k in ks])
    ax.set_yticks(range(len(drafts)))
    ax.set_yticklabels([str(d) for d in drafts])
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:.2f}x", ha="center", va="center", color="w", fontsize=9)
    ax.set_title("Latency speedup over baseline")
    fig.colorbar(im, ax=ax, label="speedup (x)")
    return _save(fig, out)


def acceptance_dist_hist(rows: list[DecodeResult], out: Path) -> Path:
    vals = [r.acceptance_rate for r in rows if r.K > 0]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(vals, bins=20, color="#5b8d4a", edgecolor="white")
    ax.set_xlabel("acceptance rate")
    ax.set_ylabel("configurations")
    ax.set_title("Acceptance-rate distribution across (draft, K)")
    return _save(fig, out)
