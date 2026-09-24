# Scoring: Valor Marginal (Optimización de Cartera)

En LALIGA Fantasy, el dinero es finito y un equipo solo tiene 11 huecos que puntúan. Un jugador no es "bueno" o "malo" en el vacío; es bueno o malo en comparación con *a quién reemplaza* y *cuánto dinero inmoviliza*.

## La Fórmula Mental para el LLM

Cada vez que evalúes una recomendación de compra, aplica esta lógica de Valor Marginal:

`Valor Marginal = (Puntos_Esperados_Nuevo - Puntos_Esperados_Reemplazado) / Capital_Invertido`

### Cómo aplicarlo (Ejemplo Práctico)
Si el usuario quiere fichar a Vinícius por 25M, y su delantero actual es Hugo Duro (8M).
- ¿Cuántos puntos *extra* le va a dar Vinícius sobre Hugo Duro? (Ej. 4 puntos más de media).
- ¿Vale la pena gastar 17M de presupuesto (la diferencia) para conseguir 4 puntos extra? 
- Si con esos 17M podría fichar a 2 mediocentros top que en conjunto mejorarían a sus suplentes en 10 puntos, entonces **fichar a Vinícius tiene un coste de oportunidad altísimo y NO se recomienda**.

## Conceptos Derivados

1. **Liquidez Restante:** Jamás recomiendes pujar todo el cash si deja al usuario a 0. La falta de liquidez impide especular mañana.
2. **Capital Inmovilizado en Banquillo:** Los millones invertidos en suplentes no generan puntos. Fomenta vender suplentes caros y cambiarlos por parches baratos que aseguren jugar (1 punto) liberando cash.
