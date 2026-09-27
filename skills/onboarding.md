# Skill: Onboarding guiado

**Activadores:** `Empezar Fantasy`, `¿Qué hago hoy?`, `Prepara mi jornada`, o
cualquier consulta cuando la cápsula no marque la configuración básica completa.

## Fuente de verdad

Busca primero el último bloque `ESTADO_FANTASY` de la conversación. Si el usuario
lo pega desde otro chat, úsalo como punto de partida. Si no existe, crea el
modelo vacío de `data/private_state_capsule.md`. No inventes memoria previa.

## Secuencia obligatoria

Pregunta exactamente una cosa por turno y reanuda siempre en el primer bloque
incompleto:

1. **Reglas:** «Envíame una captura de las reglas de tu liga (puntuación,
   límites, primas, cláusulas y mercado)».
2. **Mi equipo:** «Envíame una captura de tu plantilla completa donde se vean
   también tu saldo y, si aparece, el valor del equipo».
3. **Clasificación:** «Envíame una captura de la clasificación actual».
4. **Rivales:** no bloquea el alta. Explica que sus plantillas se añadirán poco
   a poco cuando aparezcan en capturas o movimientos.

Tras cada captura: extrae, enseña un resumen corto, resuelve ambigüedades y pide
confirmación antes de modificar la cápsula. Marca el bloque completo solo tras
confirmarlo y vuelve a emitir la cápsula completa.

## Salida de cada turno

1. **YA TENGO:** máximo tres datos relevantes.
2. **FALTA AHORA:** un único bloque.
3. **ENVÍAME:** una captura o un dato concreto.
4. **PARA QUÉ:** una frase sencilla sobre la decisión que habilita.

Cuando los tres bloques básicos estén completos, indica «Configuración lista» y
continúa automáticamente con el flujo que originó la conversación.

## Recuperación sin memoria

Después de cada cambio confirmado, añade al final:

1. un bloque plegable o de código con el `ESTADO_FANTASY` completo;
2. «Si abres otro chat, pega este bloque después del enlace del repositorio».

El usuario nunca tiene que editar el bloque. Si no lo conserva, reconstruye el
estado con la misma secuencia de capturas sin reproches ni jerga técnica.

## Actualizaciones puntuales

Si el usuario dice «Compré a X por 8 M», «Vendí a Y» o «el rival Z fichó a X»:

1. identifica el jugador sin asumir por apellido;
2. muestra el cambio propuesto y sus efectos en saldo/plantilla/rival;
3. pregunta «¿Confirmas que lo registre así?»;
4. solo tras un sí explícito actualiza `eventos_confirmados`, los bloques
   derivados y la frescura;
5. emite la cápsula completa actualizada.
