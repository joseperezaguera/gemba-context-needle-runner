# gemba-context-needle-runner

> **Mide el lost-in-the-middle en tu propio uso de LLMs.** Material complementario del artículo de [Gemba](https://www.gemba.es/) [«¿Por qué los LLMs olvidan?»](https://www.gemba.es/) (25 de mayo de 2026).

Lanza el experimento de "aguja en el pajar" contra OpenAI, Anthropic o modelos abiertos vía HuggingFace, varía el tamaño del contexto y la posición de la aguja, y te devuelve la curva de aciertos por posición. Para que dejes de adivinar dónde colapsa tu modelo y empieces a medirlo.

## Por qué

El paper de Liu et al. 2024 (*Lost in the Middle*) midió el fenómeno en diez modelos. Pero tu caso de uso —tu modelo, tu idioma, tu tipo de pregunta, tu tamaño de contexto típico— tiene una curva propia. Esta herramienta te la mide en tres comandos.

## Empezar en 60 segundos

```bash
git clone https://github.com/joseperezaguera/gemba-context-needle-runner.git
cd gemba-context-needle-runner
pip install -r requirements.txt           # MockRunner (sin claves)
python -m src.cli --runner mock
```

Esto corre needle-in-haystack contra un runner mock determinista (que simula lost-in-the-middle) y dibuja la curva. Para correr contra modelos reales:

```bash
pip install openai anthropic              # solo lo que vayas a usar
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
python -m src.cli --runner openai --model gpt-4o-mini
python -m src.cli --runner anthropic --model claude-sonnet-4-6
```

## Para entender vs para decidir

- Este repo: **para decidir** midiendo el efecto en tu modelo y tu caso de uso.
- [`gemba-attention-from-scratch`](https://github.com/joseperezaguera/gemba-attention-from-scratch): **para entender** la mecánica de la atención desde dentro.

## Tests

```bash
python3 -m unittest discover tests
```

Los tests usan un `MockRunner` determinista — no requieren claves API.

## Licencia

MIT.
