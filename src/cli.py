"""CLI de gemba-needle: lanza el experimento needle-in-haystack."""
from __future__ import annotations

import sys
from pathlib import Path

# Hack para imports relativos cuando se ejecuta como módulo
sys.path.insert(0, str(Path(__file__).parent))

import click

from curve import run_curve
from visualize import plot_recall_curve


def _build_runner(runner_name: str, model: str | None):
    """Construye el runner adecuado o aborta con mensaje claro."""
    if runner_name == "mock":
        from runners.mock_runner import MockRunner
        return MockRunner()
    elif runner_name == "openai":
        try:
            from runners.openai_runner import OpenAIRunner
        except ImportError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        return OpenAIRunner(model=model or "gpt-4o-mini")
    elif runner_name == "anthropic":
        try:
            from runners.anthropic_runner import AnthropicRunner
        except ImportError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        return AnthropicRunner(model=model or "claude-sonnet-4-6")
    else:
        click.echo(f"Runner desconocido: {runner_name}", err=True)
        sys.exit(1)


@click.command(help="Mide la curva de recall por posición de un LLM (needle-in-haystack).")
@click.option(
    "--runner",
    type=click.Choice(["mock", "openai", "anthropic"], case_sensitive=False),
    default="mock",
    show_default=True,
    help="Proveedor del modelo.",
)
@click.option(
    "--model",
    default=None,
    help="Modelo concreto. Si no se pasa, usa el por defecto del runner.",
)
@click.option(
    "--context-chars",
    type=int,
    default=20000,
    show_default=True,
    help="Tamaño del heno en caracteres.",
)
@click.option(
    "--positions",
    default="0.05,0.25,0.5,0.75,0.95",
    show_default=True,
    help="Lista de posiciones relativas separadas por comas.",
)
@click.option(
    "--n-trials",
    type=int,
    default=3,
    show_default=True,
    help="Trials por posición.",
)
@click.option(
    "--seed",
    type=int,
    default=0,
    show_default=True,
    help="Seed base para reproducibilidad.",
)
@click.option(
    "--output",
    type=click.Path(),
    default="output/recall_curve.png",
    show_default=True,
    help="Path donde guardar el PNG con la curva.",
)
def main(runner, model, context_chars, positions, n_trials, seed, output):
    """Lanza el experimento needle-in-haystack y dibuja la curva."""
    positions_list = [float(p.strip()) for p in positions.split(",")]
    r = _build_runner(runner, model)

    click.echo(f"Runner: {r.name} ({r.model})")
    click.echo(f"Heno: {context_chars} chars · posiciones: {positions_list} · trials: {n_trials}")
    click.echo("Ejecutando...")

    results = run_curve(
        runner=r,
        haystack_chars=context_chars,
        positions=positions_list,
        n_trials=n_trials,
        seed=seed,
    )

    click.echo("\nResultados:")
    click.echo(f"{'pos':>6} | {'recall':>8}")
    click.echo("-" * 20)
    for pos in sorted(results.keys()):
        click.echo(f"{pos:>6.2f} | {results[pos]:>7.2%}")

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plot_recall_curve(
        results,
        title=f"Recall por posición — {r.name}/{r.model}",
        savepath=str(output_path),
    )
    click.echo(f"\nGráfico: {output_path}")


if __name__ == "__main__":
    main()
