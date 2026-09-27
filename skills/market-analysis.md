# Skill: Market Analysis

**Cuándo usar:** el usuario envía una captura/lista de su mercado privado o pide
analizar el mercado del día.

## Workflow

1. Extrae todos los jugadores y los precios que muestra la app; esos precios
   explícitos tienen prioridad durante la conversación.
2. Lee `data/public/latest/metadata.json`. Solo si mercado y/o titularidad están
   `fresh`, carga en bloque `players.json`, `market-values.json` y
   `starter-probabilities.json`.
3. Resuelve identidades por `player_id`; usa nombre normalizado + equipo +
   posición solo para localizar el ID. No unas jugadores únicamente por apellido.
4. Usa el snapshot para valor de referencia, variación diaria y titularidad.
   Nunca rellenes un valor ausente con otra plataforma o un snippet.
5. Busca en web solo contexto complementario: lesión, sanción, entrenamiento,
   rueda de prensa, rotación o calendario.
6. Cruza con saldo/reglas y aplica `scoring/marginal_value.md`.

Si el snapshot está `stale`, muestra el último valor conocido con fecha y
advertencia. Si no puede verificarse, devuelve `UNKNOWN`.

## Salida

Devuelve un Top 3 de decisiones. Para cada jugador separa **HECHO**
(precio/tendencia con fuente y fecha), **ESTIMACIÓN** (titularidad y jornada) y
la ficha de `skills/decision-brief.md`. Contrasta fichar, esperar y la mejor
alternativa disponible; explica el coste de oportunidad antes de pedir elección.
