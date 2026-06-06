"""Tests for model-profile sanity."""

from __future__ import annotations

from specdec.models.profiles import all_drafts, draft_strong, draft_tiny, target_frontier


def test_target_more_expensive_than_drafts() -> None:
    t = target_frontier()
    for d in all_drafts():
        assert t.usd_per_token_out > d.usd_per_token_out


def test_drafts_strictly_ordered_by_agreement() -> None:
    weak = draft_tiny().agreement_with_target
    strong = draft_strong().agreement_with_target
    assert weak < strong


def test_drafts_strictly_ordered_by_latency() -> None:
    weak = draft_tiny().decode_ms
    strong = draft_strong().decode_ms
    assert weak < strong
