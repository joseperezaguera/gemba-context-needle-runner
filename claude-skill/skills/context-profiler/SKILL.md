---
name: context-profiler
description: >
  Cuándo y cómo usar gemba-context-needle-runner para medir el
  lost-in-the-middle en LLMs reales. Lanza un experimento
  needle-in-haystack contra el modelo del usuario, varía la posición
  de la aguja y devuelve la curva de recall.

  Triggers: "mide el lost-in-the-middle en GPT-4o", "¿qué porcentaje
  de mi contexto importa de verdad?", "compara recall por posición
  entre Claude y OpenAI", "¿en qué tamaño de contexto colapsa mi
  modelo?", "needle in a haystack en mi modelo".
version: 0.1.0
---

# Skill: context-profiler

## Cuándo invocar esta skill

Cuando el usuario quiera **medir empíricamente** el efecto *lost-in-the-middle* en un LLM concreto. Esta skill no explica la teoría (eso lo hace el artículo de Gemba y `gemba-attention-from-scratch`); aquí se trata de **medir en su propio modelo**.

Casos típicos:

- *"¿Cuánto se olvida GPT-4o-mini con 30k tokens de contexto?"*
- *"Necesito decidir si meter todo el manual en el prompt o trocearlo: ¿hasta dónde puedo estirar antes de que colapse?"*
- *"Compara Claude Sonnet y GPT-4o en recall por posición."*
- *"Estoy considerando reducir el system prompt a la mitad. ¿Cuánto recall gano?"*

Si el usuario pregunta por la **teoría** (qué es la atención, por qué los LLMs olvidan), redirígele al repo hermano `gemba-attention-from-scratch` y al artículo de Gemba.

## Quick start

El CLI vive en `src/cli.py` y se ejecuta como módulo:

```bash
# Sin claves, sin coste — recomendado para empezar
python -m src.cli --runner mock

# OpenAI (necesita OPENAI_API_KEY)
python -m src.cli --runner openai --model gpt-4o-mini

# Anthropic (necesita ANTHROPIC_API_KEY)
python -m src.cli --runner anthropic --model claude-sonnet-4-6
```

Flags clave (verificados contra `src/cli.py`):

| Flag | Default | Para qué |
|------|---------|----------|
| `--runner` | `mock` | `mock`, `openai` o `anthropic` |
| `--model` | (por runner) | Modelo concreto del proveedor |
| `--context-chars` | `20000` | Tamaño del heno en caracteres |
| `--positions` | `0.05,0.25,0.5,0.75,0.95` | Posiciones relativas de la aguja |
| `--n-trials` | `3` | Trials por posición (más = menos varianza) |
| `--seed` | `0` | Reproducibilidad |
| `--output` | `output/recall_curve.png` | Path del PNG |

## Interpretación de resultados

El CLI imprime una tabla y guarda un PNG con la curva de recall por posición.

- **Recall = 1.0** en todas las posiciones → el modelo no sufre lost-in-the-middle en ese tamaño de contexto. Puedes seguir estirando.
- **Curva en U** (extremos altos, medio bajo) → patrón clásico de *Liu et al. 2024*. Cuanto más profunda la U, más severo el efecto.
- **Curva descendente** (alta al inicio, baja al final) → efecto "recency-only": el modelo solo se acuerda del final.
- **Curva plana baja** → el modelo no localiza la aguja ni siquiera en los bordes; revisa el tamaño de contexto (puede estar saturado) o el prompt.

Magnitud de referencia: Liu et al. 2024 reportan caídas de **15-25 puntos porcentuales** entre extremo y medio en varios modelos. Si tu curva muestra algo similar, estás reproduciendo el fenómeno.

## Coste estimado

Cada trial envía aproximadamente `context-chars / 4` tokens de input más una respuesta corta. Coste por experimento ≈

```
n_posiciones × n_trials × (context_chars / 4) × precio_input_por_token
```

Catálogo de precios indicativos en `src/prices.yaml` (mayo 2026).

Algunos ejemplos prácticos:

| Modelo | Contexto | Pos × Trials | Coste aprox. |
|--------|----------|--------------|--------------|
| `gpt-4o-mini` | 20k chars (~5k tok) | 5 × 3 = 15 | **~$0.01** |
| `claude-haiku-4-5` | 20k chars (~5k tok) | 5 × 3 = 15 | **~$0.06** |
| `gpt-4o` | 100k chars (~25k tok) | 7 × 5 = 35 | **~$2.20** |
| `claude-opus-4-7` | 100k chars (~25k tok) | 7 × 5 = 35 | **~$13** |

Recomendación: **siempre** empezar con `--runner mock` para validar el setup, después escalar a un modelo barato (`gpt-4o-mini` o `claude-haiku-4-5`), y reservar Opus/GPT-4-turbo para una pasada final.

## Caveats

- Es **needle-in-haystack**: una tarea sintética de retrieval (encontrar una frase clave en medio de texto distractor). Tu caso real puede tener efectos distintos —preguntas multihop, razonamiento en cadena, instrucciones implícitas— donde el lost-in-the-middle se manifiesta de otra forma.
- La aguja es siempre la misma frase canónica. Si tu caso real depende de cifras o nombres concretos, replica el experimento adaptando `src/needle.py`.
- Esta herramienta da una **primera aproximación**, no un veredicto definitivo. Si una decisión de producto depende del resultado, valida también con tu propio gold set.
- Modelos detrás de proxies o con caching agresivo pueden inflar el recall artificialmente. Si los números son sospechosamente altos, varía `--seed` y revisa la varianza entre trials.

## Comandos disponibles

- `/medir-olvido` — Lanza un mini-experimento con presets seguros y resume la curva en una línea. Ver `commands/medir-olvido.md`.

## Referencias

- Artículo Gemba [«¿Por qué los LLMs olvidan?»](https://www.gemba.es/) — 25 de mayo de 2026.
- Liu et al. 2024 «Lost in the Middle: How Language Models Use Long Contexts» — TACL.
- Repo hermano `gemba-attention-from-scratch` — la mecánica de la atención desde dentro.
- Catálogo de precios: `src/prices.yaml` en este repo.

---

*Material complementario del artículo de Gemba [«¿Por qué los LLMs olvidan?»](https://www.gemba.es/) — 25 de mayo de 2026.*
