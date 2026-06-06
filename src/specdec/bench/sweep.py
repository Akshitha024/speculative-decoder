"""Sweep over (draft, K) and aggregate."""

from __future__ import annotations

from specdec.decode.speculative import speculative_decode
from specdec.models.profiles import all_drafts, target_frontier
from specdec.types import DecodeResult


def run_sweep(n_tokens: int = 256, ks: tuple[int, ...] = (1, 2, 4, 8)) -> list[DecodeResult]:
    target = target_frontier()
    results: list[DecodeResult] = []
    # baseline (no draft)
    results.append(speculative_decode(target, all_drafts()[0], n_tokens=n_tokens, K=0))
    for draft in all_drafts():
        for k in ks:
            results.append(speculative_decode(target, draft, n_tokens=n_tokens, K=k))
    return results
