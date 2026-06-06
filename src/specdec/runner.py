"""End-to-end runner: sweep + charts + summary.json."""

from __future__ import annotations

import json
from pathlib import Path

from specdec.bench.sweep import run_sweep
from specdec.viz.charts import (
    acceptance_dist_hist,
    acceptance_vs_k,
    cost_per_token_bar,
    latency_vs_k,
    speedup_heatmap,
)


def run(out_dir: Path, n_tokens: int = 256) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = Path("results/figures")
    rows = run_sweep(n_tokens=n_tokens)

    acceptance_vs_k(rows, figs / "acceptance_vs_k.png")
    latency_vs_k(rows, figs / "latency_vs_k.png")
    cost_per_token_bar(rows, figs / "cost_per_token.png")
    speedup_heatmap(rows, figs / "speedup_heatmap.png")
    acceptance_dist_hist(rows, figs / "acceptance_dist.png")

    baseline = next((r for r in rows if r.K == 0), None)
    best_speedup = None
    best_cost = None
    if baseline:
        speedups = [(r, baseline.elapsed_ms / max(1.0, r.elapsed_ms)) for r in rows if r.K > 0]
        if speedups:
            best_speedup = max(speedups, key=lambda kv: kv[1])
            best_cost = min(rows, key=lambda r: r.cost_usd / max(1, r.n_tokens))

    summary: dict[str, object] = {
        "n_runs": len(rows),
        "baseline_ms": baseline.elapsed_ms if baseline else None,
        "best_speedup": {
            "draft": best_speedup[0].draft,
            "K": best_speedup[0].K,
            "speedup_x": best_speedup[1],
        }
        if best_speedup
        else None,
        "best_cost_per_token_usd": best_cost.cost_usd / max(1, best_cost.n_tokens)
        if best_cost
        else None,
        "results": [r.model_dump() for r in rows],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    return summary
