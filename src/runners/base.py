"""Protocolo común que todos los runners deben cumplir."""
from __future__ import annotations

from typing import Protocol


class Runner(Protocol):
    """
    Interfaz mínima que debe implementar un runner.

    Un runner toma un contexto largo (el haystack con la aguja insertada)
    y una pregunta, y devuelve la respuesta del modelo. La curva de
    aciertos por posición se mide comparando la respuesta con la clave
    esperada de la aguja.
    """

    name: str
    model: str

    def query(self, context: str, question: str) -> str:
        """Devuelve la respuesta del modelo al contexto + pregunta."""
        ...
