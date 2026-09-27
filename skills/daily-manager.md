# Skill: Daily Manager

**Cuándo usar:** «¿Qué hago hoy?» o petición de análisis diario integral.

## Workflow

1. Lee `metadata.json` y, si está fresco, carga una sola vez todo
   `data/public/latest/`.
2. Cruza el snapshot con la lista/captura diaria del mercado privado, la plantilla
   y el saldo. No busques cada jugador individualmente.
3. Detecta huecos del once, sanciones, lesiones y activos que pierden valor.
4. Busca contexto web únicamente para novedades deportivas posteriores al
   snapshot.
5. Prioriza las tres acciones con mayor valor marginal y coste de oportunidad.

Persiste lógicamente los eventos `BUY`, `SELL`, cambios de saldo y plantilla. No
pidas capturas completas repetidas salvo inconsistencia real.

## Salida

Tres prioridades como máximo: **VENDER**, **PUJAR**, **ALINEAR** o **MANTENER
CASH**. Cada dato dinámico incluye fuente/frescura y cada conclusión queda
separada como **ANÁLISIS**.
