"""
Construcción de "heno" (haystack) para experimentos needle-in-haystack.

El heno es un texto largo y diverso en el que se inserta la aguja. Usar
texto repetitivo (el mismo párrafo N veces) genera artefactos en la
tokenización y el modelo lo nota. Aquí intercalamos tres temas distintos
(ML, biología y historia) para que el contexto sea variado.
"""
from __future__ import annotations

_BASE_PARAGRAPHS = [
    # ML / Transformers
    "Las arquitecturas de transformers han transformado el procesamiento "
    "del lenguaje natural. Los modelos preentrenados como BERT, GPT y T5 "
    "dominan los benchmarks. La atención escalar producto, propuesta en "
    "el artículo Attention is All You Need de 2017, es la operación "
    "fundamental sobre la que se construyen estos sistemas. ",
    # Biología
    "La fotosíntesis es el proceso por el cual las plantas convierten "
    "energía lumínica en energía química, almacenada en moléculas de "
    "glucosa. Ocurre principalmente en los cloroplastos, en presencia de "
    "clorofila. El oxígeno se libera como subproducto del proceso. ",
    # Historia
    "El Renacimiento fue un movimiento cultural surgido en Italia en el "
    "siglo XIV, caracterizado por un renovado interés en la antigüedad "
    "clásica. Figuras como Leonardo da Vinci, Miguel Ángel y Rafael "
    "definieron el arte de la época y elevaron la categoría del artista. ",
]


def build_haystack(target_chars: int) -> str:
    """
    Construye un texto largo de al menos `target_chars` caracteres,
    intercalando varios párrafos base para evitar artefactos de
    tokenización por repetición exacta.
    """
    out: list[str] = []
    total = 0
    i = 0
    while total < target_chars:
        para = _BASE_PARAGRAPHS[i % len(_BASE_PARAGRAPHS)]
        out.append(para)
        total += len(para)
        i += 1
    return "".join(out)


def estimate_tokens(text: str) -> int:
    """
    Estimación grosera del número de tokens. Asume ~4 caracteres por token
    para español/inglés (es una aproximación de andar por casa que no
    sustituye al tokenizador real del modelo).
    """
    return max(1, len(text) // 4)


if __name__ == "__main__":
    h = build_haystack(target_chars=5000)
    print(f"Heno generado: {len(h)} chars, ~{estimate_tokens(h)} tokens estimados.")
    print(f"Primeros 300 chars:\n{h[:300]}...")
