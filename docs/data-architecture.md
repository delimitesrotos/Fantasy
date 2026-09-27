# Arquitectura de datos públicos

## Flujo

```text
FútbolFantasy (HTML público, una petición)
        │
        ▼
fetch → parse → validate → freshness gate → serialize
                                            │
                                            ▼
                                  data/public/latest/
                                            │
                                            ▼
                              SKILL y workflows de decisión
```

La adquisición no decide y las skills no extraen HTML. El parser produce
registros tipados; el validador acepta o rechaza el lote completo; el serializador
publica documentos deterministas solo después de superar todos los controles.

## Componentes

- `scripts/public_data/fetch.py`: una petición HTTPS identificada, con timeout,
  límite de 8 MB y comprobación de tipo de contenido.
- `parse.py`: valida marcadores independientes de plataforma y extrae filas con
  `HTMLParser`. Los nombres normalizados son alias; el ID primario es
  `futbolfantasy:<source_id>`.
- `validate.py`: comprueba recuentos, posiciones, equipos, referencias, IDs,
  rangos, plataforma y cambios bruscos frente al snapshot previo.
- `freshness.py`: calcula `fresh`, `stale` o `unknown`; nunca acepta el estado
  declarado por una entrada.
- `serialize.py`: construye los cuatro contratos JSON y los sustituye desde un
  directorio temporal.
- `update_public_data.py`: orquesta modo vivo, fixtures, `--check` y publicación.

## Contratos de salida

`metadata.json` es el punto de entrada. Contiene estado del pipeline, plataforma,
recuentos y metadata por fuente. Un consumidor debe detenerse si el dataset que
necesita no está `fresh`.

`players.json` separa identidad de observaciones dinámicas. `market-values.json`
y `starter-probabilities.json` referencian siempre `player_id`; nunca enlazan por
nombre visible.

Los timestamps usan ISO 8601 con zona horaria. El mercado se evalúa contra
`source_updated_at` con 30 horas de máximo. La titularidad no ofrece timestamp
propio en la fuente, por lo que usa `retrieved_at` y un máximo de 8 horas.

## Validación y fallos

Se rechaza un lote cuando falta la identidad inequívoca de plataforma, hay menos
de 400 jugadores o 15 equipos, falta una posición, existen IDs duplicados,
referencias rotas, precios no positivos, porcentajes fuera de 0–100, timestamps
inválidos, caída superior al 20 % del censo o variación individual superior al
50 % frente al snapshot previo.

Ante fallo, los tres datasets del último snapshot válido permanecen intactos.
Solo `metadata.json` registra `pipeline_status: failed`, recalcula la frescura y
guarda el error. El comando devuelve código distinto de cero y GitHub Actions
termina visiblemente en rojo después de conservar esa metadata.

## Automatización

`.github/workflows/update-public-data.yml` se ejecuta cuatro veces al día y bajo
demanda. Usa `ubuntu-latest`, permisos `contents: write`, concurrencia única,
Python 3.11 y ninguna dependencia externa. Ejecuta toda la suite antes de
consultar la fuente y solo crea un commit cuando cambia el contenido.

## Seguridad y privacidad

El pipeline no conoce cuentas, ligas ni usuarios de LALIGA. No existen secretos,
cookies o endpoints autenticados. `data/public/` contiene únicamente datos
públicos. `data/user_state.md` es una plantilla; el estado real debe permanecer
en el chat o en almacenamiento privado del usuario.
