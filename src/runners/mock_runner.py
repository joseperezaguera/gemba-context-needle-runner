"""
MockRunner: simula el lost-in-the-middle de forma determinista.

Sin claves API, sin red. Encuentra la clave si está en los extremos del
contexto (primer o último 15%); falla en el medio. Útil para tests, demos
locales y para verificar que la pipeline funciona end-to-end antes de
gastar tokens en modelos reales.
"""
from __future__ import annotations

import re


class MockRunner:
    """Runner determinista que simula la curva en U."""

    name = "mock"
    model = "mock-v1"

    def query(self, context: str, question: str) -> str:
        # Busca la clave alfanumérica de 6 chars en el contexto
        match = re.search(r"\b([A-Z0-9]{6})\b", context)
        if not match:
            return "no encontrada"

        # Simula lost-in-the-middle:
        # - Si la clave está en el 15% inicial o el 15% final → recuerda.
        # - Si está en el medio → falla.
        n = len(context)
        pos = match.start() / n
        if pos < 0.15 or pos > 0.85:
            return match.group(1)
        return "no estoy seguro"
