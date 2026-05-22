"""
Orquestador del experimento needle-in-haystack.

Para cada posición de la lista, ejecuta n_trials needles distintas con
seeds derivadas y mide cuántas veces el modelo recupera la clave. Devuelve
un dict {posición: recall ∈ [0, 1]}.
"""
from __future__ import annotations

from haystack import build_haystack
from needle import extract_key_from_needle, generate_needle, insert_needle


def run_curve(
    runner,
    haystack_chars: int,
    positions: list[float],
    n_trials: int = 3,
    seed: int = 0,
) -> dict[float, float]:
    """
    Lanza n_trials por posición, devuelve recall (proporción de aciertos).

    Args:
        runner: cualquier objeto con .query(context, question) -> str.
        haystack_chars: tamaño del heno en caracteres.
        positions: lista de posiciones relativas (cada una ∈ [0, 1]).
        n_trials: trials por posición.
        seed: seed base; cada trial deriva su propia seed.

    Returns:
        {posición: recall} donde recall = aciertos / n_trials.
    """
    results: dict[float, float] = {}
    for pos in positions:
        hits = 0
        for trial in range(n_trials):
            needle = generate_needle(seed=seed + trial)
            key = extract_key_from_needle(needle)
            haystack = build_haystack(haystack_chars)
            context = insert_needle(haystack, needle, pos_ratio=pos)
            answer = runner.query(context, "¿Cuál es la clave secreta del experimento?")
            # Recall = 1 si la clave aparece literalmente en la respuesta
            if key in answer:
                hits += 1
        results[pos] = hits / n_trials
    return results


if __name__ == "__main__":
    from runners.mock_runner import MockRunner

    runner = MockRunner()
    results = run_curve(
        runner=runner,
        haystack_chars=3000,
        positions=[0.05, 0.25, 0.5, 0.75, 0.95],
        n_trials=5,
        seed=42,
    )
    print(f"Runner: {runner.name} ({runner.model})")
    print(f"Recall por posición:")
    for pos, recall in sorted(results.items()):
        print(f"  pos={pos:.2f} → recall={recall:.2%}")
