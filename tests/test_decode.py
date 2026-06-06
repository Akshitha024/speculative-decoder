"""Tests for the speculative-decoding loop."""

from __future__ import annotations

from specdec.decode.speculative import speculative_decode
from specdec.models.profiles import draft_strong, draft_tiny, target_frontier


def test_baseline_k0_makes_n_target_calls() -> None:
    t = target_frontier()
    r = speculative_decode(t, draft_tiny(), n_tokens=50, K=0)
    assert r.total_target_calls == 50
    assert r.total_draft_calls == 0
    assert r.acceptance_rate == 0.0


def test_speculative_makes_fewer_target_calls() -> None:
    t = target_frontier()
    d = draft_strong()
    base = speculative_decode(t, d, n_tokens=200, K=0)
    spec = speculative_decode(t, d, n_tokens=200, K=4)
    assert spec.total_target_calls < base.total_target_calls


def test_acceptance_rate_increases_with_agreement() -> None:
    t = target_frontier()
    weak = speculative_decode(t, draft_tiny(), n_tokens=400, K=4, seed=1)
    strong = speculative_decode(t, draft_strong(), n_tokens=400, K=4, seed=1)
    assert strong.acceptance_rate > weak.acceptance_rate


def test_produces_at_least_n_tokens() -> None:
    t = target_frontier()
    r = speculative_decode(t, draft_strong(), n_tokens=128, K=3)
    assert r.n_tokens == 128
