# LALIGA Fantasy Decision Assistant

**Documento de implementación independiente · Handoff técnico**

## 0. Propósito del documento

Este documento define un proyecto completamente independiente para ayudar a un usuario de LALIGA Fantasy a tomar mejores decisiones desde el móvil utilizando un LLM como interfaz conversacional, datos públicos y un conjunto de skills/procedimientos especializados.

El sistema NO debe asociarse, integrarse ni compartir infraestructura, repositorios, dominios, nombres, secretos, pipelines o dependencias con ningún otro proyecto existente.

El objetivo NO es automatizar el juego. El objetivo es aumentar la calidad del análisis y la toma de decisiones manteniendo al humano como único ejecutor de cualquier acción dentro de LALIGA Fantasy.

## 1. Objetivo del producto

Crear un "cerebro de decisión" para LALIGA Fantasy que permita al usuario hacer preguntas naturales desde el móvil, por ejemplo:

- "Analiza este mercado" + captura.
- "¿Comprarías a este jugador por 8,4 M?"
- "¿Venderías ahora o esperarías?"
- "Tengo 11,2 M y esta plantilla. ¿Qué harías?"
- "Prepara mi jornada."
- "¿Qué tres decisiones tienen más impacto hoy?"
- "¿Esta operación mejora mi equipo o solo mi patrimonio?"

El sistema debe responder con recomendaciones razonadas, límites de precio, riesgos, alternativas y contexto, pero nunca realizar acciones en la cuenta.

## 2. Principios no negociables

1. **Cuenta real aislada del código.**
   - No solicitar usuario, contraseña, token, cookie, refresh token ni credenciales de LALIGA.
   - No reutilizar sesiones del navegador.
   - No llamar a APIs privadas/no documentadas de LALIGA desde la implementación final.

2. **Human-in-the-loop absoluto.**
   - El usuario compra, vende, puja, clausula y alinea exclusivamente desde la aplicación/web oficial.
   - El sistema solo analiza y recomienda.

3. **Mobile-first.**
   - La interfaz principal debe poder ser un chat móvil.
   - Las capturas de pantalla son una entrada válida y prioritaria.

4. **Sin servidor ni dominio en la primera versión.**
   - El sistema debe ser viable con un repo privado + LLM/chat.
   - La infraestructura adicional solo se justifica si aparece una necesidad concreta.

5. **Separar método, datos y modelo.**
   - El método de análisis vive en skills/workflows.
   - Los cálculos reproducibles deben separarse del razonamiento libre del LLM.
   - El modelo de lenguaje es intercambiable.

6. **Trazabilidad.**
   - Toda recomendación debería poder explicar qué factores pesaron a favor y en contra.

## 3. Cuenta secundaria: decisión

### 3.1 No usar una identidad inventada

No se recomienda crear una identidad falsa. Las condiciones de uso de LALIGA exigen información de registro veraz y el control del correo utilizado.

### 3.2 Cuenta secundaria legítima: uso permitido dentro del proyecto

Una cuenta secundaria legítima puede ser útil SOLO como entorno de laboratorio del desarrollador:

- estudiar cambios de autenticación;
- validar estructuras de respuestas;
- comprender modelos de datos;
- comprobar si un repo de terceros sigue funcionando;
- probar adaptadores en una liga de pruebas separada.

### 3.3 Lo que NO resuelve

Una cuenta secundaria no convierte una API privada en oficial ni elimina el riesgo técnico/regulatorio de automatización. Tampoco aporta información sobre el mercado, presupuesto o rivales de la liga real salvo que se introduzca en esa liga, lo que deja de ser un entorno aislado.

**Conclusión:** útil para I+D del desarrollador; irrelevante para la experiencia final del usuario. No debe ser dependencia del producto.

## 4. Repositorios analizados y qué aprovechar

### 4.1 jonortega20/fantasybot

Referencia:
https://github.com/jonortega20/fantasybot

Qué aporta:
- lectura de plantilla, mercado, alineación y rivales;
- tendencias externas;
- `flip` para oportunidades de reventa;
- `optimize` para once;
- `needs` para carencias;
- `rivals` para contexto competitivo;
- `history` para P&L / ROI;
- `scout` para análisis de jugadores;
- arquitectura separada por sources / strategy / state / agent;
- salida JSON para consumo programático.

Qué NO copiar:
- autenticación OAuth contra la API no oficial;
- almacenamiento/refresh de tokens;
- pujas, ventas, clausulazos, lineup apply;
- cron de acciones;
- ejecución autónoma;
- cualquier funcionalidad que toque la cuenta real.

Qué sí reutilizar conceptualmente:
- taxonomía de workflows;
- separación sources/strategy/state;
- idea de `flip`, `needs`, `optimize`, `scout`;
- trazabilidad de decisiones;
- formato estructurado/JSON.

### 4.2 sergioalmela/la-liga-fantasy-analyzer

Referencia:
https://github.com/sergioalmela/la-liga-fantasy-analyzer

Relevancia:
- actualizado para temporada 2026/27;
- plantillas, mercado, jornada y rivales;
- tendencias por snapshots;
- estimación de valor;
- recomendación de formación y once;
- análisis de carencias;
- radar de actividad/presupuesto;
- validación runtime de respuestas;
- arquitectura moderna Next.js/TypeScript.

Qué aprovechar:
- modelos de datos 2026/27;
- estructura de entidades;
- validaciones;
- lógica conceptual de tendencia;
- recomendación de formación;
- análisis de carencias;
- forma de separar servicios/adaptadores.

Qué NO copiar:
- login ROPC/OAuth;
- proxy hacia API privada;
- cookies de sesión;
- publicar plantilla;
- aplicar once;
- aceptar/rechazar ofertas;
- vigilancia/ejecución de cláusulas.

### 4.3 Externoak/LaLigaApp

Referencia:
https://github.com/Externoak/LaLigaApp

Qué aporta:
- referencia actual de OAuth y modelos;
- mercado, tendencias y onces probables;
- UI útil para estudiar experiencia;
- integración con datos externos.

Uso recomendado:
- referencia de ingeniería/documentación no oficial;
- no usar como cliente final ni conectar la cuenta real.

### 4.4 carlosgeos/laligafantasy

Referencia:
https://github.com/carlosgeos/laligafantasy

Qué aporta:
- histórico de puntos/precios;
- dashboards e insights;
- ideas de optimización matemática;
- valor por rendimiento;
- restricciones de alineación.

Qué aprovechar:
- formulación del problema de optimización;
- selección de XI como problema de restricciones;
- métricas de eficiencia de capital.

Qué NO copiar:
- autenticación con USERNAME/PASSWORD;
- acceso directo a API privada.

### 4.5 Luperbal/Mercado-Liga-Fantasy

Referencia:
https://github.com/Luperbal/Mercado-Liga-Fantasy

Qué aporta:
- scraping de datos públicos de FutbolFantasy;
- ranking de subidas de valor;
- exportación JSON;
- idea simple y útil de pipeline datos -> ranking -> LLM.

Qué aprovechar:
- concepto de momentum;
- formato JSON intermedio;
- separación entre extracción y explicación.

Precaución:
- respetar términos/robots/rate limits de las fuentes;
- preferir acceso público documentado cuando exista.

### 4.6 kiet08hogit/LaLiga-Fantasy

Referencia:
https://github.com/kiet08hogit/LaLiga-Fantasy

Qué aporta:
- analytics;
- predicciones ML;
- construcción de equipos;
- frontend/backend estructurado.

Uso recomendado:
- inspiración para features y visualización;
- no tomar sus datos históricos como representativos de la temporada actual sin validación.

### 4.7 Condiciones de LALIGA Fantasy

Referencia:
https://www.laliga.com/informacion-legal/condiciones-de-uso-fantasy

La implementación debe asumir que:
- las APIs privadas/no documentadas pueden cambiar;
- automatizaciones agresivas pueden entrar en conflicto con las condiciones;
- el diseño final debe evitar actuar sobre la cuenta.

## 5. Arquitectura recomendada: dos flujos

# FLUJO A — SIMPLE / VALIDACIÓN

## 5.1 Objetivo

Validar que las skills y el método realmente mejoran decisiones antes de construir pipelines de datos o infraestructura.

## 5.2 Arquitectura

Usuario móvil
    ↓
Chat / LLM
    ↓
Repo privado de conocimiento
    ├── SKILL.md
    ├── workflows/
    ├── scoring/
    ├── strategy/
    └── sources/
    ↓
Búsqueda web pública + capturas del usuario
    ↓
Recomendación
    ↓
Usuario ejecuta manualmente en app oficial

## 5.3 Entrada de datos privados

Solo mediante:
- capturas de mercado;
- capturas de plantilla;
- texto pegado por el usuario;
- presupuesto indicado manualmente;
- reglas particulares indicadas por el usuario.

Nunca mediante autenticación programática.

## 5.4 Interfaz

Preferida:
- ChatGPT/Gemini/Claude u otro LLM con visión y web.

Alternativa robusta:
- compilar el repo a un único `FANTASY_CONTEXT.md` que el usuario pueda adjuntar/importar cuando el conector GitHub no esté disponible.

## 5.5 Ventajas

- casi cero infraestructura;
- UX inmediata;
- muy fácil de iterar;
- permite descubrir qué métricas son útiles;
- minimiza riesgo;
- portable entre LLMs.

## 5.6 Limitaciones

- estado de plantilla/presupuesto no siempre persistente;
- dependencia de capacidades del chat;
- datos públicos recuperados bajo demanda;
- los cálculos pueden ser menos reproducibles si todavía viven solo como instrucciones.

# FLUJO B — ELABORADO / MOTOR DE DATOS

## 5.7 Objetivo

Mantener la misma UX conversacional, pero precalcular datos y scores de forma reproducible sin conectar la cuenta LALIGA.

## 5.8 Arquitectura

Fuentes públicas
    ↓
GitHub Actions / jobs programados
    ↓
extractores + normalización
    ↓
data/latest.json + históricos
    ↓
motor de scoring
    ↓
repo privado
    ↓
LLM/chat
    ↑
capturas del usuario
    ↓
recomendación contextual

## 5.9 Qué automatizar

Sí:
- recopilar fuentes públicas;
- normalizar nombres;
- calcular tendencias;
- calcular scores;
- generar snapshots;
- tests de calidad;
- compilar contexto para LLM.

No:
- login a LALIGA;
- lectura de cuenta privada;
- pujas;
- ventas;
- alineaciones;
- cláusulas;
- scraping agresivo;
- tareas cada minuto para actuar sobre el juego.

## 5.10 Por qué GitHub Actions antes que servidor

- suficiente para jobs diarios/horarios;
- sin servidor permanente;
- fácil de auditar;
- histórico versionado;
- coste potencialmente cero/bajo;
- mantiene el proyecto autocontenido.

Un servidor/dominio solo se considerará si aparecen necesidades como:
- estado multiusuario;
- persistencia más cómoda;
- API propia;
- notificaciones;
- interfaz específica;
- consultas de baja latencia a datos propios.

## 6. Estructura del repo a implementar

Nombre genérico sugerido:
`laliga-fantasy-decision-assistant`

Estructura:

```text
laliga-fantasy-decision-assistant/
├── README.md
├── SKILL.md
├── AGENT_HANDOFF.md
│
├── skills/
│   ├── market-analysis.md
│   ├── player-scout.md
│   ├── buy-decision.md
│   ├── sell-decision.md
│   ├── lineup.md
│   ├── squad-needs.md
│   ├── investment.md
│   └── daily-manager.md
│
├── scoring/
│   ├── fantasy_score.md
│   ├── investment_score.md
│   ├── fixture_score.md
│   ├── risk_score.md
│   └── opportunity_score.md
│
├── strategy/
│   ├── principles.md
│   ├── portfolio.md
│   ├── risk_profiles.md
│   └── decision_rules.md
│
├── sources/
│   ├── sources.md
│   ├── source_policy.md
│   └── field_mapping.md
│
├── schemas/
│   ├── player.schema.json
│   ├── squad.schema.json
│   ├── market.schema.json
│   └── recommendation.schema.json
│
├── data/
│   ├── latest/
│   ├── historical/
│   └── fixtures/
│
├── scripts/
│   ├── normalize_players.py
│   ├── calculate_scores.py
│   ├── build_context.py
│   └── validate_data.py
│
├── tests/
│   ├── test_scoring.py
│   ├── test_normalization.py
│   └── fixtures/
│
└── .github/
    └── workflows/
        ├── update-public-data.yml
        └── validate.yml
```

En Fase 1, `data/`, `scripts/` y GitHub Actions pueden existir vacíos o mínimos. El repo debe permitir crecer hacia Fase 2 sin reorganización drástica.

## 7. Diseño del SKILL.md

El `SKILL.md` debe ser el punto de entrada obligatorio.

Debe instruir al LLM para:

1. Identificar la intención:
   - mercado;
   - compra;
   - venta;
   - jugador;
   - plantilla;
   - jornada;
   - inversión;
   - decisión global.

2. Identificar información disponible y ausente.

3. Extraer datos de capturas sin inventar valores no visibles.

4. Buscar únicamente fuentes públicas.

5. Ejecutar el workflow correspondiente.

6. Separar:
   - rendimiento deportivo;
   - rendimiento financiero;
   - riesgo;
   - coste de oportunidad.

7. Expresar incertidumbre explícitamente.

8. Entregar una decisión accionable y breve primero; explicación después.

## 8. Skills / workflows requeridos

### 8.1 market-analysis

Input:
- captura/lista del mercado;
- presupuesto;
- plantilla si está disponible.

Output:
- top oportunidades;
- jugadores a evitar;
- tipo: rendimiento / trading / híbrido;
- precio actual;
- puja objetivo;
- puja máxima;
- horizonte;
- riesgo;
- motivo principal.

### 8.2 player-scout

Evaluar:
- puntos;
- media;
- minutos;
- titularidad;
- rol;
- lesiones;
- sanciones;
- forma;
- próximos rivales;
- valor;
- tendencia;
- competencia por posición;
- sensibilidad a rotaciones.

### 8.3 buy-decision

Pregunta central:
"¿Este jugador mejora el uso de mi capital frente a no comprar o frente a otra alternativa?"

Debe considerar:
- mejora marginal del XI;
- coste de oportunidad;
- liquidez restante;
- tendencia de precio;
- horizonte;
- necesidad posicional.

### 8.4 sell-decision

Debe distinguir:
- vender por deterioro deportivo;
- vender por techo de revalorización;
- vender para liberar capital;
- vender por lesión/sanción;
- mantener pese a caída de corto plazo.

### 8.5 lineup

Debe optimizar:
- formación válida;
- probabilidad de titularidad;
- minutos esperados;
- puntos esperados;
- dificultad del rival;
- riesgo de cero;
- dudas/rotaciones.

### 8.6 squad-needs

Clasificar posiciones en:
- fuerte;
- suficiente;
- mejorable;
- urgente.

Considerar sustitución marginal: no recomendar un fichaje solo porque sea bueno; debe mejorar al jugador al que desplaza.

### 8.7 investment

Separar:
- cash generation;
- preservación de valor;
- activo de corto plazo;
- activo de rendimiento;
- híbrido.

### 8.8 daily-manager

Workflow de mayor valor.

Pregunta:
"¿Qué tres acciones tienen mayor impacto hoy?"

Debe combinar:
- mercado;
- plantilla;
- presupuesto;
- próxima jornada;
- oportunidades;
- riesgos.

Output máximo:
1. acción;
2. importe/umbral;
3. razón;
4. alternativa;
5. condición que haría cambiar la recomendación.

## 9. Modelo de scoring

IMPORTANTE: comenzar con fórmulas simples y versionables. No fingir precisión científica.

### 9.1 Fantasy Score

Variables candidatas:
- puntos por partido ajustados;
- minutos esperados;
- probabilidad de titularidad;
- forma reciente;
- rival;
- rol ofensivo/defensivo;
- balón parado;
- disponibilidad.

Ejemplo conceptual:

`FantasyScore = rendimiento_base × disponibilidad × minutos × fixture_modifier × form_modifier`

No fijar pesos definitivos hasta disponer de backtests.

### 9.2 Investment Score

Variables:
- variación 1d;
- variación 7d;
- aceleración;
- precio;
- liquidez/coste;
- sostenibilidad de subida;
- catalizadores;
- riesgo de corrección.

### 9.3 Risk Score

Variables:
- lesión;
- sanción;
- rotación;
- baja titularidad;
- volatilidad;
- calendario;
- dependencia de eventos poco repetibles.

### 9.4 Opportunity Score

Combina valor deportivo + valor financiero - riesgo - coste de oportunidad.

Los pesos deben depender de un perfil:
- conservador;
- equilibrado;
- agresivo.

### 9.5 Regla crítica

El LLM NO debe tratar los scores como hechos objetivos. Son herramientas de comparación sujetas a sus datos y pesos.

## 10. Optimización de cartera

El sistema debe pensar en plantilla como cartera limitada por capital.

Preguntas necesarias:
- ¿Qué puntos marginales compra cada millón?
- ¿Cuánto capital queda inmovilizado?
- ¿Comprar A impide comprar B+C?
- ¿La operación mejora XI o solo banquillo?
- ¿Existe alternativa barata con 80-90% del rendimiento?

Métrica sugerida:

`MarginalValue = (ExpectedPoints_new - ExpectedPoints_replaced) / NetCapitalRequired`

Esto es más útil que comparar jugadores aislados.

## 11. Fuentes de datos

Prioridad:

1. fuentes oficiales públicas;
2. fuentes especializadas públicas con reputación;
3. múltiples fuentes para datos inciertos;
4. captura/texto del usuario para información privada de su liga.

Tipos de datos:
- calendario;
- resultados;
- lesiones;
- sanciones;
- minutos;
- estadísticas;
- probabilidad de titularidad;
- onces probables;
- valores;
- tendencias;
- noticias del club.

Mantener `sources/source_policy.md` con:
- URL;
- qué campos aporta;
- frecuencia;
- fiabilidad;
- limitaciones;
- método permitido de acceso;
- fallback.

## 12. Interfaz recomendada

### Fase 1: chat móvil

Es la interfaz prioritaria.

Razones:
- ya soporta voz;
- imágenes;
- seguimiento conversacional;
- preguntas abiertas;
- contraargumentos;
- refinamiento.

Ejemplos UX:

**Mercado**
Usuario: captura + "Analiza el mercado."
Respuesta:
- 3 mejores oportunidades;
- precio máximo;
- riesgo;
- por qué.

**Jugador**
Usuario: "¿Pagarías 8,7 M por X?"
Respuesta:
- Sí / No / Solo bajo condición;
- máximo;
- alternativa.

**Jornada**
Usuario: plantilla + "Prepara jornada."
Respuesta:
- XI;
- cambios;
- dudas;
- riesgos.

### Fase 2: seguir usando chat

Incluso si el backend de datos crece, mantener chat como interfaz principal salvo que aparezca una necesidad clara de dashboard.

### Posible interfaz futura

Una PWA solo si se desea:
- ver rankings visuales;
- estado persistente;
- botones predefinidos;
- notificaciones.

No construirla antes de validar que aporta más que el chat.

## 13. Estado del usuario

En Fase 1, evitar base de datos.

Opciones, por orden:
1. el usuario aporta captura cuando cambia algo;
2. un archivo `user_state.md` actualizado manualmente;
3. contexto persistente del LLM si es fiable y configurable;
4. base de datos solo si la fricción lo justifica.

Campos útiles:
- presupuesto;
- plantilla;
- sistema de puntuación;
- objetivo;
- perfil de riesgo;
- jugadores protegidos/no vendibles;
- horizonte.

No almacenar credenciales de LALIGA.

## 14. Privacidad y seguridad

- Repo privado.
- Sin secretos de LALIGA.
- Sin credenciales en archivos.
- `.env` solo para fuentes/API opcionales ajenas al juego.
- Logs sin datos sensibles.
- No almacenar capturas salvo necesidad explícita.
- Si se añaden Actions, usar secrets de GitHub solo para servicios externos permitidos.
- Revisar licencias antes de copiar código de repos terceros.
- Preferir reimplementación conceptual sobre copiar módulos enteros.

## 15. Qué NO implementar

El agente encargado debe rechazar de diseño:

- login a cuenta real de LALIGA;
- cookies/session hijacking;
- tokens OAuth del usuario;
- reverse engineering necesario para operar la cuenta final;
- auto-bid;
- auto-sell;
- auto-lineup;
- auto-clause;
- cron de acciones sobre la cuenta;
- pujas de último segundo;
- vigilancia activa de cláusulas conectada a la cuenta;
- bypass de rate limits;
- mecanismos anti-detección;
- cuentas falsas como solución de producción.

## 16. Plan de implementación

### Fase 0 — Investigación

- revisar licencias de repos de referencia;
- mapear ideas reutilizables;
- definir fuentes públicas;
- definir esquema `Player`;
- decidir sistema de puntuación objetivo.

Entrega:
- `AGENT_HANDOFF.md`;
- `sources.md`;
- `schemas/player.schema.json`.

### Fase 1 — Skill-first

Construir:
- `README.md`;
- `SKILL.md`;
- 8 skills;
- scoring conceptual;
- casos de prueba manuales.

No código de scraping obligatorio.

Validar con escenarios:
1. analizar mercado;
2. decidir compra;
3. decidir venta;
4. preparar jornada;
5. optimizar presupuesto.

### Fase 2 — Scoring reproducible

Implementar scripts:
- normalización;
- scoring;
- validación;
- compilador de contexto.

Añadir tests.

### Fase 3 — Datos públicos automáticos

Solo si merece la pena:
- jobs de GitHub Actions;
- snapshots diarios;
- histórico;
- build de `data/latest.json`.

### Fase 4 — Backtesting

Guardar decisiones y resultados para medir:
- acierto de titularidad;
- error en puntos esperados;
- ROI de inversión;
- valor de pujas recomendadas;
- mejora marginal del XI.

Ajustar pesos basándose en resultados, no intuición.

### Fase 5 — UX opcional

Solo entonces evaluar:
- PWA;
- dashboard;
- notificaciones;
- backend.

## 17. Criterios de aceptación de V1

La V1 está lista cuando:

1. Un LLM puede leer `SKILL.md` y seleccionar workflow correcto.
2. Una captura de mercado produce una lista priorizada.
3. Cada compra incluye:
   - precio objetivo;
   - máximo;
   - uso (rendimiento/trading/híbrido);
   - riesgo;
   - alternativa.
4. Una captura de plantilla permite detectar necesidades.
5. La jornada produce XI razonado.
6. Ninguna función necesita credenciales LALIGA.
7. No existe código de escritura hacia LALIGA.
8. El usuario puede entender la recomendación en menos de 30 segundos.
9. El modelo puede explicar por qué cambiaría de opinión.
10. El sistema distingue hechos, estimaciones e incertidumbre.

## 18. Formato de respuesta recomendado al usuario

Primero la decisión, después el análisis.

Ejemplo:

**DECISIÓN**
Comprar a X hasta 8,6 M.

**POR QUÉ**
- Mejora clara sobre tu actual MC.
- Titularidad alta.
- Próximos dos rivales favorables.
- Tendencia de precio positiva.

**RIESGO**
Rotación moderada entre semana.

**NO SUPERAR**
9,1 M. A partir de ahí el coste de oportunidad deja de compensar.

**ALTERNATIVA**
Y si se mantiene por debajo de 6,3 M.

**CAMBIARÍA DE OPINIÓN SI**
X no aparece en el once probable o se confirma una molestia.

## 19. Principios de implementación para el agente

- No sobrearquitectar Fase 1.
- Mantener componentes desacoplados.
- Todo score debe ser testeable.
- Todo dato debe conocer su fuente y timestamp.
- No mezclar "precio" con "calidad deportiva".
- No recomendar por nombre/reputación.
- Comparar siempre contra alternativa y jugador reemplazado.
- No inventar disponibilidad, titularidad o presupuesto.
- Si falta información crítica, presentar escenarios.
- Mantener la salida móvil breve.
- Guardar profundidad para cuando el usuario pregunte "por qué".

## 20. Decisión final de arquitectura

### Recomendación inicial

**Repo privado + skills + chat móvil.**

Sin:
- dominio;
- servidor;
- PWA;
- agente autónomo;
- conexión a cuenta LALIGA.

### Evolución recomendada

Si el método demuestra valor:

**Repo privado + jobs de datos públicos + scoring determinista + chat móvil.**

El chat sigue siendo la interfaz. GitHub actúa como fuente de verdad y motor de actualización. Solo añadir infraestructura adicional cuando exista una limitación concreta.

## 21. Referencias

1. fantasybot — jonortega20  
   https://github.com/jonortega20/fantasybot

2. LALIGA Fantasy Analyzer — sergioalmela  
   https://github.com/sergioalmela/la-liga-fantasy-analyzer

3. LaLigaApp — Externoak  
   https://github.com/Externoak/LaLigaApp

4. LaLiga Fantasy Companion Tool — carlosgeos  
   https://github.com/carlosgeos/laligafantasy

5. Mercado-Liga-Fantasy — Luperbal  
   https://github.com/Luperbal/Mercado-Liga-Fantasy

6. LaLiga-Fantasy analytics/ML — kiet08hogit  
   https://github.com/kiet08hogit/LaLiga-Fantasy

7. Condiciones de uso de LALIGA Fantasy  
   https://www.laliga.com/informacion-legal/condiciones-de-uso-fantasy

## 22. Instrucción final al agente implementador

Implementa este proyecto como un sistema completamente independiente.

No busques, abras, modifiques, reutilices ni enlaces repositorios del propietario que no sean el nuevo repositorio creado expresamente para este proyecto.

No asumas acceso a ninguna infraestructura previa.

Comienza por Fase 0 y Fase 1. No construyas servidor, dominio, PWA ni conexión con LALIGA salvo que una fase posterior los justifique explícitamente.

El objetivo principal de la primera versión no es automatizar más: es tomar mejores decisiones de forma reproducible, explicable y segura.
