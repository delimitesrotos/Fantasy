# Plantilla de estado privado del usuario

> No introduzcas datos reales en este repositorio público. Usa la copia privada
> en el Drive del jugador descrita en `data/private_drive_state.md`; no dependas
> de la memoria del chat.

- **Sistema de puntuación:** `[Mixto / Sofascore / Picas / otro]`
- **Saldo disponible:** `[ejemplo ficticio: 12,5 M€]`
- **Valor de equipo:** `[opcional]`
- **Reglas especiales:** `[límites, primas, clausulazos]`
- **Perfil:** `[conservador / agresivo]`
- **Plantilla:**
  - `[POR ficticio]`
  - `[DEF ficticio]`
- **Intocables:** `[jugadores ficticios]`
- **Rivales conocidos:** `[opcional]`
- **Última reconciliación completa:** `[fecha]`

## Eventos incrementales

El chat debe mostrar el cambio propuesto, pedir confirmación y después actualizar
la hoja privada sin solicitar una captura completa tras cada operación:

```text
BUY <player_id o nombre inequívoco> <precio>
SELL <player_id o nombre inequívoco> <precio>
CASH <nuevo saldo confirmado>
LINEUP <lista de player_id>
```

Ejemplo ficticio: `BUY futbolfantasy:999999 8000000` añade el jugador, descuenta
8 M€ y registra el movimiento. Si identidad, precio o saldo son ambiguos, el
chat pregunta solo por el dato mínimo que falta.
