# Skill: Market Analysis (Análisis Diario de Mercado)

**Cuándo usar:** El usuario sube una captura del mercado de fichajes y pregunta qué comprar, o dice "Analiza el mercado de hoy".

## Pasos del Análisis

1. **Extracción:** Identifica todos los jugadores de la captura, su precio (VM) y su racha de puntos.
2. **Contexto Externo (Vital):** Si el precio objetivo o la tendencia no se ven, busca en internet su tendencia de mercado actual (¿sube 100k al día? ¿está bajando?). 
3. **Cruce con el User State:** Filtra aquellos jugadores que el usuario NO puede permitirse o que chocarían con restricciones de su liga.
4. **Evaluación de Oportunidades:** Usa `scoring/marginal_value.md` para separar a los jugadores en tres buckets:
   - **Rendimiento (Titulares fiables):** Para puntuar el fin de semana.
   - **Trading (Especulación):** Jugadores baratos que están subiendo rápido de valor (lesionados que vuelven, revulsivos que acaban de marcar).
   - **Evitar:** Sobrepreciados o bajando en picado.

## Formato de Salida

Devuelve SOLO un Top 3 de acciones recomendadas con este formato:

1. **Jugador X:** [COMPRAR PARA RENDIMIENTO]
   - Puja Máxima: [XX Millones]
   - Riesgo: [Medio - Rotación por Champions]
   - Motivo: Mejora tu centro del campo directamente.

2. **Jugador Y:** [COMPRAR PARA ESPECULAR]
   - Puja Máxima: [Precio mercado + 10%]
   - Riesgo: [Bajo - Si no rinde se vende sin pérdida]
   - Motivo: Sube 150k al día. Revender en 5 días.
