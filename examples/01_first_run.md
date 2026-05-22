# 01 — Primera ejecución con MockRunner

> Coste: **cero**. Tiempo: **menos de un minuto**.

## Por qué empezar con MockRunner

Antes de gastar un euro contra OpenAI o Anthropic, conviene validar que el setup funciona:

- No requiere claves API ni red.
- Es **determinista** (mismo `--seed` → mismo resultado).
- Simula una curva en U realista, así que verás un gráfico parecido al que produciría un modelo real con lost-in-the-middle moderado.

Si MockRunner te devuelve una curva sensata y un PNG, ya tienes el repo funcionando y puedes pasar a modelos reales con confianza.

## Comando

Desde la raíz del repo:

```bash
pip install -r requirements.txt
python -m src.cli --runner mock
```

Eso es todo. No hay que exportar variables de entorno.

## Qué deberías ver

En consola, algo parecido a:

```
Runner: mock (mock-llm)
Heno: 20000 chars · posiciones: [0.05, 0.25, 0.5, 0.75, 0.95] · trials: 3
Ejecutando...

Resultados:
   pos |   recall
--------------------
  0.05 |   100.00%
  0.25 |    66.67%
  0.50 |    33.33%
  0.75 |    66.67%
  0.95 |   100.00%

Gráfico: output/recall_curve.png
```

Y un PNG en `output/recall_curve.png` con la curva en U.

## Interpretación

- **Extremos (pos=0.05 y pos=0.95)**: el modelo "recuerda" perfectamente. Esto es lo que esperarías de un LLM con lost-in-the-middle.
- **Centro (pos=0.5)**: caída fuerte. En MockRunner es exagerada a propósito para que la curva sea visible al primer vistazo.
- **Forma de U**: si la curva real de tu modelo se parece a esto (aunque más suave), estás reproduciendo el fenómeno medido por Liu et al. 2024.

## Siguiente paso

Cuando MockRunner te devuelva la curva esperada:

```bash
export OPENAI_API_KEY=sk-...
python -m src.cli --runner openai --model gpt-4o-mini
```

Con `gpt-4o-mini` y los presets por defecto, el experimento cuesta aproximadamente **$0.01**. Es la forma más barata de ver tu primera curva real.
