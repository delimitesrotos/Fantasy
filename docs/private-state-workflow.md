# Flujo de estado privado

Este documento define el recorrido único para una persona sin conocimientos
técnicos. No requiere Drive, instalación, scripts ni una cuenta del propietario
del repositorio. La memoria oculta del chat nunca es la referencia principal.

## Las tres frases que necesita conocer

- **Empezar Fantasy**: inicia o reanuda el onboarding.
- **¿Qué hago hoy?**: revisa el mercado privado y las prioridades del día.
- **Prepara mi jornada**: compara alternativas de alineación.

El chat guía el resto. Si falta información, pide una sola captura o dato por
mensaje y explica para qué sirve.

## Primera configuración

1. El chat busca una cápsula `ESTADO_FANTASY` previa. Si no existe, crea la
   plantilla de `data/private_state_capsule.md` con valores `UNKNOWN`.
2. Pide una captura de las reglas y prepara el bloque `liga`.
3. Pide una captura de la plantilla, saldo y valor; prepara el bloque `usuario`.
4. Pide una captura de la clasificación; completa `clasificacion` y `rivales`.
5. Declara la configuración básica lista. Las plantillas rivales se incorporan
   progresivamente cuando aparezcan; no bloquean el uso.
6. Resume lo entendido y pide confirmación antes de marcar cada bloque como
   completo. Después muestra la cápsula actualizada.

## Uso diario

1. Con **¿Qué hago hoy?**, el chat relee la última cápsula visible.
2. Si no existe mercado de hoy, pide una sola captura del mercado privado.
3. Cruza esos datos con el snapshot público fresco del repositorio.
4. Presenta un máximo de tres decisiones. Cada una sigue
   `skills/decision-brief.md`: evidencia, incertidumbre, opciones e
   implicaciones.
5. El usuario elige. El chat pregunta una confirmación final si la respuesta
   implica compra, venta, cambio de saldo o alineación.
6. Solo tras confirmar, añade un objeto a `eventos_confirmados`, actualiza los
   bloques afectados y vuelve a mostrar la cápsula completa.

## Actualizaciones puntuales

El usuario puede decir frases naturales como «He comprado a X por 8 M» o «Y ha
fichado a X». El chat resuelve la identidad, muestra el cambio propuesto y pide
confirmación. Después registra el evento y actualiza la cápsula. No pide una
captura completa salvo contradicción o antigüedad real.

## Política de frescura

| Bloque | Vigencia | Si caduca |
|---|---|---|
| Reglas | Hasta cambio comunicado | Preguntar solo la regla afectada |
| Plantilla y saldo | Cada evento; aviso a las 48 h | Pedir confirmación breve |
| Mercado privado | Día de captura | Pedir captura de hoy |
| Clasificación | Jornada actual; aviso a 7 días | Pedir clasificación |
| Plantillas rivales | Parciales, con fecha | Declarar cobertura y confianza |

## Cambio de chat

El chat termina cada actualización con una cápsula visible y la frase «Si abres
otro chat, pega este bloque después del enlace del repositorio». No es necesario
entender ni editar YAML: el amigo solo copia el bloque completo. Si lo pierde,
el onboarding lo reconstruye con las tres capturas básicas.

## Privacidad

Los datos quedan exclusivamente en la conversación del amigo y en cualquier
copia que él decida guardar. Nunca se envían al Drive ni a cuentas del
propietario del repositorio, ni se incluyen en el repositorio público. Toda
operación en LALIGA la ejecuta el usuario manualmente.
