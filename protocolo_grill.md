# Protocolo de Grill Inicial (User State)

Cuando el usuario inicia el asistente sin contexto previo, aplica
`skills/onboarding.md`. Este archivo conserva el contenido que debe extraerse,
pero ya no se pregunta en un bloque ni se confía en la memoria del chat.

**Instrucción para el LLM:** Pide una sola captura o dato por turno, explica para
qué sirve y guarda lo confirmado en la hoja privada del Drive del jugador.

### Las 5 preguntas del Grill

1. **Sistema de puntuación:** ¿Qué sistema usas en tu liga? (Picas AS, Sofascore, Estadísticas, Mixto, Relevo).
2. **Capital Inicial / Actual:** ¿De qué presupuesto líquido (cash) dispones ahora mismo para fichar?
3. **Límites de tu liga:** ¿Hay alguna regla especial? (Máximo de jugadores en plantilla, límite por equipo, prohibido clausular, abonos fijos por punto, etc.).
4. **Intocables:** ¿Qué 2 o 3 jugadores de tu equipo actual consideras el núcleo duro que NO venderías bajo ninguna circunstancia?
5. **Perfil de Inversor:** 
   - *Conservador:* Prioriza titulares fijos, evita rotaciones y apuestas, compra valor seguro.
   - *Agresivo (Trader):* Busca especular con jugadores lesionados que vuelven, parches que suben de precio rápido, asume más ceros a cambio de maximizar patrimonio.

*(Nota interna: la hoja privada es el `User State` canónico. La memoria de
sesión solo sirve para preparar y confirmar la siguiente escritura).*
