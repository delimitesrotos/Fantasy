# Cápsula privada `ESTADO_FANTASY`

> Plantilla pública sin datos reales. El chat crea una copia dentro de la
> conversación; nunca escribe la copia completada en este repositorio.

La cápsula es el estado explícito y portátil. No es memoria oculta: aparece en
el chat después de cada cambio confirmado. Si se abre un chat nuevo, basta pegar
la última cápsula junto al enlace del repositorio.

```yaml
ESTADO_FANTASY:
  version: 1
  actualizado: UNKNOWN
  onboarding:
    reglas: pendiente
    equipo: pendiente
    clasificacion: pendiente
    rivales: parcial
  liga:
    sistema_puntuacion: UNKNOWN
    reglas_especiales: []
  usuario:
    saldo: UNKNOWN
    valor_equipo: UNKNOWN
    perfil: UNKNOWN
    intocables: []
    plantilla: []
  clasificacion: []
  rivales: []
  mercado_privado:
    fecha: UNKNOWN
    jugadores: []
  eventos_confirmados: []
  frescura:
    reglas: UNKNOWN
    equipo_saldo: UNKNOWN
    clasificacion: UNKNOWN
    rivales: UNKNOWN
    mercado: UNKNOWN
  siguiente_paso: reglas
```

## Reglas de actualización

- El chat enseña un resumen del cambio y pide confirmación.
- Solo una confirmación explícita modifica la cápsula.
- Los datos ambiguos permanecen `UNKNOWN`.
- La cápsula completa reaparece tras cada cambio, dentro de un bloque plegable
  si el chat lo permite.
- Al iniciar un chat sin cápsula, el onboarding comienza en `reglas`.

