# Taller Evaluado I - Estándar de Respuestas HTTP JSON
**Asignatura:** ICINF1108 - Desarrollo Backend  
**Institución:** Universidad Católica de Temuco  
**Framework Utilizado:** FastAPI (Rama: `estudiantes_icinf-fastapi`)

## Descripción del Proyecto
Este proyecto implementa un estándar de respuesta dinámico y unificado para el framework FastAPI mediante la modificación de los retornos de los controladores HTTP y la configuración de manejadores globales de excepciones. 
El objetivo es proporcionar un contrato único y predecible para el cliente, adaptando los campos visibles según la naturaleza de la respuesta (Éxito, Error o Vacío).

---

## Documentación del Estándar de Respuesta

### Campos del Contrato Global
El estándar cuenta con un total de **6 campos posibles**, divididos entre campos fijos y condicionales:

1. `success` (Boolean): **Siempre presente.** Determina si la operación fue correcta (`true`) o falló (`false`).
2. `statusCode` (Integer): **Siempre presente.** Código de estado HTTP de la respuesta.
3. `data` (Generic / Object / Null): **Siempre presente.** Carga útil con la información del recurso. Puede ser un objeto, una lista o `null`.
4. `message` (String): **Condicional.** Explicación legible del error. *Visible solo si `success === false`.*
5. `route` (String): **Condicional.** El endpoint o ruta HTTP que originó la petición. *Visible solo si `success === false`.*
6. `keys` (Array[String]): **Condicional.** Lista de atributos o llaves del recurso involucradas en la operación. *Visible solo si `data === null`.*

---

## Reglas de Lógica Dinámica (Visibilidad de Campos)

### 1. Operación Exitosa con Datos
*   **Condición:** `success === true` y `data !== null`.
*   **Comportamiento:** Se ocultan los campos de error (`route`, `message`) y se oculta `keys` porque el payload de `data` contiene la estructura completa.

```json
{
  "success": true,
  "statusCode": 201,
  "data": {
    "id": 101,
    "fileName": "report_2026.pdf",
    "fileType": "application/pdf",
    "sizeInBytes": 1048576
  }
}
```

### 2. Operación Fallida (Error)
*   **Condición:** `success === false` y `data === null`.
*   **Comportamiento:** Se activan `route` y `message` para diagnosticar la falla. Al ser `data` nulo, se incluye `keys` para indicar qué campos o atributos causaron el error o eran requeridos.

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Failed to create file: Invalid file format",
  "route": "/api/v1/files",
  "keys": ["fileName", "fileType"],
  "data": null
}
```

### 3. Operación Exitosa pero sin Datos
*   **Condición:** `success === true` y `data === null` *(Ej: Eliminación exitosa de un recurso / HTTP 200 o 204)*.
*   **Comportamiento:** Se ocultan `route` y `message` por ser una operación correcta. Sin embargo, al ser `data` nulo, se activa el campo `keys` para dejar constancia de la identidad del recurso afectado (ej. el `id` eliminado).

```json
{
  "success": true,
  "statusCode": 200,
  "keys": ["id"],
  "data": null
}
```
