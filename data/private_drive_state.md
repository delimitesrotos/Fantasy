# Contrato del estado privado en Drive

La fuente canónica del jugador es una copia privada de
`templates/Fantasy-Estado-Privado.xlsx`, convertida a Google Sheets en su propio
Drive. La conversación no es la base de datos.

## Identidad del documento

- Nombre: `Fantasy — Estado privado — <nombre de liga>`.
- Una hoja por liga.
- Ubicación: Drive conectado del jugador.
- Visibilidad inicial: privada; no compartir automáticamente.
- Identificador: URL real devuelta por Drive, nunca una URL inventada.

## Ingesta desde captura o audio

1. Registrar la evidencia original en la carpeta privada `Evidencias` cuando la
   acción de subida esté disponible.
2. Extraer un borrador estructurado con fuente y fecha.
3. Mostrar únicamente el resumen necesario para validar.
4. Pedir confirmación o corrección al jugador.
5. Escribir datos y enlace a evidencia solo tras confirmación.
6. Actualizar `Control` y, si corresponde, añadir un evento append-only.

Si no es posible guardar el original, `Evidencias` debe marcar
`archivo_drive_url = UNKNOWN` y el chat debe avisarlo. No puede afirmar que el
archivo quedó archivado.

## Lectura antes de responder

Cada sesión y cada recomendación comienzan leyendo `Control` y las pestañas
privadas relevantes. Si un recuerdo del chat contradice la hoja, prevalece la
hoja. Los datos públicos del repositorio solo enriquecen el estado privado; no
lo sustituyen.

