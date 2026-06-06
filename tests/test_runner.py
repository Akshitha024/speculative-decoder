"""End-to-end runner smoke test."""

from __future__ import annotations

from pathlib import Path

from specdec.runner import run


def test_runner_writes_summary(tmp_path: Path) -> None:
    s = run(tmp_path / "out", n_tokens=128)
    assert s["n_runs"] >= 13  # 1 baseline + 3 drafts x 4 K values
    assert (tmp_path / "out" / "summary.json").exists()
    assert s["baseline_ms"] is not None
    assert s["best_speedup"] is not None
