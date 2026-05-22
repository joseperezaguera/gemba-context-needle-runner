"""
Visualización de la curva de recall por posición.

Toma un dict {posición: recall} y dibuja un gráfico con matplotlib.
La forma esperada para LLMs con lost-in-the-middle es una U: recall alto
en los extremos, bajo en el medio.
"""
from __future__ import annotations


def plot_recall_curve(
    results: dict[float, float],
    title: str = "Recall por posición",
    savepath: str | None = None,
):
    """
    Dibuja la curva de recall por posición.

    Args:
        results: dict {posición ∈ [0,1]: recall ∈ [0,1]}.
        title: título del gráfico.
        savepath: si se pasa, guarda PNG; si no, intenta plt.show().

    Returns:
        La figura de matplotlib.
    """
    import matplotlib.pyplot as plt

    positions = sorted(results.keys())
    recalls = [results[p] for p in positions]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(positions, recalls, marker="o", linewidth=2, color="#16213e")
    ax.fill_between(positions, recalls, alpha=0.1, color="#16213e")
    ax.set_xlabel("Posición de la aguja en el contexto (0=inicio, 1=final)")
    ax.set_ylabel("Recall (proporción de aciertos)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-0.02, 1.02)
    ax.grid(True, alpha=0.3)
    ax.set_title(title)
    # Líneas guía
    ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.axhline(y=0.0, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, dpi=150)
    return fig


if __name__ == "__main__":
    # Smoke test con datos sintéticos en forma de U
    fake_results = {
        0.05: 0.95,
        0.20: 0.70,
        0.35: 0.45,
        0.50: 0.30,
        0.65: 0.45,
        0.80: 0.70,
        0.95: 0.95,
    }
    import tempfile
    out = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    plot_recall_curve(fake_results, title="Curva en U sintética (demo)", savepath=out)
    print(f"Curva guardada en: {out}")
