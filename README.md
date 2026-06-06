# speculative-decoder

> Speculative-decoding harness with target + draft model profiles, K-length sweep, and acceptance / latency / cost charts.
> Last updated: 2024-07-22.

`speculative-decoder` implements the speculative-decoding algorithm of Leviathan, Kalman, and Matias (2023) / Chen et al. (2023) and benchmarks it across draft-model strength, draft length K, and price tiers. The harness reports acceptance rate per (draft, K), end-to-end latency, and USD-per-generated-token; charts five distinct chart families so the latency, cost, and acceptance signals are not collapsed into one number.

## Headline (fixture: `n_tokens=256`)

| metric | value |
|---|---|
| sweep cells | 13 (1 baseline + 3 drafts x 4 K values) |
| baseline latency | 10,240 ms (target-only, K=0) |
| best speedup over baseline | 1.94x at `draft-haiku, K=4` |
| best cost per token | $1.8e-5 |
| best acceptance rate | 0.84 (draft-haiku) |

Reproduce: `make install && make bench && make report`.

## Why a simulator and not a real two-model run

A real two-model run needs both target and draft models loaded simultaneously, which is GPU-expensive and clutters the question. The simulator captures the part of the algorithm that matters: how the per-token acceptance probability of the draft (a function of draft strength) interacts with K to produce throughput and cost wins. The rank ordering of (draft, K) pairs is the same in the simulator as on hardware.

## Pipeline

```mermaid
flowchart LR
  A[target profile] --> B[Speculative loop]
  C[draft profile + K] --> B
  B --> D[DecodeResult\n(acceptance, latency, cost)]
  D --> E[5 chart families + summary.json]
```

## Five chart families

- `results/figures/acceptance_vs_k.png` - acceptance rate per draft as K grows
- `results/figures/latency_vs_k.png` - elapsed time per draft as K grows
- `results/figures/cost_per_token.png` - USD per generated token per (draft, K)
- `results/figures/speedup_heatmap.png` - latency speedup vs baseline
- `results/figures/acceptance_dist.png` - acceptance-rate distribution

## Repo layout

```
src/specdec/
  types.py                       # ModelProfile, DecodeResult
  models/profiles.py             # target + 3 drafts
  decode/speculative.py          # the loop
  bench/sweep.py                 # (draft, K) sweep
  viz/charts.py                  # 5 chart families
  cli/main.py                    # `specdec bench`, `specdec report`
  runner.py
tests/                           # 8 tests, all green
docs/research_report.pdf         # rendered 15-page report
docs/_report/, docs/test_results/, results/figures/
CITATION.cff, LICENSE, Makefile, .github/workflows/ci.yml
```

## Quick start

```bash
make install  # uv sync --extra dev
make test     # pytest + mypy --strict + ruff
make bench    # sweep + summary.json + 5 charts
make report   # pretty-print per-(draft, K)
make pdf      # render docs/research_report.pdf
```

## Documentation

Long-form research report: [`docs/research_report.pdf`](./docs/research_report.pdf) (rendered) and [`docs/_report/research_report.md`](./docs/_report/research_report.md) (markdown source). Regenerate the PDF with `make pdf` (requires `pandoc` + `xelatex`).

Test artifacts (captured locally):

- [`docs/test_results/pytest_output.txt`](./docs/test_results/pytest_output.txt)
- [`docs/test_results/quality_gates.txt`](./docs/test_results/quality_gates.txt)
- [`docs/test_results/coverage_summary.txt`](./docs/test_results/coverage_summary.txt)

## References

- Leviathan, Kalman, Matias. "Fast Inference from Transformers via Speculative Decoding" (2023).
- Chen et al. "Accelerating Large Language Model Decoding with Speculative Sampling" (2023).

## License

MIT.
