# 03 — Encontrando tu sweet spot de contexto

> Coste estimado: **$0.10-0.50** para un barrido completo en un modelo barato.

## El sweet spot

La intuición habitual es *"mete tanto contexto como te permita la ventana"*. Es mala intuición.

Cada modelo tiene un **sweet spot**: el tamaño de contexto donde recall es alto y consistente. Por debajo de ahí desperdicias capacidad; por encima, empiezas a perder información del centro. Encontrar ese sweet spot para **tu modelo y tu tipo de prompt** te ahorra dinero (menos tokens) y te da más calidad (menos olvido).

Síntomas de que estás pasado de tamaño:

- El sistema deja de obedecer instrucciones del system prompt.
- Las respuestas "esquivan" partes del input que sabes que están ahí.
- La calidad cae no por la pregunta, sino por el ruido del contexto.

## Comando

Barre `--context-chars` en una escalera y observa cómo se deforma la curva:

```bash
export OPENAI_API_KEY=sk-...

for chars in 5000 20000 50000 100000 200000; do
  python -m src.cli \
    --runner openai --model gpt-4o-mini \
    --context-chars $chars \
    --n-trials 3 \
    --seed 7 \
    --output output/sweet_${chars}.png
done
```

Esto deja cinco PNGs en `output/sweet_*.png`. Mismo modelo, mismas posiciones, mismas trials — solo cambia el tamaño del heno.

## Cómo decidir tu zona segura

Abre los cinco PNGs en orden de menor a mayor `--context-chars` y busca **el último** que cumpla los tres criterios:

1. **Recall medio (pos=0.5) por encima de 0.7.** Por debajo de ahí, el modelo está olvidando información crítica.
2. **Diferencia extremo-centro por debajo de 0.2.** Si la U es demasiado profunda, cualquier dato que metas en el medio es ruleta.
3. **Varianza baja entre trials.** Si los tres trials de la misma posición dan números muy distintos, el modelo está al límite y no es fiable.

Ese tamaño es tu **techo cómodo**. Tu zona segura es trabajar entre el 50% y el 80% de ese techo: tienes margen para variabilidad en producción y para inputs ocasionalmente más largos.

## Heurística rápida

Si no quieres barrer, una heurística honesta:

- Empieza por `--context-chars` = 25% de la ventana nominal del modelo (un modelo de 128k tokens → 32k tokens ≈ 130k chars).
- Mide. Si pasa los tres criterios, sube al 50%. Si no, baja al 12%.
- Itera dos o tres veces hasta encontrar el último tamaño que pasa.

## Coste del barrido completo

Con `gpt-4o-mini`, 5 tamaños × 5 posiciones × 3 trials:

| Tamaño | Coste aprox. |
|--------|--------------|
| 5k chars | ~$0.002 |
| 20k chars | ~$0.01 |
| 50k chars | ~$0.03 |
| 100k chars | ~$0.06 |
| 200k chars | ~$0.12 |
| **Total** | **~$0.22** |

Por menos de 25 céntimos sabes dónde colapsa **tu** modelo. Después puedes tomar decisiones de arquitectura (chunking, RAG, resumen) con datos en vez de intuición.
