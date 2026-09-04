# CLAUDE.md

Lee y cumple `AGENTS.md` antes de realizar cualquier tarea en este repositorio.

`AGENTS.md` es la **fuente canónica de instrucciones del proyecto** y contiene:

- contexto y modelo de la aplicación;
- alcance funcional;
- exclusiones;
- estado actual de la entrega;
- arquitectura Flet → Laravel;
- estándares de ingeniería de software;
- buenas prácticas modernas de Python;
- orientación a objetos y modularidad;
- estrategia de pruebas;
- uso de `uv`;
- obligación de consultar Flet MCP;
- selección de skills;
- decisiones abiertas;
- criterio de prioridad.

No dupliques ni contradigas esas reglas en este archivo.

## Reglas no negociables para Claude Code

No concentres la aplicación en un único `main.py`.

Antes de escribir código:

- identifica objetos, responsabilidades y fronteras;
- diseña una solución modular;
- aplica orientación a objetos donde exista estado, comportamiento o una
  responsabilidad propia;
- mantén `main.py` como punto de composición/arranque;
- separa vistas, componentes, servicios, modelos y clientes cuando tengan
  responsabilidades reales;
- usa type hints;
- favorece composición sobre herencia;
- evita estado global mutable;
- evita clases y funciones gigantes;
- evita abstracciones especulativas;
- preserva bajo acoplamiento y alta cohesión.

La exigencia de modularidad **no autoriza sobreingeniería**. No crees capas,
interfaces, factorías, repositorios o patrones sin una necesidad concreta.

Las pruebas reciben la misma atención arquitectónica que el código de producción:

- no acumular todo en `test_main.py`;
- probar comportamiento, no detalles triviales;
- mantener tests pequeños, deterministas e independientes;
- separar unitarios e integración cuando esa distinción exista;
- hacer que la lógica relevante pueda probarse sin levantar toda la interfaz;
- no depender de red real en pruebas unitarias.

Si una tarea aparentemente pequeña produce un archivo monolítico o acoplamiento
innecesario, refactoriza antes de considerarla terminada.

## Skills

Antes de implementar una tarea, carga únicamente las skills aplicables desde
`.claude/skills/`:

- `clinica-mobile-producto`
- `clinica-mobile-flet`
- `clinica-mobile-integracion`

Selección:

```text
UI / navegación
→ clinica-mobile-producto + clinica-mobile-flet

Nueva funcionalidad
→ clinica-mobile-producto primero

Código o API Flet
→ clinica-mobile-flet + Flet MCP

Integración Flet ↔ Laravel
→ las tres skills
```

Cuando intervenga Flet, consulta **Flet MCP** antes de asumir controles,
propiedades, eventos, enums, iconos o APIs.

No conviertas `CLAUDE.md` en una segunda fuente de verdad. Si una nueva regla es
general para todos los agentes, actualiza `AGENTS.md`. Si es un procedimiento
especializado, actualiza la skill correspondiente.

Si `CLAUDE.md` y `AGENTS.md` entraran en conflicto, prevalece `AGENTS.md`, salvo
una instrucción explícita actual del usuario.
