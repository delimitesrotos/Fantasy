# Skill: Preparar Jornada

**Cuándo usar:** el usuario pide su once o duda entre jugadores.

## Workflow

1. Lee `metadata.json` y usa primero `starter-probabilities.json` fresco para la
   jornada objetivo. Resuelve cada jugador mediante `players.json`.
2. Descarta lesionados graves y sancionados confirmados.
3. Busca después contexto reciente: entrenamientos, rueda de prensa, lesión de
   última hora, sanción, competición europea o rotación.
4. No conviertas ausencia de porcentaje en 0 %; significa `UNKNOWN`.
5. Elige formación legal que maximice puntos marginales. Para desempates valora
   localía, balón parado, rival y minutos esperados.

## Salida

- **EL ONCE:** once por posición.
- **ESTIMACIONES:** probabilidades con fuente, jornada y hora de consulta.
- **DUDAS/ROTACIONES:** hechos recientes y nivel de riesgo.
- **DECISIÓN DISCUTIBLE:** compara al menos las dos alineaciones razonables,
  explica techo, suelo, minutos, rival y qué noticia haría cambiar la elección.
- **TU DECISIÓN:** ofrece una preferencia, pero pide al usuario que confirme el
  once que quiere usar.

No presentes una probabilidad `stale` como actual.
