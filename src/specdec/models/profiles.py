"""Canonical model profiles.

Prices and decode-latency numbers are illustrative but calibrated to public
pricing tiers: a frontier target model (Claude 3.5 Sonnet class) and three
candidate draft models (Haiku, a 1B-parameter local model, and a 4B local
model). The `agreement_with_target` field controls how often the draft model
emits the same token the target would have emitted; in real systems this is
measured from logits, here it is a tunable hyperparameter.
"""

from __future__ import annotations

from specdec.types import ModelProfile


def target_frontier() -> ModelProfile:
    """The model whose answer we want to match."""
    return ModelProfile(
        name="frontier-target",
        usd_per_token_in=3e-6,
        usd_per_token_out=15e-6,
        decode_ms=40.0,
        agreement_with_target=1.0,
    )


def draft_tiny() -> ModelProfile:
    """A very small, very cheap draft."""
    return ModelProfile(
        name="draft-1B",
        usd_per_token_in=0.25e-6,
        usd_per_token_out=1.25e-6,
        decode_ms=4.0,
        agreement_with_target=0.55,
    )


def draft_small() -> ModelProfile:
    """A 4B-class local draft with stronger agreement."""
    return ModelProfile(
        name="draft-4B",
        usd_per_token_in=0.40e-6,
        usd_per_token_out=2.00e-6,
        decode_ms=8.0,
        agreement_with_target=0.72,
    )


def draft_strong() -> ModelProfile:
    """A Haiku-class hosted draft with the highest agreement."""
    return ModelProfile(
        name="draft-haiku",
        usd_per_token_in=0.80e-6,
        usd_per_token_out=4.00e-6,
        decode_ms=10.0,
        agreement_with_target=0.84,
    )


def all_drafts() -> list[ModelProfile]:
    return [draft_tiny(), draft_small(), draft_strong()]
