---
name: clinica-mobile-producto
description: Modelo funcional y alcance de la aplicación móvil del paciente para la Clínica San Buenaventura. Úsala SIEMPRE antes de crear una pantalla, flujo, destino de navegación, acción del paciente o funcionalidad nueva en la app Flet, y SIEMPRE que haya que decidir si algo pertenece o no a la app móvil. Es la fuente para saber qué puede hacer el paciente, qué no puede ver y cuál es el estado actual de la entrega.
---

# Modelo funcional de la aplicación móvil

Aplicación móvil complementaria del proyecto de la Clínica San Buenaventura,
desarrollada en Apps Móviles II con Flet.

La app pertenece a otra asignatura y **no es condición de completitud del sistema
de grado**. El sistema Laravel debe seguir siendo completo y defendible sin ella.

## Cómo usar esta skill

Cada regla lleva una etiqueta que indica cuánta libertad tienes con ella:

- **[CANON]** — proviene del alcance ya fijado del proyecto de grado. No se cambia
  en silencio porque puede romper la coherencia con el documento principal.
- **[DECISIÓN]** — el autor ya lo decidió para la aplicación móvil.
- **[PROPUESTA]** — supuesto de diseño útil pero todavía modificable.
- **[ABIERTO]** — no decidido. Pregunta antes de implementar.
- **Sin etiqueta** — detalle de implementación. Decide la opción más simple.

Si una observación de Apps Móviles II contradice un **[CANON]** del proyecto de
grado, no la rechaces: explica en pocas líneas qué alcance del proyecto principal
afecta y pide confirmación antes de implementarla.

## 1. Actor de la aplicación [CANON]

La aplicación móvil está dirigida **exclusivamente al paciente**.

No es una interfaz móvil para médicos, admisión, enfermería, dirección ni
administradores. Los seis roles del sistema interno pertenecen al sistema Laravel,
no a esta app.

La app nunca debe asumir que el paciente tiene permisos del personal interno.

## 2. Alcance funcional máximo [CANON]

El paciente puede:

1. **Ver sus citas.**
2. **Solicitar una cita.**
3. **Cancelar una cita.**

Ese es el alcance máximo comprometido actualmente.

No agregues por iniciativa propia:

- historia clínica;
- diagnósticos;
- prescripciones;
- antecedentes;
- signos vitales;
- resultados o exámenes;
- reportes institucionales;
- auditoría;
- administración de usuarios;
- roles y permisos internos;
- cobros o facturación;
- reprogramación de citas.

Si una nueva función no cabe claramente en `ver`, `solicitar` o `cancelar`
citas, pregunta antes de implementarla.

## 3. Información clínica [CANON]

**La aplicación móvil no expone la historia clínica.**

No existe una pantalla de expediente, consultas anteriores, diagnósticos,
prescripciones o antecedentes.

No "prepares" componentes, rutas, modelos ni endpoints para mostrar esa
información. Hacerlo introduciría alcance excluido aunque permanezca oculto.

## 4. Modelo de navegación [DECISIÓN]

La navegación principal de la app tiene tres destinos persistentes:

```
Inicio
Citas
Perfil
```

### Inicio

Pantalla de entrada del paciente.

[PROPUESTA] Cuando el proyecto avance puede mostrar información no clínica como
la próxima cita y accesos rápidos. No debe convertirse en un panel clínico.

### Citas

Es el núcleo funcional de la app.

Aquí viven, como flujos secundarios y no como nuevas pestañas principales:

- listado de citas;
- detalle de una cita;
- solicitud de cita;
- cancelación de cita.

**Solicitar cita no es una cuarta pestaña.** Es una acción dentro de `Citas`.

### Perfil

Contiene información de cuenta y sesión del paciente.

[ABIERTO] Todavía no está definido qué datos del perfil serán editables. No
inventes edición de datos personales antes de resolverlo.

## 5. Estado actual de la entrega [DECISIÓN]

La entrega inmediata de Apps Móviles II requiere **únicamente una barra de
navegación funcional**.

En este estado:

- implementar `Inicio`, `Citas` y `Perfil`;
- al pulsar cada destino debe cambiar la vista;
- el destino seleccionado debe reflejarse visualmente;
- no implementar autenticación;
- no consumir la API Laravel;
- no crear formularios reales de citas;
- no crear datos simulados innecesarios;
- no adelantar funcionalidades de futuras entregas.

La entrega se considera funcional si la navegación cambia de pantalla sin errores
y mantiene correctamente el estado del destino seleccionado.

Cuando la materia solicite una funcionalidad nueva, actualiza esta sección en vez
de dejar a los agentes adivinar cuál es el objetivo de la semana.

## 6. Modelo conceptual de la app [DECISIÓN]

La app se entiende como un **cliente móvil del sistema**, no como un segundo
sistema de negocio.

```
Paciente
   ↓
Aplicación Flet
   ↓
API móvil del sistema Laravel
   ↓
Mismos servicios de negocio del sistema principal
   ↓
Base de datos institucional
```

Consecuencias:

- Flet presenta información y captura intención del paciente.
- Laravel decide las reglas de negocio.
- La app no replica reglas de agenda.
- La app no accede directamente a la base de datos.
- La app no obliga al backend a conocer detalles de interfaz móvil.

## 7. Propiedad de los datos [CANON]

El paciente solo puede operar sobre **sus propios datos y sus propias citas**.

La interfaz puede ocultar acciones, pero la garantía real de propiedad debe
aplicarse en el backend. Nunca presentes una comprobación en Flet como control de
seguridad suficiente.

## 8. Operación en línea [CANON]

La operación sin conexión está excluida del proyecto.

No agregues:

- caché de operaciones pendientes;
- colas de sincronización;
- resolución de conflictos;
- base local replicada;
- modo offline.

Un estado de carga o una pantalla de error de conexión sí son parte normal de un
cliente en línea.

## 9. Regla de expansión

Antes de crear una nueva pantalla, comprueba:

1. ¿La usa el paciente?
2. ¿Pertenece a ver, solicitar o cancelar citas, o al manejo mínimo de su sesión?
3. ¿No expone información clínica?
4. ¿No introduce una regla de negocio que deba vivir en Laravel?

Si alguna respuesta es dudosa, pregunta antes de escribir código.
