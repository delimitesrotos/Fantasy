# LALIGA Fantasy Decision Assistant

Sistema de apoyo para tomar decisiones en **LALIGA Fantasy Oficial** desde un
chat normal de ChatGPT, Gemini o Claude. El usuario no ejecuta scripts ni
conecta su cuenta: aporta únicamente su estado privado y el mercado concreto de
su liga; el repositorio aporta inteligencia y datos públicos validados.

**Para una persona sin conocimientos técnicos:** abre
[`EMPEZAR_AQUI.md`](EMPEZAR_AQUI.md), copia el único mensaje y deja que el chat
guíe las capturas una a una.

## Las dos capas

### Inteligencia

`SKILL.md`, `skills/`, `scoring/` y `strategy/` contienen los procedimientos
para decidir compras, ventas y alineaciones mediante valor marginal y coste de
oportunidad.

### Datos públicos

`data/public/latest/` contiene:

- `metadata.json`: primer archivo que debe leer el chat; declara frescura,
  proveedor, timestamps, estado del pipeline y recuentos.
- `players.json`: identidad estable, nombre normalizado, equipo y posición.
- `market-values.json`: valor y variación diaria de LALIGA Fantasy Oficial.
- `starter-probabilities.json`: estimación de titularidad y jornada objetivo.

Cada dato dinámico conserva fuente, plataforma, fecha de consulta, fecha de
actualización cuando existe y estado `fresh`, `stale` o `unknown`.

## Uso desde móvil

1. Tu amigo abre un chat normal y envía este único mensaje:

   > Lee `https://github.com/delimitesrotos/Fantasy` y sigue `SKILL.md`.
   > Empezar Fantasy.

2. El onboarding pide una sola captura por turno y mantiene reglas, equipo y
   clasificación en una cápsula privada visible dentro de su conversación.
3. Después basta escribir **¿Qué hago hoy?** o **Prepara mi jornada**. Si hace
   falta, el chat pedirá una captura del mercado privado de ese día.
4. El chat consulta primero la cápsula, `metadata.json` y los snapshots frescos, y busca en
   Internet solamente contexto complementario.
5. Recibes alternativas justificadas con ventajas, costes, riesgos y umbrales.
   Tú eliges y confirmas; después ejecutas manualmente la acción en la app.

El propietario del repositorio no configura nada, no usa Drive y no recibe los
datos privados. Si tu amigo cambia de chat, pega la última cápsula que el propio
chat le mostró; no necesita entenderla ni editarla.

Un valor leído por ti en la aplicación oficial tiene prioridad durante esa
conversación. Si el snapshot está caducado y la fuente canónica no puede
verificarse, la respuesta correcta es `UNKNOWN`, no un número de otro fantasy.

## Actualización automática

GitHub Actions ejecuta `scripts/update_public_data.py` cuatro veces al día en
un runner estándar `ubuntu-latest`. El proceso realiza una única petición a la
página pública canónica de FútbolFantasy, ejecuta validaciones completas y
solo sustituye `latest/` si todo es coherente. Un fallo conserva el último
snapshot válido, actualiza su metadata y deja el workflow en rojo.

Ejecución local para mantenimiento:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/update_public_data.py --check
```

Consulta [la arquitectura de datos](docs/data-architecture.md) y
[la política de fuentes](source/data-policy.md) para los contratos completos.
El [flujo de estado privado](docs/private-state-workflow.md) explica el onboarding,
la actualización diaria y por qué supera a la memoria aislada de un chat.

## Seguridad absoluta

Nunca introduzcas credenciales, cookies ni tokens de LALIGA. Este repositorio
no autentica contra LALIGA, no usa APIs privadas y no ejecuta acciones en la
cuenta. No guardes información real de tu liga en este repositorio público;
`data/user_state.md` es exclusivamente una plantilla.
