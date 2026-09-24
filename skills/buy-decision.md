# Skill: Decisión de Compra (Buy Decision)

**Cuándo usar:** El usuario pregunta explícitamente si debería fichar a un jugador en concreto (Ej: "¿Pujarías por X jugador por 8 millones?").

## Workflow de Decisión

1. **Lectura del Estado:** Verifica en `data/user_state.md` cuánto saldo tiene el usuario. 
2. **Chequeo del Jugador (Contexto Público):** 
   - Busca si el jugador es titular fijo, está sancionado o tiene riesgo de rotar.
   - Revisa si su valor de mercado está subiendo o bajando.
3. **Análisis de Valor Marginal (La Regla de Oro):**
   - ¿A quién sentaría este jugador en el 11 titular actual del usuario?
   - ¿Cuántos puntos extra va a dar respecto al jugador que va al banquillo?
   - ¿Justifica ese incremento de puntos gastar esa cantidad de millones?
4. **Cálculo de Límite de Puja:**
   - Si es para **rendimiento**, el límite es Precio de Mercado + 10% a 15% (dependiendo de la necesidad posicional).
   - Si es para **trading/especular**, NUNCA pujar más del Precio de Mercado + lo que subirá en 3 días.

## Formato de Respuesta
1. **DECISIÓN CLARA:** (Ej: "Sí, pero solo hasta 8.2M" / "No, déjalo pasar").
2. **MOTIVO:** Explicación matemática y deportiva.
3. **A QUIÉN MEJORA:** El jugador de tu plantilla que debe ir al banquillo o ser vendido.
4. **RIESGO:** Nivel de riesgo (rotaciones, histórico de lesiones).
