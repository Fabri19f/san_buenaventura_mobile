---
name: clinica-mobile-integracion
description: Contrato arquitectónico entre la app Flet del paciente y el sistema Laravel de la Clínica San Buenaventura. Úsala SIEMPRE que trabajes en autenticación móvil, consumo HTTP, endpoints, DTOs, seguridad, solicitud/cancelación de citas o cualquier cambio que toque a la vez Flet y Laravel. Evita duplicar reglas de negocio y evita que la app móvil se convierta en dependencia del sistema principal.
---

# Integración Flet ↔ Laravel

La aplicación móvil es un cliente opcional del sistema principal.

## Cómo usar esta skill

Etiquetas:

- **[CANON]** — decisión que sostiene el proyecto de grado.
- **[DECISIÓN]** — decisión ya tomada y modificable con el autor.
- **[PROPUESTA]** — contrato provisional.
- **[ABIERTO]** — falta definir; pregunta antes de implementar.

## 1. Dirección de la dependencia [CANON]

La dependencia va en un solo sentido:

```
App Flet → API Laravel → servicios existentes → modelos/base de datos
```

Nunca:

```
Laravel → app Flet
```

El backend debe seguir funcionando aunque la aplicación móvil no exista.

## 2. Reutilización de lógica de negocio [CANON]

La lógica de negocio del sistema vive en la capa de servicios de Laravel.

Cuando la app móvil se integre, los controladores REST deben ser delgados e
invocar **los mismos servicios** que usa la interfaz web.

No dupliques en Python reglas como:

- disponibilidad de horarios;
- detección de superposiciones;
- propiedad de la cita;
- estados válidos;
- condiciones de cancelación;
- generación de identificadores;
- autorización.

Flet expresa intención. Laravel decide.

## 3. Alcance de la API móvil [CANON]

La API destinada al paciente solo necesita soportar el alcance móvil:

- autenticación del paciente;
- consultar sus citas;
- consultar disponibilidad necesaria para solicitar una cita;
- solicitar una cita;
- cancelar una cita;
- cerrar sesión;
- obtener los datos mínimos de perfil necesarios para la app.

No expongas endpoints de:

- expediente clínico;
- consultas;
- diagnósticos;
- antecedentes;
- prescripciones;
- bitácora;
- reportes;
- usuarios internos;
- permisos internos.

## 4. Autenticación [CANON]

El acceso del paciente se mantiene separado de la autenticación del personal
interno.

La arquitectura prevista usa **Laravel Sanctum con tokens y un mecanismo/guard
independiente para pacientes**.

No reutilices sin análisis el modelo `User` del personal interno para representar
al paciente.

### Modelo de cuenta del paciente [ABIERTO]

Aún no está fijado cómo se representa la credencial del paciente ni cómo se
relaciona con `pacientes`.

No inventes por tu cuenta:

- tabla de credenciales;
- contraseña dentro de `pacientes`;
- reutilización de `users`;
- OTP;
- login por documento;
- registro autónomo.

Resolver este punto antes de implementar autenticación real.

## 5. Propiedad y autorización [CANON]

Todo endpoint del paciente debe comprobar en Laravel que el recurso pertenece al
paciente autenticado.

Ejemplo conceptual:

```
token paciente A
    ↓
GET cita X
    ↓
Laravel comprueba cita.paciente_id == paciente A
    ↓
respuesta o 403/404
```

Filtrar la lista en Flet no es una medida de seguridad.

## 6. Contrato HTTP [PROPUESTA]

Cuando llegue la integración, versiona el contrato de la API desde el inicio.

Propuesta:

```text
/api/mobile/v1/...
```

No la conviertas en decisión sin confirmación del autor.

Mantén respuestas consistentes y orientadas a la app. No serialices modelos
Eloquent completos por comodidad.

[PROPUESTA] Para errores funcionales, devuelve códigos y mensajes suficientemente
estables para que Flet pueda presentar una explicación en español sin analizar
texto libre.

## 7. Datos de citas [CANON + PROPUESTA]

La app puede recibir únicamente los datos necesarios para que el paciente
comprenda y opere su cita, por ejemplo:

- identificador;
- fecha;
- hora;
- especialidad;
- profesional;
- estado;
- información necesaria para cancelarla.

La lista exacta del DTO es [ABIERTO] hasta diseñar el endpoint.

No incluyas datos clínicos porque "ya vienen en la relación" del modelo.

## 8. Solicitud de cita [CANON]

La app no crea una cita como hecho consumado sin validación del backend.

Flujo:

```
Paciente selecciona opción
        ↓
Flet envía solicitud
        ↓
Laravel valida disponibilidad y reglas
        ↓
Laravel crea/rechaza
        ↓
Flet muestra el resultado
```

La disponibilidad mostrada por la app puede quedar obsoleta entre consulta y
confirmación. Laravel siempre revalida al crear.

## 9. Cancelación [CANON]

Flet solicita la cancelación; Laravel decide si el estado actual permite efectuarla
y registra el cambio según las reglas del sistema.

No borres la cita.

La cita forma parte de la trazabilidad de agenda del sistema principal.

## 10. Reprogramación [CANON]

La app móvil actualmente **no incluye reprogramación**.

Aunque el backend interno la soporte, no expongas esa capacidad al paciente sin
una nueva decisión de alcance.

## 11. Errores y seguridad del cliente [DECISIÓN]

La app debe tratar explícitamente:

- sesión expirada;
- falta de conexión;
- respuesta no autorizada;
- conflicto de disponibilidad;
- error inesperado.

No registres tokens, contraseñas ni datos sensibles en consola.

### Persistencia del token [ABIERTO]

Antes de decidir cómo persistir el token en el dispositivo, consulta Flet MCP y
las capacidades actuales de la plataforma.

No guardes credenciales de larga duración en texto plano por comodidad.

## 12. Desarrollo desacoplado [DECISIÓN]

Mientras la asignatura móvil no exija integración real, no fuerces una API
incompleta únicamente para alimentar la interfaz.

Para entregas puramente visuales o de navegación:

- no hace falta backend;
- no hace falta mock de red;
- no hace falta autenticación falsa.

Si una entrega futura necesita datos antes de que la API exista, puede usarse un
adaptador simulado **explícitamente identificado como mock**, de modo que después
pueda sustituirse por el cliente HTTP sin reescribir las vistas.

## 13. Regla de cambio cruzado

Si una tarea móvil requiere modificar Laravel:

1. identifica el caso de uso de backend afectado;
2. revisa las skills `clinica-alcance`, `clinica-convenciones`,
   `clinica-integridad` y `clinica-modelo-datos`;
3. evita introducir un endpoint que salte la capa de servicios;
4. comprueba que el sistema principal siga siendo completo sin la app;
5. si toca un punto [CANON], informa el impacto antes de cambiarlo.
