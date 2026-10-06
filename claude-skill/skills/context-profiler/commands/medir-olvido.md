---
description: Lanza un mini-experimento needle-in-haystack contra el modelo configurado y reporta la curva de recall por posición
allowed-tools: Bash, Read
argument-hint: [--runner mock|openai|anthropic] [--model <id>] [--context-chars N]
---

# /medir-olvido

Ejecuta el CLI de `gemba-context-needle-runner` con presets seguros (5 posiciones, 3 trials, 20k chars de heno) y devuelve un resumen interpretado de los resultados.

## Antes de ejecutar

Comprueba en este orden:

1. **Repo clonado.** Busca `~/gemba-context-needle-runner/`. Si no existe, pregunta al usuario dónde está y haz `cd` allí. Si no lo tiene, sugiérele:
   ```bash
   git clone https://github.com/joseperezaguera/gemba-context-needle-runner.git ~/gemba-context-needle-runner
   ```
2. **Dependencias.** El runner `mock` no requiere claves. Para `openai` o `anthropic`, verifica que `OPENAI_API_KEY` o `ANTHROPIC_API_KEY` esté en el entorno.
3. **Default seguro.** Si el usuario no especifica `--runner`, usa `--runner mock` para evitar gasto inesperado. Avisa: *"Voy a usar el runner mock para validar el setup sin coste. Si quieres medir tu modelo real, dímelo."*

## Pasos

1. `cd` al repo.
2. Construye el comando:
   ```bash
   python -m src.cli \
     --runner <X> \
     --model <Y> \
     --context-chars 20000 \
     --positions 0.05,0.25,0.5,0.75,0.95 \
     --n-trials 3 \
     --output output/recall_curve.png
   ```
3. Ejecuta y captura la tabla de la salida (`pos | recall`).
4. Resume al usuario en este formato:
   - Tabla con las 5 posiciones y su recall.
   - Posición del **mínimo** (la más floja).
   - Caída del **extremo al medio** en puntos porcentuales: `max(extremos) - min(medio)`.
   - Veredicto en una línea:
     - Caída < 5 pp → *"lost-in-the-middle leve"*.
     - 5-15 pp → *"lost-in-the-middle moderado"*.
     - \> 15 pp → *"lost-in-the-middle fuerte (en línea con Liu et al. 2024)"*.
5. Devuelve la ruta del PNG: `output/recall_curve.png`.

## Ejemplos

```
/medir-olvido
```
→ corre con `--runner mock` (sin coste).

```
/medir-olvido --runner openai --model gpt-4o-mini
```
→ ~$0.01 con los presets por defecto.

```
/medir-olvido --runner anthropic --model claude-sonnet-4-6 --context-chars 50000
```
→ contexto más largo, ~$0.20-0.40.

## Si algo falla

- **Falta `OPENAI_API_KEY` o `ANTHROPIC_API_KEY`** → indica al usuario qué exportar y reintenta.
- **Recall plano a 1.0** → ningún olvido; sugiere subir `--context-chars` (50k, 100k) para forzar el efecto.
- **Recall plano a 0** → la aguja no se está localizando ni en los bordes; revisa que el modelo sea instructable y no un modelo base.
- **Varianza alta entre runs** → sugiere subir `--n-trials` a 5 o 7.

## Recordatorio

Esta es una **primera aproximación**. Si una decisión de producto depende del resultado, valida también con tu propio gold set específico del dominio.
