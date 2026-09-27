# Plantilla de estado privado

`Fantasy-Estado-Privado.xlsx` es una plantilla pública, neutra y sin datos
reales. Su finalidad es que un chat normal pueda crear una copia privada en el
Google Drive conectado del jugador.

## Regla de propiedad

La copia completada pertenece exclusivamente al jugador. Nunca se crea ni se
actualiza en el Drive del propietario del repositorio y nunca se devuelve al
repositorio público.

## Creación obligatoria

Antes de pedir capturas o audios privados, el chat debe:

1. comprobar que Google Drive está conectado en la cuenta del jugador con
   acciones de lectura y escritura;
2. buscar `Fantasy — Estado privado — <nombre de liga>` para evitar duplicados;
3. si existe una única coincidencia, leer `Control` y continuar;
4. si no existe, importar `Fantasy-Estado-Privado.xlsx` como Google Sheets
   nativo en el Drive del jugador;
5. crear junto a la hoja una carpeta privada `Evidencias`;
6. verificar que puede leer y escribir la hoja y conservar su URL como
   identificador canónico;
7. solo entonces comenzar el onboarding de datos.

Si el chat no dispone de una acción de escritura en Drive, debe detenerse y
guiar la conexión. No puede fingir persistencia ni sustituirla con Memory.

## Pestañas

- `Inicio`: instrucciones sencillas para el jugador.
- `Liga`: reglas, puntuación y límites.
- `Mi cuenta`: saldo, valor, puntos, posición y perfil de riesgo.
- `Mi equipo`: plantilla, precios, valores y estado.
- `Rivales`: clasificación y plantillas conocidas.
- `Mercado diario`: fotografía privada con fecha.
- `Eventos`: cambios confirmados y append-only.
- `Control`: frescura, huecos y siguiente pregunta.
- `Evidencias`: índice de capturas, audios y textos originales guardados en la
  carpeta privada de Drive.

Cada fila privada conserva fuente, fecha, confianza y estado. Un dato ambiguo se
guarda como `UNKNOWN` o queda pendiente; nunca se completa por memoria.
