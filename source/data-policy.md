# Política de fuentes y frescura

## Regla general

Todo dato dinámico debe declarar `source`, `platform`, `retrieved_at`,
`source_updated_at` cuando exista, `freshness` y el valor observado. La ausencia
de trazabilidad convierte el dato en `UNKNOWN`.

## Jerarquía por campo

| Campo | Fuente primaria | Freshness | Alternativas permitidas |
|---|---|---|---|
| `market_value` | FútbolFantasy, página explícita de LALIGA Fantasy Oficial | 30 h desde `source_updated_at` | Dato que el usuario lee en su app; si no, `UNKNOWN` |
| `daily_change` | Misma fila y ciclo que `market_value` | 30 h | Ninguna fuente fantasy alternativa |
| `starter_probability` | FútbolFantasy, jugador/equipo/jornada identificados | 8 h desde `retrieved_at` | `UNKNOWN` si no se publica |
| lesiones y sanciones | FútbolFantasy, club o LALIGA | Contextual y fechado | Prensa deportiva fiable |
| fixtures | Fuente oficial o deportiva estructurada | Jornada identificada | Fuente secundaria verificable |

Fuente canónica del mercado:

`https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado`

No se aceptan automáticamente valores de otras plataformas, snippets, cachés
de buscador ni resultados antiguos. El dato explícito leído por el usuario en
su app oficial tiene prioridad únicamente para la conversación donde lo aporta.

## Auditoría de FútbolFantasy

Realizada el 27/09/2026:

- HTML público renderizado por servidor, sin autenticación ni API privada.
- URL canónica y encabezado identifican LALIGA Fantasy Oficial.
- Filas con ID, equipo, posición, valor, variación y probabilidad opcional.
- Timestamp explícito para el ciclo de mercado; sin timestamp independiente
  para cada probabilidad.
- `robots.txt` no restringe el acceso.
- El servidor anuncia 30 peticiones por cada 10 segundos; este proyecto hace
  como máximo cuatro peticiones diarias.
- El aviso legal reserva derechos sobre el contenido. El proyecto atribuye la
  fuente, limita la frecuencia y conserva solo hechos mínimos necesarios; no
  copia textos editoriales ni código.

Si aparecen bloqueos, CAPTCHA, autenticación o una prohibición material, se
detiene la extracción. No se suplantan navegadores ni se eluden protecciones.

## Freshness Gate

- `fresh`: observación válida dentro del umbral.
- `stale`: última observación válida fuera del umbral; solo puede mostrarse como
  último dato conocido con fecha y advertencia.
- `unknown`: no existe una observación válida.

Una fecha futura en más de cinco minutos, una plataforma ambigua o un ciclo de
mercado de más de 30 horas hacen fallar el pipeline.

## Regla de buscadores

Los snippets sirven para descubrir contexto, nunca como evidencia de un precio
exacto. Si el snapshot no está fresco, se abre la fuente canónica. Si esta no se
puede verificar, se responde `UNKNOWN`.
