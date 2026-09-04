---
name: clinica-mobile-flet
description: Convenciones técnicas de la app móvil Flet de la Clínica San Buenaventura — uv, Flet MCP, estructura del proyecto, navegación, estado y estilo de implementación. Úsala SIEMPRE antes de escribir o modificar código Python/Flet, crear controles, cambiar la navegación, añadir dependencias o ejecutar comandos del proyecto. Si vas a usar una propiedad, control, icono o comando de Flet, consulta esta skill y Flet MCP antes de inventarlo.
---

# Convenciones técnicas de la aplicación Flet

Aplicación móvil desarrollada con Python + Flet y dependencias administradas con
`uv`.

## Cómo usar esta skill

Etiquetas:

- **[CANON]** — restricción heredada del proyecto principal.
- **[DECISIÓN]** — decisión técnica ya tomada para esta app.
- **[PROPUESTA]** — supuesto de trabajo modificable.
- **[ABIERTO]** — no decidido. Pregunta antes de fijarlo.
- **Sin etiqueta** — detalle mecánico: elige la solución más simple.

## 1. Gestor de proyecto y dependencias [DECISIÓN]

Se usa **uv**.

No uses `pip`, `pipenv`, Poetry ni `requirements.txt` por iniciativa propia.

Comandos normales:

```bash
uv sync
uv add <paquete>
uv add --dev <paquete>
uv run flet --version
uv run flet run src/main.py
```

Cuando haga falta ejecutar Flet, prefiere `uv run flet ...` para usar exactamente
la versión declarada por el proyecto.

## 2. Flet MCP es la fuente técnica primaria [DECISIÓN]

Antes de escribir o modificar código que dependa de la API de Flet, **consulta
Flet MCP**.

Es obligatorio especialmente para:

- nombres de controles;
- propiedades;
- eventos;
- enums;
- iconos;
- navegación;
- temas;
- APIs móviles;
- almacenamiento;
- comandos CLI;
- APIs que puedan haber cambiado entre versiones.

Regla:

> No inventes una API de Flet de memoria si Flet MCP puede verificarla.

Si Flet MCP y el conocimiento previo del agente difieren, prevalece la API
reportada por Flet MCP para la versión instalada en el proyecto.

Si MCP no está disponible, verifica primero:

```bash
uv run flet --version
uv run flet mcp --help
```

y no introduzcas sintaxis dudosa en silencio.

## 3. Idioma y nombres [DECISIÓN]

La interfaz visible está en español.

Código propio de la app:

- clases propias: `PascalCase`;
- funciones, variables y módulos: `snake_case`;
- nombres descriptivos en español cuando representen conceptos del dominio:
  `cita`, `paciente`, `solicitar_cita`, `cancelar_cita`;
- nombres impuestos por Flet/Python permanecen como exige el framework.

No uses tildes ni `ñ` en identificadores de Python. Sí se usan en textos visibles.

## 4. Arquitectura de cliente [DECISIÓN]

Flet es **capa de presentación y cliente**, no capa de negocio.

La app puede:

- renderizar vistas;
- capturar eventos;
- validar formato básico de entrada;
- mantener estado de interfaz;
- llamar a servicios/clientes HTTP;
- presentar errores y resultados.

La app no puede:

- decidir disponibilidad real de una cita;
- detectar superposiciones como autoridad final;
- decidir si una cita puede cancelarse;
- fabricar identidad del paciente;
- saltarse autorización del backend.

Esas reglas pertenecen al sistema Laravel.

## 5. Estructura del proyecto [PROPUESTA]

Mantén la estructura pequeña y explícita:

```text
src/
  main.py
  views/
    inicio.py
    citas.py
    perfil.py
  components/
    navegacion.py
  services/
    api.py
  state/
    sesion.py
  models/
```

No crees carpetas vacías "por arquitectura". Añade `services`, `state` o `models`
solo cuando exista código real que colocar ahí.

Para la entrega actual de navegación, es aceptable mantener una implementación
más pequeña si separar archivos no aporta claridad.

## 6. Navegación principal [DECISIÓN]

La navegación persistente contiene exactamente:

```
Inicio
Citas
Perfil
```

Utiliza el control de navegación móvil vigente recomendado por Flet para la
versión instalada, validado mediante Flet MCP.

No agregues una cuarta pestaña para `Solicitar cita`: esa acción pertenece a la
vista `Citas`.

La selección de destino debe tener una única fuente de estado. Evita mantener un
índice en dos lugares distintos.

## 7. Estado [DECISIÓN]

Mantén el estado tan local como sea posible.

Orden de preferencia:

1. estado local de la vista;
2. estado compartido mínimo de sesión/navegación;
3. gestor de estado adicional solo si aparece una necesidad concreta.

No introduzcas Redux, BLoC, Riverpod, repositorios genéricos ni patrones traídos
de otros frameworks móviles.

Para tres pantallas y navegación, un estado simple es suficiente.

## 8. Asincronía y red [PROPUESTA]

Cuando se incorpore la API, las operaciones de red deben evitar bloquear la
interfaz.

Antes de elegir `async`, tareas o APIs específicas de Flet, consulta Flet MCP
para la versión instalada.

La interfaz debe distinguir como mínimo:

- cargando;
- éxito;
- error recuperable.

No conviertas errores HTTP en `print()` silenciosos.

## 9. Dependencias [DECISIÓN]

No agregues un paquete externo si Flet o la biblioteca estándar resuelven el caso
de forma razonable.

Antes de `uv add`:

1. explica qué necesidad concreta resuelve;
2. verifica que no exista ya una solución en Flet;
3. añade la dependencia mínima.

Evita librerías "por si acaso".

## 10. Diseño visual [PROPUESTA]

Prioriza una interfaz móvil clara y sobria, coherente con una aplicación de salud,
sin convertir la entrega académica en un ejercicio de diseño ornamental.

Para la barra actual:

- etiquetas visibles;
- iconos reconocibles;
- estado seleccionado evidente;
- áreas táctiles cómodas;
- contenido que demuestre inequívocamente el cambio de sección.

No gastes tiempo en animaciones, branding avanzado o temas complejos mientras la
materia solo evalúe navegación.

## 11. Calidad mínima

Antes de dar por terminada una modificación:

```bash
uv sync
uv run flet run src/main.py
```

Cuando corresponda, prueba también el objetivo móvil soportado por tu entorno.

Verifica:

- la app inicia sin excepciones;
- los tres destinos de navegación responden;
- no hay imports muertos;
- no hay controles o propiedades inventados;
- no hay dependencias innecesarias.

## 12. Criterio general

Prefiere código explícito y corto.

No construyas una "clean architecture" móvil completa para una app cuyo dominio
vive en Laravel. La separación importante es:

```
vista Flet → cliente/servicio HTTP → backend
```

Agrega más capas solo cuando una necesidad concreta lo justifique.
