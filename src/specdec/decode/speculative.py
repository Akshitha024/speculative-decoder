"""Core speculative-decoding loop.

The contract we model:

  1. The draft model proposes K tokens.
  2. The target model is invoked once on the prefix + K draft tokens; this
     produces K + 1 target tokens (one per position, the last being the
     "correction" for whichever draft was rejected).
  3. We accept the longest prefix of draft tokens that agree with the target.
  4. If all K draft tokens are accepted, we keep them and the (K+1)-th
     target token as the bonus.
  5. If a draft token is rejected at position j, we keep the first j tokens
     plus the target's correction at position j+1, then restart.

The simulation is governed by `agreement_with_target`: at each draft position
we accept with that probability (Bernoulli). This is the standard speculative-
decoding lower-bound model and matches the Leviathan/Chen formulation.
"""

from __future__ import annotations

import random

from specdec.types import DecodeResult, ModelProfile


def speculative_decode(
    target: ModelProfile,
    draft: ModelProfile,
    n_tokens: int,
    K: int,
    prompt_tokens: int = 256,
    seed: int = 17,
) -> DecodeResult:
    rng = random.Random(seed)
    if K <= 0:
        return _baseline(target, n_tokens, prompt_tokens)
    produced = 0
    accepted = 0
    rejected = 0
    target_calls = 0
    draft_calls = 0
    elapsed = 0.0
    cost = 0.0
    while produced < n_tokens:
        draft_calls += 1
        elapsed += draft.decode_ms * K
        cost += K * draft.usd_per_token_out
        target_calls += 1
        elapsed += target.decode_ms
        cost += (K + 1) * target.usd_per_token_out + prompt_tokens * target.usd_per_token_in
        n_accept = 0
        for _ in range(K):
            if rng.random() < draft.agreement_with_target:
                n_accept += 1
            else:
                break
        accepted += n_accept
        rejected += K - n_accept
        produced += n_accept + 1
        if produced > n_tokens:
            produced = n_tokens
    return DecodeResult(
        target=target.name,
        draft=draft.name,
        K=K,
        n_tokens=n_tokens,
        n_accepted_draft=accepted,
        n_rejected_draft=rejected,
        total_target_calls=target_calls,
        total_draft_calls=draft_calls,
        elapsed_ms=elapsed,
        cost_usd=cost,
        acceptance_rate=accepted / max(1, accepted + rejected),
    )


def _baseline(target: ModelProfile, n_tokens: int, prompt_tokens: int) -> DecodeResult:
    """K=0: just call target n_tokens times."""
    cost = n_tokens * target.usd_per_token_out + prompt_tokens * target.usd_per_token_in
    return DecodeResult(
        target=target.name,
        draft=None,
        K=0,
        n_tokens=n_tokens,
        n_accepted_draft=0,
        n_rejected_draft=0,
        total_target_calls=n_tokens,
        total_draft_calls=0,
        elapsed_ms=target.decode_ms * n_tokens,
        cost_usd=cost,
        acceptance_rate=0.0,
    )
