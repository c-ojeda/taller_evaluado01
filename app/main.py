from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.pets.pets_controller import router as pets_router
from app.students.students_controller import router as students_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI CRUD Students & Pets",
        description="API de un CRUD en memoria para la entidad Student y sus mascotas (Pet)",
        version="1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware para envolver respuestas exitosas
    @app.middleware("http")
    async def response_wrapper_middleware(request: Request, call_next):
        response = await call_next(request)
        
        # Solo transformamos si no es una respuesta de error o streaming
        if response.headers.get("content-type") == "application/json" and 200 <= response.status_code < 300:
            import json
            body = [section async for section in response.body_iterator]
            original_data = json.loads(body[0].decode()) if body else None
            
            wrapped_body = {
                "success": True,
                "statusCode": response.status_code,
                "data": original_data
            }
            return JSONResponse(status_code=response.status_code, content=wrapped_body)

        return response

    # Manejador de errores HTTP (404, 400, etc.)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "statusCode": exc.status_code,
                "message": exc.detail if isinstance(exc.detail, str) else "Error procesando la solicitud",
                "route": request.url.path,
                "keys": getattr(exc, "headers", None) or [],
                "data": None,
            },
        )

    # Manejador de errores de validación (Pydantic)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        invalid_keys = [str(err["loc"][-1]) for err in exc.errors()]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "statusCode": 400,
                "message": "Validation Error",
                "route": request.url.path,
                "keys": invalid_keys,
                "data": None,
            },
        )

    app.include_router(students_router)
    app.include_router(pets_router)

    return app


app = create_app()