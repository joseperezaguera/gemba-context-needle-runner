"""Anthropic runner. Requiere ANTHROPIC_API_KEY y el paquete `anthropic`."""
from __future__ import annotations

import os


class AnthropicRunner:
    """Runner que llama a la API de Anthropic."""

    name = "anthropic"

    def __init__(self, model: str = "claude-sonnet-4-6"):
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise ImportError(
                "AnthropicRunner requiere `pip install anthropic`. "
                "Alternativamente, usa MockRunner para tests sin claves."
            ) from e
        if "ANTHROPIC_API_KEY" not in os.environ:
            raise RuntimeError(
                "Falta la variable de entorno ANTHROPIC_API_KEY."
            )
        self.model = model
        self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def query(self, context: str, question: str) -> str:
        msg = (
            f"Contexto:\n{context}\n\n"
            f"Pregunta: {question}\n"
            f"Responde solo con la clave alfanumérica de 6 caracteres, sin más texto."
        )
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=30,
            messages=[{"role": "user", "content": msg}],
        )
        # resp.content[0].text en la API actual
        if resp.content and hasattr(resp.content[0], "text"):
            return resp.content[0].text.strip()
        return ""
