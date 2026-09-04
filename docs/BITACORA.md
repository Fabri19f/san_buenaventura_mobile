# Bitácora de desarrollo

Registro cronológico de los hitos técnicos de la aplicación móvil del paciente
de la Clínica San Buenaventura. Las reglas y el alcance canónico permanecen en
`AGENTS.md`; esta bitácora documenta qué se hizo, por qué se hizo y cómo se
verificó.

## Estado de corte

- **Fecha:** 4 de septiembre de 2026.
- **Entrega actual:** barra de navegación funcional.
- **Destinos principales:** `Inicio`, `Citas` y `Perfil`.
- **Tecnologías:** Python 3.14, Flet 0.86.5 y uv.
- **Pruebas automatizadas:** 9 aprobadas.
- **Integraciones externas:** ninguna.

## Registro cronológico

### 1. Inicialización del proyecto

**Commit:** `b7ff558` — `chore: inicializa el proyecto móvil con Flet`

- Se configuró el proyecto Python con uv como único gestor de dependencias.
- Se declararon Flet y las herramientas necesarias para ejecución y pruebas.
- Se incorporaron los recursos gráficos iniciales de la aplicación.
- Se configuraron las exclusiones para entornos virtuales, cachés, artefactos de
  Flet y archivos locales del editor.
- Se fijó `src` como directorio de la aplicación.

### 2. Definición del alcance y de las reglas de desarrollo

**Commit:** `adaceb3` — `docs: define el alcance y las reglas de desarrollo`

- Se estableció `AGENTS.md` como fuente canónica de instrucciones.
- Se documentó que la aplicación está dirigida exclusivamente al paciente.
- Se limitó la entrega actual a una navegación funcional con tres destinos.
- Se excluyeron autenticación, consumo de API, formularios reales de citas,
  persistencia y funciones clínicas.
- Se definieron criterios de modularidad, orientación a objetos, tipado,
  pruebas, bajo acoplamiento y ausencia de sobreingeniería.
- Se añadieron skills especializadas para producto, Flet e integración futura
  con Laravel.

### 3. Configuración de Flet MCP

**Commit:** `61ea32f` — `chore: configura Flet MCP para los agentes`

- Se configuró Flet MCP para verificar controles, propiedades, eventos, enums,
  iconos y comandos antes de modificar código dependiente de Flet.
- Se habilitaron los grupos de ejemplos y CLI.
- Las configuraciones utilizan rutas relativas para que el repositorio no
  dependa del directorio personal de una estación de trabajo.
- La confianza local de Codex no se incluyó en la configuración compartida.

### 4. Implementación y refactorización de la navegación

**Commit:** `1c307c1` — `feat: implementa la navegación principal`

- `src/main.py` quedó como punto de composición y arranque.
- `AplicacionMovil` asumió la coordinación de la página, las vistas y la barra
  de navegación.
- `EstadoNavegacion` encapsuló el destino actual sin depender de Flet.
- `DestinoPrincipal` definió los únicos destinos válidos: `Inicio`, `Citas` y
  `Perfil`.
- `BarraNavegacion` encapsuló el control `NavigationBar`, sus elementos y la
  traducción de eventos de Flet a destinos de la aplicación.
- `VistaPrincipal` definió un contrato estructural mediante `Protocol`.
- `VistaInformativa` permitió reutilizar la presentación actual sin crear tres
  clases idénticas ni impedir que una vista sea sustituida cuando adquiera una
  responsabilidad propia.
- Se eliminó el punto de entrada raíz generado por plantilla para conservar un
  único arranque real en `src/main.py`.

La API utilizada fue contrastada con Flet MCP para Flet 0.86.5, incluyendo
`NavigationBar`, `NavigationBarDestination`, `SafeArea`, `Page`, `Event`,
alineaciones, iconos y `ft.run`.

### 5. Cobertura automatizada de la navegación

**Commit:** `a2c8360` — `test: cubre la navegación principal`

- Se separaron las pruebas del estado y de la coordinación de la aplicación.
- Se verificó que el destino inicial sea `Inicio`.
- Se probaron los cambios a `Inicio`, `Citas` y `Perfil`.
- Se comprobó la coherencia entre destino, índice seleccionado y contenido
  visible.
- Se verificó que la aplicación rechace un catálogo incompleto de vistas.
- Se evitó arrancar la interfaz completa para probar comportamiento que puede
  aislarse de forma determinista.

## Decisiones arquitectónicas vigentes

1. La única fuente de estado semántico es `EstadoNavegacion`; el índice de Flet
   es una representación visual administrada por `BarraNavegacion`.
2. La composición de dependencias es manual y explícita porque el tamaño actual
   no justifica un contenedor de inyección.
3. Las vistas actuales comparten una implementación informativa porque todavía
   no tienen comportamiento diferente. El contrato `VistaPrincipal` permite
   sustituirlas sin modificar el coordinador.
4. Flet se limita a presentación y estado de interfaz. Las futuras reglas de
   citas pertenecerán a Laravel.
5. No se crean capas, servicios, clientes o modelos hasta que exista una
   responsabilidad real que los necesite.

## Estructura actual relevante

```text
src/
├── main.py
├── app/
│   ├── aplicacion.py
│   └── navegacion.py
├── components/
│   └── barra_navegacion.py
└── views/
    └── vista_informativa.py

tests/
├── test_aplicacion.py
└── test_navegacion.py
```

## Verificación del estado de corte

Se ejecutaron satisfactoriamente:

```bash
uv sync
uv run pytest
uv run python -m compileall -q src tests
uv run flet run src/main.py
```

Resultado relevante de pruebas:

```text
9 passed
```

La aplicación inició sin excepciones y se comprobó que los tres destinos
actualizan el contenido y el estado seleccionado.

## Fuera del alcance actual

Hasta este corte no se implementaron:

- autenticación ni sesión del paciente;
- consumo de API Laravel;
- solicitud o cancelación real de citas;
- formularios y datos simulados;
- persistencia local u operación sin conexión;
- información clínica;
- edición del perfil.

Estas ausencias son decisiones de alcance, no trabajo incompleto de la entrega
actual.

## Plantilla para próximas entradas

```markdown
### N. Título del hito

**Fecha:** AAAA-MM-DD
**Commit:** `hash` — `tipo: descripción`

- Cambio realizado.
- Motivo de la decisión.
- Pruebas o verificaciones ejecutadas.
- Restricciones, riesgos o decisiones pendientes.
```
