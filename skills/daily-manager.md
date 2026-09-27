# Skill: Daily Manager

**Cuándo usar:** «¿Qué hago hoy?» o petición de análisis diario integral.

## Workflow

1. Lee la última cápsula `ESTADO_FANTASY`. Si el onboarding básico no está
   completo, reanuda `skills/onboarding.md` en el primer bloque ausente.
2. Comprueba frescura privada: reglas hasta cambio comunicado; plantilla/saldo
   tras cada evento y aviso a las 48 horas; clasificación de la jornada actual o
   aviso a los 7 días; mercado únicamente válido en la fecha de captura. Si no
   hay mercado de hoy, pide una sola captura antes de recomendar pujas exactas.
3. Lee `metadata.json` y, si está fresco, carga una sola vez todo
   `data/public/latest/`.
4. Cruza el snapshot con la lista/captura diaria del mercado privado, la plantilla
   y el saldo. No busques cada jugador individualmente.
5. Detecta huecos del once, sanciones, lesiones y activos que pierden valor.
6. Busca contexto web únicamente para novedades deportivas posteriores al
   snapshot.
7. Prioriza las tres decisiones con mayor valor marginal y coste de oportunidad.

Persiste lógicamente los eventos `BUY`, `SELL`, cambios de saldo y plantilla. No
pidas capturas completas repetidas salvo inconsistencia real.

## Salida

Tres prioridades como máximo. Cada una usa `skills/decision-brief.md`, compara
al menos dos opciones —por ejemplo **PUJAR** frente a **MANTENER CASH**— e
incluye fuente/frescura, impacto, riesgo, reversibilidad y umbral de cambio.
