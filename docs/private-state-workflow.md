# Flujo de estado privado

Este documento define el recorrido único para una persona sin conocimientos
técnicos. Requiere que el jugador conecte una vez su propio Google Drive, pero no
requiere instalación, scripts ni una cuenta del propietario del repositorio. La
memoria del chat nunca es la referencia principal.

## Las tres frases que necesita conocer

- **Empezar Fantasy**: inicia o reanuda el onboarding.
- **¿Qué hago hoy?**: revisa el mercado privado y las prioridades del día.
- **Prepara mi jornada**: compara alternativas de alineación.

El chat guía el resto. Si falta información, pide una sola captura o dato por
mensaje y explica para qué sirve.

## Primera configuración

1. El chat guía la conexión del Drive del jugador y busca una única hoja de su
   liga. Si no existe, importa `templates/Fantasy-Estado-Privado.xlsx`, crea
   `Evidencias` y verifica lectura/escritura.
2. Pide una captura de las reglas, confirma la extracción y escribe `Liga`.
3. Pide una captura de la plantilla, saldo y valor; escribe `Mi equipo`.
4. Pide una captura de la clasificación; escribe `Rivales`.
5. Declara la configuración básica lista. Las plantillas rivales se incorporan
   progresivamente cuando aparezcan; no bloquean el uso.
6. Resume lo entendido y pide confirmación antes de marcar cada bloque como
   completo. Escribe, verifica y formula automáticamente la siguiente pregunta.

## Uso diario

1. Con **¿Qué hago hoy?**, el chat localiza la hoja y relee `Control`.
2. Si no existe mercado de hoy, pide una sola captura del mercado privado.
3. Cruza esos datos con el snapshot público fresco del repositorio.
4. Presenta un máximo de tres decisiones. Cada una sigue
   `skills/decision-brief.md`: evidencia, incertidumbre, opciones e
   implicaciones.
5. El usuario elige. El chat pregunta una confirmación final si la respuesta
   implica compra, venta, cambio de saldo o alineación.
6. Solo tras confirmar, añade una fila append-only a `Eventos`, actualiza las
   pestañas afectadas, relee los rangos y confirma la persistencia.

## Actualizaciones puntuales

El usuario puede decir frases naturales como «He comprado a X por 8 M» o «Y ha
fichado a X». El chat resuelve la identidad, muestra el cambio propuesto y pide
confirmación cuando sea necesaria. Después registra el evento y actualiza la
hoja automáticamente. No pide una
captura completa salvo contradicción o antigüedad real.

## Política de frescura

| Bloque | Vigencia | Si caduca |
|---|---|---|
| Reglas | Hasta cambio comunicado | Preguntar solo la regla afectada |
| Plantilla y saldo | Cada evento; aviso a las 48 h | Pedir confirmación breve |
| Mercado privado | Día de captura | Pedir captura de hoy |
| Clasificación | Jornada actual; aviso a 7 días | Pedir clasificación |
| Plantillas rivales | Parciales, con fecha | Declarar cobertura y confianza |

## Control transversal de cada mensaje

Antes de responder, el chat ejecuta `skills/private-state-runtime.md`. Detecta
datos nuevos incluso cuando el jugador no pide guardarlos. Si el mismo mensaje
también solicita consejo, la escritura ocurre primero y el análisis usa el
readback recién verificado.

## Cambio de chat

El nuevo chat conecta el mismo Drive, busca la hoja por nombre exacto, lee
`Control` y continúa. No se copia ningún estado desde el historial.

## Privacidad

Los datos estructurados quedan en la hoja privada y las evidencias originales,
cuando sea posible subirlas, en la carpeta privada del Drive del jugador. Nunca
se envían a cuentas del propietario del repositorio ni al repositorio público.
Toda operación en LALIGA la ejecuta el usuario manualmente.
