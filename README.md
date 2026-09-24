# LALIGA Fantasy Decision Assistant

Este es un "cerebro de decisión" local para LALIGA Fantasy. No automatiza acciones en tu cuenta; te ayuda a tomar decisiones matemáticas y tácticas basadas en el valor marginal y el coste de oportunidad.

## Cómo usar el asistente (Fase 1)

1. **Arranca la sesión:** Proporciona este repositorio (o el archivo `SKILL.md`) como contexto a tu LLM (ChatGPT, Claude, Gemini).
2. **Ejecuta el Grill:** Si es tu primera vez, el asistente te pedirá que pases por el `protocolo_grill.md` para definir tu liga (sistema de puntos, presupuesto, etc.).
3. **Pasa a la acción:** Envía capturas de pantalla de tu mercado, tu plantilla o escribe tu duda directamente (ej. *"¿Comprarías a Lamine por 20M?"*).
4. **Decide:** El LLM cruzará tu contexto privado con búsquedas web públicas (si falta información) y te dará la decisión recomendada y el precio máximo, usando la lógica de los archivos `skills/` y `scoring/`.

## Regla de Oro
**NUNCA introduzcas credenciales ni tokens de tu cuenta real de LALIGA.** Toda operación la ejecutas tú manualmente en tu app móvil.
