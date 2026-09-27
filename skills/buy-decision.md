# Skill: Decisión de Compra

**Cuándo usar:** el usuario pregunta si debe fichar a un jugador concreto.

## Resolución del valor

Aplica estrictamente:

```text
dato explícito del usuario en su app
> snapshot canónico fresco
> fuente canónica abierta y verificada
> UNKNOWN
```

No existe un quinto nivel con «otra web». Ignora snippets y valores de Comunio,
Biwenger, Mister, Futmondo u otras plataformas.

## Workflow

1. Lee saldo, reglas y plantilla del estado conversacional.
2. Consulta primero `data/public/latest/metadata.json` y los snapshots frescos.
3. Comprueba titularidad, lesión, sanción y rotación; la búsqueda web aquí aporta
   contexto, no un precio exacto sustituto.
4. Determina a quién reemplaza y calcula el valor marginal.
5. Para rendimiento, limita normalmente la puja a VM +10–15 % según necesidad.
   Para trading, nunca superes VM + subida razonable hasta el próximo partido.

## Salida

Separa **HECHO**, **ESTIMACIÓN** y **ANÁLISIS**, y termina con decisión clara,
precio máximo, jugador al que mejora y riesgo. Si VM es `UNKNOWN`, no fabriques
un límite exacto: solicita el valor que muestra la app.
