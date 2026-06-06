"""Types for the speculative-decoder harness."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ModelProfile(BaseModel):
    """Per-token cost (USD) and per-token latency (ms) for one model."""

    name: str
    usd_per_token_in: float = Field(..., ge=0)
    usd_per_token_out: float = Field(..., ge=0)
    decode_ms: float = Field(..., ge=0)
    agreement_with_target: float = Field(default=1.0, ge=0, le=1.0)


class DecodeResult(BaseModel):
    """Outcome of running one (target, draft, K) configuration on one prompt."""

    target: str
    draft: str | None
    K: int
    n_tokens: int
    n_accepted_draft: int
    n_rejected_draft: int
    total_target_calls: int
    total_draft_calls: int
    elapsed_ms: float
    cost_usd: float
    acceptance_rate: float
