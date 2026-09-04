# AGENTS.md

## Proyecto

Este repositorio contiene la aplicación móvil del paciente para la Clínica San
Buenaventura, desarrollada en **Apps Móviles II** con **Python + Flet** y
dependencias administradas con **uv**.

La aplicación móvil es un cliente complementario del sistema Laravel del proyecto
de grado. El sistema principal debe seguir siendo completo y defendible aunque
esta app no exista.

Este archivo es la **fuente canónica de instrucciones para agentes** dentro de
este repositorio. Las instrucciones específicas de proveedor deben remitirse a
este archivo y no duplicar sus reglas.

## Modelo de la aplicación

```text
Paciente
   ↓
Aplicación Flet
   ↓
API móvil Laravel
   ↓
Servicios de negocio existentes
   ↓
Base de datos institucional
```

Consecuencias:

- Flet presenta información y captura intención del paciente.
- Laravel conserva las reglas de negocio.
- La app no accede directamente a la base de datos.
- La app no replica reglas de agenda o autorización.
- El backend no debe depender de la existencia de esta app.

## Estado actual de la entrega

La entrega actual requiere **únicamente una barra de navegación funcional**.

Implementar exactamente estos destinos principales:

- `Inicio`
- `Citas`
- `Perfil`

Al pulsar cada destino:

- debe cambiar el contenido visible;
- debe reflejarse correctamente el destino seleccionado;
- la app no debe producir errores.

Por ahora **no implementar**:

- autenticación;
- consumo de API;
- formularios reales de citas;
- mocks de red innecesarios;
- persistencia de sesión;
- funcionalidades clínicas;
- arquitectura especulativa para entregas futuras.

No adelantar funcionalidades aunque parezcan fáciles.

## Actor de la aplicación

La aplicación móvil está dirigida exclusivamente al **paciente**.

No es una interfaz móvil para:

- médicos;
- enfermería;
- admisión;
- dirección médica;
- dirección general;
- administración.

Los roles del sistema interno pertenecen al sistema Laravel, no a esta app.

## Alcance móvil

El alcance funcional máximo actualmente comprometido es:

1. ver sus citas;
2. solicitar una cita;
3. cancelar una cita.

La app **nunca expone historia clínica**.

No agregar por iniciativa propia:

- diagnósticos;
- antecedentes;
- prescripciones;
- signos vitales;
- consultas anteriores;
- bitácora;
- reportes institucionales;
- gestión de usuarios internos;
- roles y permisos internos;
- cobros o facturación;
- exámenes complementarios;
- reprogramación de citas.

La reprogramación existe en el sistema interno, pero no forma parte del alcance
móvil actual.

## Navegación

La navegación principal tiene exactamente:

```text
Inicio
Citas
Perfil
```

Las acciones de citas viven dentro de `Citas`:

```text
Citas
├── Ver citas
├── Solicitar cita
└── Cancelar cita
```

`Solicitar cita` no es una cuarta pestaña principal.

## Ingeniería de software y calidad de código

El código debe desarrollarse como **software mantenible**, no como una demo de una
sola entrega. Aplicar buenas prácticas de Python, orientación a objetos,
modularidad, separación de responsabilidades, pruebas y diseño limpio.

### Principios obligatorios

- **Preferir diseño orientado a objetos** para vistas, componentes, servicios,
  clientes, modelos y objetos con estado o comportamiento propio.
- No concentrar toda la aplicación en `main.py`.
- `main.py` debe actuar como **punto de composición/arranque**, no como contenedor
  de todas las vistas, eventos, reglas y utilidades.
- Cada módulo y clase debe tener una responsabilidad clara.
- Aplicar **SRP** y, cuando aporte valor real, los demás principios SOLID.
- Favorecer **composición sobre herencia**.
- Evitar clases gigantes, funciones gigantes, módulos "util" sin cohesión y
  objetos que conozcan demasiado del resto del sistema.
- Mantener bajo acoplamiento y alta cohesión.
- Usar encapsulación: el estado interno de un objeto no debe modificarse desde
  cualquier lugar sin una interfaz clara.
- Usar nombres expresivos y tipos explícitos.
- Añadir **type hints** a funciones, métodos, atributos públicos y contratos
  relevantes.
- Evitar `Any` salvo necesidad justificada.
- Usar `dataclass`, `Enum`, `Protocol`, clases abstractas o value objects cuando
  representen mejor un concepto real; no por decoración.
- Mantener funciones pequeñas y previsibles.
- Preferir guard clauses a anidaciones profundas.
- No usar estado global mutable.
- Evitar efectos secundarios ocultos.
- No capturar excepciones con `except Exception` salvo frontera de aplicación
  donde exista una estrategia clara de manejo.
- No usar `print()` como mecanismo permanente de diagnóstico o manejo de errores.
- Documentar el **porqué** de decisiones no obvias; no comentar lo que el código
  ya expresa.
- Seguir las convenciones modernas de Python y PEP 8.

### Orientación a objetos sin sobreingeniería

La orientación a objetos es el estilo principal del proyecto, pero no se debe
convertir cada literal o función pura trivial en una clase artificial.

Crear objetos cuando exista:

- estado;
- identidad;
- comportamiento;
- una responsabilidad reusable;
- una frontera arquitectónica;
- un contrato que deba probarse o sustituirse.

Una función pura pequeña sigue siendo válida cuando sea más clara que una clase.
La meta es **diseño limpio y modular**, no maximizar el número de clases.

### Arquitectura

Separar responsabilidades por capas ligeras y explícitas:

```text
Presentación Flet
    ↓
Aplicación / servicios del cliente
    ↓
Infraestructura / cliente HTTP
    ↓
API Laravel
```

Los modelos/objetos de datos compartidos se mantienen independientes de las
vistas.

No introducir una Clean Architecture ceremonial con capas vacías, pero sí
preservar fronteras claras desde el inicio.

Como guía, cuando existan responsabilidades reales:

```text
src/
  main.py
  app/
    aplicacion.py
  views/
    inicio_view.py
    citas_view.py
    perfil_view.py
  components/
    barra_navegacion.py
  models/
  services/
  clients/
  state/
```

No crear directorios sin contenido real. La estructura debe crecer con el
producto, conservando esas fronteras.

### Vistas y componentes

- Una vista principal no debe implementar lógica de negocio.
- Los componentes reutilizables viven fuera de las vistas.
- Los callbacks de UI deben ser breves: delegan a métodos del objeto o servicios.
- Evitar lambdas extensas y callbacks anidados con lógica relevante.
- La navegación debe estar encapsulada, no repartida entre controles sin un dueño
  claro del estado.
- Las vistas deben poder modificarse sin tocar código no relacionado.

### Inyección de dependencias

Preferir pasar dependencias explícitamente a los objetos que las necesitan.

Ejemplo conceptual:

```text
Aplicacion
 ├── Navegador
 ├── ServicioCitas
 └── ClienteApi
```

Evitar singletons y service locators globales.

No añadir un contenedor de inyección de dependencias externo salvo necesidad
real; la composición manual es suficiente mientras el proyecto sea pequeño.

## Pruebas

Las pruebas son parte del desarrollo, no una tarea posterior.

### Principios

- Todo comportamiento no trivial debe poder probarse sin arrancar toda la app.
- Separar lógica y estado de los controles Flet para facilitar pruebas unitarias.
- No escribir tests que dependan innecesariamente de detalles internos.
- Probar comportamiento observable y contratos.
- Un test debe comprobar principalmente una razón de fallo.
- Nombres de test descriptivos.
- Estructura Arrange → Act → Assert cuando mejore la lectura.
- Evitar fixtures gigantes y estado compartido entre pruebas.
- Mantener pruebas deterministas, rápidas e independientes.
- No depender de red real en tests unitarios.
- Cuando aparezca el cliente HTTP, sustituirlo mediante dobles/fakes/mocks en la
  frontera correspondiente.
- No mockear clases internas sin necesidad: probar objetos reales cuando sean
  baratos y deterministas.
- Mantener la misma calidad de nombres, modularidad y tipado en tests que en
  producción.

### Organización sugerida

```text
tests/
  unit/
  integration/
```

Crear estas carpetas cuando existan ambos tipos de prueba. Mientras el proyecto
sea pequeño puede mantenerse una estructura más simple.

Las pruebas deben reflejar el diseño del código, no acumularse todas en
`test_main.py`.

### Entrega actual

Para la navegación, cubrir al menos el comportamiento separable que permita
verificar:

- destino inicial;
- cambio a `Inicio`;
- cambio a `Citas`;
- cambio a `Perfil`;
- índice/estado seleccionado coherente;
- tratamiento razonable de un destino inválido si el diseño lo admite.

No escribir tests artificiales de Flet que solo comprueben que una constante
existe. Probar comportamiento útil.

## Reglas técnicas

### Gestor de dependencias

Usar **uv**.

No usar por iniciativa propia:

- `pip`;
- Poetry;
- Pipenv;
- `requirements.txt`.

Comandos base:

```bash
uv sync
uv run flet --version
uv run flet run src/main.py
```

Usar las herramientas de calidad ya presentes en el proyecto. Si falta una
herramienta necesaria, justificarla antes de añadirla.

### Flet MCP

Antes de escribir o modificar código que dependa de la API de Flet, consultar
**Flet MCP**.

Usarlo especialmente para verificar:

- controles;
- propiedades;
- eventos;
- enums;
- iconos;
- navegación;
- temas;
- APIs móviles;
- almacenamiento;
- comandos CLI.

Regla:

> No inventar una API de Flet de memoria si Flet MCP puede verificarla.

Si Flet MCP contradice conocimiento previo del agente, prevalece la API reportada
por Flet MCP para la versión instalada en el proyecto.

### Idioma

Toda interfaz visible va en español.

En código propio:

- clases: `PascalCase`;
- funciones, variables y módulos: `snake_case`;
- conceptos de dominio en español;
- sin tildes ni `ñ` en identificadores.

Los nombres impuestos por Python y Flet permanecen como exige el framework.

## Arquitectura del cliente

Flet es capa de presentación y cliente.

La app puede:

- renderizar vistas;
- capturar eventos;
- validar formato básico;
- mantener estado de interfaz;
- llamar a servicios o clientes HTTP;
- presentar errores y resultados.

La app no puede decidir como autoridad final:

- disponibilidad real de una cita;
- superposiciones de agenda;
- si una cita puede cancelarse;
- propiedad de una cita;
- identidad institucional del paciente;
- permisos del paciente.

Esas reglas pertenecen a Laravel.

## Estado de interfaz

Mantener el estado tan local como sea posible.

Orden de preferencia:

1. estado local de la vista;
2. estado compartido mínimo;
3. una solución adicional solo si aparece una necesidad concreta.

No introducir gestores de estado ni arquitecturas tomadas de otros frameworks por
anticipación.

## Dependencias

No agregar un paquete externo si Flet o la biblioteca estándar resuelven el caso
de forma razonable.

Antes de `uv add`:

1. identificar la necesidad concreta;
2. verificar si Flet ya la cubre;
3. agregar únicamente la dependencia mínima necesaria.

## Integración futura con Laravel

La dependencia siempre va en este sentido:

```text
Flet → API Laravel → servicios existentes → modelos/base de datos
```

Nunca duplicar en Python reglas como:

- disponibilidad;
- detección de superposiciones;
- propiedad de una cita;
- estados válidos;
- condiciones de cancelación;
- autorización;
- generación de identificadores.

Cuando llegue la integración:

- los controladores REST de Laravel deben ser delgados;
- deben reutilizar los mismos servicios del sistema web;
- la autenticación del paciente debe permanecer separada del personal interno;
- el paciente solo puede operar sobre sus propios datos y citas.

## Skills del proyecto

Las skills son procedimientos especializados. Este archivo define cuándo
utilizarlas.

### `clinica-mobile-producto`

Leer antes de:

- crear una pantalla;
- crear un flujo;
- modificar navegación;
- añadir una funcionalidad;
- decidir si algo pertenece al alcance móvil.

### `clinica-mobile-flet`

Leer antes de:

- escribir o modificar Python/Flet;
- usar controles, propiedades, eventos o iconos;
- cambiar navegación;
- añadir dependencias;
- ejecutar comandos del proyecto.

Usar junto con **Flet MCP** cuando intervenga la API de Flet.

### `clinica-mobile-integracion`

Leer cuando la tarea incluya:

- autenticación;
- HTTP;
- API Laravel;
- Sanctum;
- endpoints;
- seguridad;
- solicitud real de citas;
- cancelación real;
- cambios coordinados entre Flet y Laravel.

### Selección de skills

```text
UI / navegación
→ clinica-mobile-producto
→ clinica-mobile-flet

Nueva funcionalidad
→ clinica-mobile-producto primero

Código o API Flet
→ clinica-mobile-flet
→ Flet MCP

Integración Flet ↔ Laravel
→ clinica-mobile-producto
→ clinica-mobile-flet
→ clinica-mobile-integracion
```

Usar el conjunto mínimo necesario. No cargar todas las skills por rutina.

## Forma de trabajar

Antes de modificar código:

1. inspeccionar la estructura existente;
2. leer las skills aplicables;
3. consultar Flet MCP si interviene Flet;
4. identificar responsabilidades y fronteras afectadas;
5. diseñar el cambio de forma modular;
6. identificar pruebas necesarias;
7. implementar el cambio mínimo correcto;
8. evitar reescrituras no relacionadas.

Después de modificar código:

1. revisar diseño, nombres y responsabilidades;
2. comprobar imports y dependencias innecesarias;
3. ejecutar tests;
4. ejecutar herramientas de calidad disponibles;
5. cuando el entorno lo permita, ejecutar la app;
6. comprobar específicamente la funcionalidad solicitada.

No dar por terminada una tarea únicamente porque "funciona visualmente" si la
implementación dejó deuda evidente como un `main.py` monolítico.

## Decisiones abiertas

No resolver por cuenta propia:

- modelo de credenciales o cuenta del paciente;
- mecanismo de inicio de sesión;
- entidad que almacenará las credenciales;
- datos editables del perfil;
- persistencia segura del token;
- contrato definitivo de la API móvil.

Cuando una tarea dependa de uno de estos puntos, preguntar antes de implementarlo.

## Criterio de prioridad

Ante conflicto, aplicar este orden:

1. instrucción explícita actual del usuario;
2. observación explícita del docente de Apps Móviles II;
3. alcance canónico del proyecto de grado;
4. decisiones registradas en las skills;
5. buenas prácticas de ingeniería de software y Python;
6. implementación mínima compatible con Flet actual.

Si una observación docente contradice el alcance canónico del proyecto de grado,
explicar brevemente el impacto y pedir confirmación antes de alterar ese alcance.
