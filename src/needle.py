"""
Generación e inserción de "agujas" para experimentos needle-in-haystack.

Una aguja es una frase corta con una clave única (6 caracteres alfanuméricos
en mayúscula) que se inserta en mitad de un texto grande para luego
preguntar al modelo si la recuerda.
"""
from __future__ import annotations

import random
import re
import string


def generate_needle(seed: int | None = None) -> str:
    """
    Genera una aguja: una frase con una clave única de 6 caracteres
    alfanuméricos mayúsculas/dígitos.

    Args:
        seed: si se pasa, el resultado es determinista.

    Returns:
        Frase del estilo: " La clave secreta del experimento es ABC123. "
    """
    rng = random.Random(seed)
    key = "".join(rng.choices(string.ascii_uppercase + string.digits, k=6))
    return f" La clave secreta del experimento es {key}. "


def extract_key_from_needle(needle: str) -> str:
    """
    Extrae la clave (6 caracteres alfanuméricos) de una frase tipo needle.

    Raises:
        ValueError: si no se encuentra una clave válida.
    """
    match = re.search(r"\b([A-Z0-9]{6})\b", needle)
    if not match:
        raise ValueError(f"No se encontró clave alfanumérica de 6 chars en: {needle!r}")
    return match.group(1)


def insert_needle(haystack: str, needle: str, pos_ratio: float) -> str:
    """
    Inserta `needle` en `haystack` en la posición relativa pos_ratio ∈ [0, 1].

    pos_ratio=0.0 → al principio.
    pos_ratio=1.0 → al final.
    pos_ratio=0.5 → en el centro.
    """
    if not 0.0 <= pos_ratio <= 1.0:
        raise ValueError(f"pos_ratio debe estar en [0, 1], no {pos_ratio}")
    n = len(haystack)
    insert_at = int(pos_ratio * n)
    return haystack[:insert_at] + needle + haystack[insert_at:]


if __name__ == "__main__":
    n = generate_needle(seed=42)
    key = extract_key_from_needle(n)
    print(f"Aguja: {n!r}")
    print(f"Clave extraída: {key}")
    h = "lorem ipsum " * 50
    out = insert_needle(h, n, pos_ratio=0.5)
    print(f"\nInsertada en el medio (pos=0.5):")
    print(out[:200] + " [...] " + out[-100:])
