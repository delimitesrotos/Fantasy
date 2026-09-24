# Protocolo de Grill Inicial (User State)

Cuando el usuario inicia el asistente sin contexto previo, el LLM DEBE realizarle esta entrevista rápida (grill) para configurar el perfil estratégico. 

**Instrucción para el LLM:** Haz estas preguntas de forma directa, en un solo bloque, para que el usuario responda en un único mensaje.

### Las 5 preguntas del Grill

1. **Sistema de puntuación:** ¿Qué sistema usas en tu liga? (Picas AS, Sofascore, Estadísticas, Mixto, Relevo).
2. **Capital Inicial / Actual:** ¿De qué presupuesto líquido (cash) dispones ahora mismo para fichar?
3. **Límites de tu liga:** ¿Hay alguna regla especial? (Máximo de jugadores en plantilla, límite por equipo, prohibido clausular, abonos fijos por punto, etc.).
4. **Intocables:** ¿Qué 2 o 3 jugadores de tu equipo actual consideras el núcleo duro que NO venderías bajo ninguna circunstancia?
5. **Perfil de Inversor:** 
   - *Conservador:* Prioriza titulares fijos, evita rotaciones y apuestas, compra valor seguro.
   - *Agresivo (Trader):* Busca especular con jugadores lesionados que vuelven, parches que suben de precio rápido, asume más ceros a cambio de maximizar patrimonio.

*(Nota interna: Una vez el usuario responda, el LLM mantendrá estos datos en su memoria de sesión como el `User State` base para condicionar todos los cálculos de límite de puja y riesgo).*
