# 02 — Comparando dos modelos

> Coste estimado: **$0.05-0.20** según el par que elijas.

## Por qué comparar

No todos los modelos sufren lost-in-the-middle con la misma intensidad. Algunos colapsan a partir de 30k tokens; otros aguantan 100k decentemente. La única forma honesta de elegir entre dos candidatos para tu caso de uso es **medir los dos en el mismo experimento** y mirar las curvas lado a lado.

Casos típicos:

- *"¿Qué cumple mejor con 50k de contexto: `gpt-4o-mini` o `claude-haiku-4-5`?"*
- *"Estoy pagando Opus. ¿Realmente compensa frente a Sonnet en mi tipo de prompt?"*
- *"Voy a migrar de Anthropic a OpenAI. ¿Cuánto recall pierdo?"*

## Comandos

Ejecuta los dos con los **mismos parámetros**, cambiando solo el output para no sobrescribir:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

python -m src.cli \
  --runner openai --model gpt-4o-mini \
  --context-chars 30000 \
  --n-trials 5 \
  --seed 42 \
  --output output/openai_gpt4o-mini.png

python -m src.cli \
  --runner anthropic --model claude-haiku-4-5 \
  --context-chars 30000 \
  --n-trials 5 \
  --seed 42 \
  --output output/anthropic_haiku.png
```

**Importante:** usa la misma `--seed` en los dos. Así la posición exacta de la aguja en cada trial es la misma, y la comparación es justa.

## Cómo leer los dos PNGs

Abre los dos PNGs lado a lado. Pregúntate:

1. **¿Cuál tiene la U más profunda?** Ese sufre más lost-in-the-middle.
2. **¿En qué posición está el mínimo?** Algunos modelos tienen el mínimo justo en el centro (0.5), otros lo tienen desplazado.
3. **¿Cuál tiene mayor recall promedio?** No solo importa la U: si un modelo tiene recall 0.6 plano y otro tiene U entre 1.0 y 0.7, el segundo puede ser mejor opción dependiendo de tu prompt.
4. **¿Cuál tiene mejor recall en el rango de posición donde tú vas a meter información crítica?** Si tu system prompt va al inicio y tu pregunta al final, te importa menos el centro.

## Coste estimado del experimento

Con los parámetros del ejemplo (30k chars ≈ 7.5k tokens, 5 posiciones, 5 trials = 25 llamadas):

| Modelo | Coste aprox. |
|--------|--------------|
| `gpt-4o-mini` | ~$0.03 |
| `claude-haiku-4-5` | ~$0.15 |
| **Total comparación** | **~$0.20** |

Si quieres medir el par premium (`gpt-4o` vs `claude-sonnet-4-6`), súbelo a ~$1-2. Para `claude-opus-4-7`, cuenta con $5-10 si subes a 100k chars.

## Recordatorio

La aguja es siempre la misma frase canónica. Si tus casos reales son muy específicos (cifras, nombres propios, instrucciones implícitas), replica con tu propia aguja editando `src/needle.py` antes de cerrar la decisión.
