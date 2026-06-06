"""Typer CLI for speculative-decoder."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from specdec.runner import run

app = typer.Typer(no_args_is_help=True, help="Speculative decoding sweep + charts.")
console = Console()


@app.command()
def bench(
    out_dir: Path = typer.Option(Path("runs/latest")),
    n_tokens: int = typer.Option(256),
) -> None:
    """Run the (draft, K) sweep against the target."""
    result = run(out_dir, n_tokens=n_tokens)
    console.print_json(json.dumps({k: v for k, v in result.items() if k != "results"}, default=str))


@app.command()
def report(out_dir: Path = typer.Option(Path("runs/latest"))) -> None:
    """Pretty-print per-(draft, K) results."""
    data = json.loads((out_dir / "summary.json").read_text())
    table = Table(title="Speculative decoding results")
    for col in ("draft", "K", "elapsed_ms", "cost_usd", "acceptance_rate"):
        table.add_column(col)
    for r in data["results"]:
        table.add_row(
            str(r.get("draft") or "-"),
            str(r["K"]),
            f"{r['elapsed_ms']:.1f}",
            f"${r['cost_usd']:.6f}",
            f"{r['acceptance_rate']:.2f}",
        )
    console.print(table)


if __name__ == "__main__":
    app()
