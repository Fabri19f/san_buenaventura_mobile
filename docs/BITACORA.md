# Bitácora de desarrollo

Registro cronológico de los hitos técnicos de la aplicación móvil del paciente
de la Clínica San Buenaventura. Las reglas y el alcance canónico permanecen en
`AGENTS.md`; esta bitácora documenta qué se hizo, por qué se hizo y cómo se
verificó.

## Estado de corte

- **Fecha:** 4 de septiembre de 2026.
- **Entrega actual:** prototipo visual con navegación principal y secundaria en
  pila.
- **Destinos principales:** `Inicio`, `Citas` y `Perfil`.
- **Pantallas secundarias:** `Solicitar cita` e `Información personal`.
- **Tecnologías:** Python 3.14, Flet 0.86.5 y uv.
- **Pruebas automatizadas:** 28 aprobadas.
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

### 6. Diseño visual de la pantalla Inicio

**Fecha:** 4 de septiembre de 2026

**Commit:** `c67b2fa` — `feat: diseña la pantalla de inicio`

- Se sustituyó la vista informativa de Inicio por una vista especializada.
- Se creó una cabecera institucional con una bienvenida neutral que no depende
  de autenticación ni inventa la identidad del paciente.
- Se añadió un espacio visual para la próxima cita sin fechas, profesionales o
  datos simulados.
- Se representaron las tres gestiones permitidas: ver, solicitar y cancelar
  citas. Las tarjetas todavía no registran eventos ni ejecutan acciones.
- Se incorporó un aviso de privacidad limitado a la gestión de citas.
- Se extrajeron la paleta visual y el componente reutilizable de acceso para
  mantener consistencia sin duplicar estilos.
- Se fijó un tema Material 3 claro y se armonizó la barra de navegación con la
  nueva identidad visual.
- Se añadió una prueba de composición para garantizar que Inicio utilice su
  vista especializada mientras Citas y Perfil mantienen el alcance anterior.
- Se verificó la API empleada con Flet MCP para Flet 0.86.5.

### 7. Diseño visual de Citas y Perfil

**Fecha:** 4 de septiembre de 2026

**Commit:** `00fccd6` — `feat: diseña las vistas de citas y perfil`

- Se reemplazaron las vistas informativas restantes por `VistaCitas` y
  `VistaPerfil`.
- Citas concentra visualmente la consulta, solicitud y cancelación de citas sin
  implementar formularios, reglas de negocio, datos simulados ni callbacks.
- Se incorporó un espacio neutral para mostrar citas cuando existan datos
  reales y un aviso de que las reglas serán validadas por la clínica.
- Perfil presenta la estructura de cuenta y sesión sin decidir campos editables,
  credenciales o mecanismos de autenticación.
- Se evitó mostrar información clínica y se hizo explícita esa restricción en la
  presentación de privacidad.
- Se extrajeron `EncabezadoSeccion`, `SeccionAccesos` y `TarjetaAviso` como
  componentes compartidos por las vistas.
- El contrato `VistaPrincipal` se trasladó a un módulo propio y se eliminó la
  vista genérica, que dejó de representar una responsabilidad real.
- Las pruebas de composición ahora verifican que los tres destinos utilicen sus
  respectivas vistas especializadas.
- Los controles e iconos empleados fueron contrastados con Flet MCP para Flet
  0.86.5.

### 8. Navegación móvil en pila y pantallas secundarias

**Fecha:** 4 de septiembre de 2026

**Commit:** `c7f95fe` — `feat: agrega navegacion movil en pila`

- Se adoptaron rutas de Flet y una pila de `View` para conservar las tres
  pestañas como raíces y presentar las tareas secundarias con retroceso nativo.
- `Citas` quedó como pantalla de consulta/listado. No se creó una segunda
  pantalla de “Consultar citas” que obligaría al paciente a realizar un toque
  adicional para llegar al contenido principal de la sección.
- `Solicitar cita` se diseñó como una pantalla secundaria con un proceso guiado
  de tres etapas. Permanece informativa: no consulta horarios ni envía datos.
- La cancelación no recibió una pantalla aislada. El flujo se iniciará desde el
  detalle de la cita elegida para evitar acciones sin contexto; hasta disponer
  de citas reales, la interfaz guía al paciente hacia el listado.
- `Información personal` se diseñó como pantalla secundaria de Perfil sin
  inventar campos editables, credenciales o datos del paciente.
- Los accesos rápidos de Inicio y las acciones habilitadas en cada raíz ahora
  delegan en un navegador mediante un contrato explícito.
- Se separaron la traducción de intenciones a rutas, el catálogo de rutas y la
  coordinación de la pila para que las vistas no dependan directamente de
  `Page`.
- Se añadieron pruebas de rutas, apilado, retroceso, composición y delegación de
  eventos de las tarjetas interactivas.
- Las rutas desconocidas se normalizan a la raíz segura más cercana en vez de
  dejar incoherentes la URL, el contenido y el destino seleccionado.
- La API de `View`, `AppBar`, rutas, retroceso, controles e iconos se contrastó
  con Flet MCP para Flet 0.86.5.

## Decisiones arquitectónicas vigentes

1. La única fuente de estado semántico es `EstadoNavegacion`; el índice de Flet
   es una representación visual administrada por `BarraNavegacion`.
2. La composición de dependencias es manual y explícita porque el tamaño actual
   no justifica un contenedor de inyección.
3. Las vistas principales y las pantallas secundarias tienen contratos
   estructurales separados; la aplicación coordina catálogos completos de ambos
   tipos sin conocer sus implementaciones concretas.
4. `NavegadorPila` traduce intenciones semánticas a rutas de Flet. Las vistas
   reciben ese contrato y no conocen ni modifican directamente `Page`.
5. `Citas` es la consulta principal. Solicitar requiere una pantalla propia y
   cancelar requerirá primero seleccionar una cita y abrir su detalle.
6. Flet se limita a presentación y estado de interfaz. Las futuras reglas de
   citas pertenecerán a Laravel.
7. No se crean capas, servicios, clientes o modelos hasta que exista una
   responsabilidad real que los necesite.

## Estructura actual relevante

```text
src/
├── main.py
├── tema.py
├── app/
│   ├── aplicacion.py
│   ├── navegacion.py
│   ├── navegador_pila.py
│   └── rutas.py
├── components/
│   ├── barra_navegacion.py
│   ├── encabezado_seccion.py
│   ├── seccion_accesos.py
│   ├── tarjeta_acceso.py
│   └── tarjeta_aviso.py
└── views/
    ├── citas.py
    ├── contratos.py
    ├── informacion_personal.py
    ├── inicio.py
    ├── perfil.py
    └── solicitar_cita.py

tests/
├── test_aplicacion.py
├── test_componentes.py
├── test_composicion.py
├── test_navegacion.py
└── test_rutas.py
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
28 passed
```

La aplicación inició sin excepciones. Las pruebas comprueban que los tres
destinos actualizan el contenido y el estado seleccionado, que las rutas
secundarias se apilan sobre la raíz correcta y que el retroceso restaura la ruta
anterior.

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
