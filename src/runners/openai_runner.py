"""OpenAI runner. Requiere OPENAI_API_KEY y el paquete `openai`."""
from __future__ import annotations

import os


class OpenAIRunner:
    """Runner que llama a la API de OpenAI."""

    name = "openai"

    def __init__(self, model: str = "gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "OpenAIRunner requiere `pip install openai`. "
                "Alternativamente, usa MockRunner para tests sin claves."
            ) from e
        if "OPENAI_API_KEY" not in os.environ:
            raise RuntimeError(
                "Falta la variable de entorno OPENAI_API_KEY."
            )
        self.model = model
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def query(self, context: str, question: str) -> str:
        msg = (
            f"Contexto:\n{context}\n\n"
            f"Pregunta: {question}\n"
            f"Responde solo con la clave alfanumérica de 6 caracteres, sin más texto."
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": msg}],
            temperature=0.0,
            max_tokens=30,
        )
        return resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
