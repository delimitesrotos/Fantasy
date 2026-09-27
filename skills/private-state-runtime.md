# Skill: Controlador transversal de estado privado

**Cuándo usar:** al principio de todos los turnos, antes de cualquier análisis o
recomendación personalizada. El usuario no necesita invocarla.

## Regla absoluta

La hoja privada del Drive del jugador es la única fuente canónica para liga,
saldo, plantilla, mercado privado, rivales y eventos. La memoria del chat puede
ayudar a entender el mensaje actual, pero nunca sustituye una lectura o escritura
de la hoja.

## Enrutador de cada mensaje

Ejecuta siempre, en este orden:

1. **LOCALIZAR:** encuentra la única hoja `Fantasy — Estado privado — <liga>` en
   el Drive conectado del jugador. Si no existe, ejecuta `skills/onboarding.md`.
2. **LEER CONTROL:** consulta frescura, onboarding, pendientes y URL de
   evidencias antes de interpretar el mensaje.
3. **CLASIFICAR:** decide si el mensaje contiene:
   - dato privado nuevo;
   - corrección de un dato;
   - evento ya ocurrido;
   - intención futura o hipótesis;
   - pregunta sin actualización.
4. **PERSISTIR PRIMERO:** si hay datos nuevos o correcciones, completa el ciclo
   de actualización antes de recomendar.
5. **ANALIZAR DESPUÉS:** solo con el readback verificado combina hoja privada +
   snapshot público + contexto web permitido.
6. **DECIDIR CON EL USUARIO:** aplica `skills/decision-brief.md`.

Si un mismo mensaje contiene una captura y «¿qué hago hoy?», primero procesa y
persiste la captura; después responde la pregunta con el estado recién leído.

## Ciclo de actualización automática

El jugador nunca tiene que decir «actualiza la hoja».

1. Lee `Control` y las filas relacionadas.
2. Extrae un borrador de la captura, audio o texto.
3. Calcula un diff: altas, bajas, cambios de saldo, reglas, mercado y rivales.
4. Si procede de OCR/audio, afecta varias filas, es ambiguo o contradice la
   hoja, enseña el resumen y pregunta una sola confirmación.
5. Si el usuario afirma inequívocamente un hecho pasado —«compré a X por 8 M»,
   «vendí a Y», «mi saldo es 12 M»— la frase cuenta como confirmación del hecho;
   actualiza automáticamente y comunica el cambio realizado.
6. No persistas intenciones, condicionales o simulaciones —«compraría», «si
   vendo», «quizá fiche»— como hechos.
7. Escribe primero el evento append-only y después las vistas derivadas.
8. Actualiza timestamps, fuente, confianza y `Control`.
9. Relee los rangos escritos. Si el readback no coincide, informa del fallo y no
   presentes el dato como persistido.

## Evidencias

- Cuando Drive permita subir el adjunto original, guárdalo en la carpeta privada
  `Evidencias` y enlázalo en la pestaña homónima.
- Si la subida no está disponible, registra `archivo_drive_url = UNKNOWN`,
  conserva la extracción confirmada y avisa que el original no quedó archivado.
- Nunca subas datos privados al repositorio público.

## Actualización diaria y esporádica

- **Mercado privado:** válido solo para la fecha de captura. En «¿Qué hago hoy?»
  pide el mercado de hoy si falta y lo persiste antes del análisis.
- **Plantilla y saldo:** actualiza tras cada compra/venta; si llevan 48 horas sin
  reconciliar y hay riesgo de cambios externos, pide una confirmación breve.
- **Clasificación:** vigente durante la jornada; pide nueva captura al cambiar de
  jornada o tras siete días.
- **Rivales:** acepta cobertura parcial, añade eventos conforme aparecen y nunca
  presenta una plantilla rival como completa sin evidencia.
- **Reglas:** permanecen vigentes hasta que el jugador comunique un cambio.

## Separación del flujo público

El controlador privado se ejecuta antes. Después, las skills públicas consultan
`metadata.json`, snapshots y fuentes web. Los datos públicos nunca sobrescriben
saldo, mercado privado, reglas particulares, plantilla o rivales de la hoja.

