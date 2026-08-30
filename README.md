# CRUD Students & Pets (FastAPI)

Proyecto FastAPI que implementa un **CRUD en memoria** para la entidad `Student` y sus mascotas (`Pet`). No requiere base de datos ni contenedores: los datos viven en un diccionario dentro del servicio y se pierden al reiniciar la aplicación.

## Requerimientos

- Python 3.13+ (gestionado automáticamente por [uv](https://docs.astral.sh/uv/))
- uv

## Resumen funcional

La API expone operaciones CRUD completas:

- **Estudiantes** bajo `/api/students`:
    - **Crear**: `POST /api/students`
    - **Listar**: `GET /api/students`
    - **Buscar por id**: `GET /api/students/:id`
    - **Actualizar**: `PATCH /api/students/:id`
    - **Eliminar**: `DELETE /api/students/:id` (también elimina sus mascotas)
- **Mascotas** anidadas bajo `/api/students/:studentId/pets`:
    - **Listar**: `GET /api/students/:studentId/pets`
    - **Crear**: `POST /api/students/:studentId/pets`
    - **Actualizar**: `PATCH /api/students/:studentId/pets/:petId`
    - **Eliminar**: `DELETE /api/students/:studentId/pets/:petId`

Cada estudiante tiene `id` (UUID), `name`, `email`, `age`, `createdAt` y `updatedAt`. El `email` es único: se rechaza con `409 Conflict` si ya existe.

Cada mascota tiene `id` (UUID), `studentId`, `name`, `species`, `age` (opcional), `createdAt` y `updatedAt`. Solo puede operar sobre su estudiante dueño.

## Estándar de Respuestas API

Todas las respuestas de la API están estandarizadas para mantener una estructura consistente en caso de éxito o error.

### Respuesta Exitosa (`2xx`)

```json
{
  "success": true,
  "statusCode": 200,
  "data": { ... }
}

##Respuesta de Error (`4xx / 5xx`)

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Mensaje descriptivo del error",
  "route": "/api/v1/endpoint",
  "keys": ["campoAfectado"],
  "data": null
}