from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    message: str
    data: Optional[T] = None

    @classmethod
    def success_response(cls, data: T = None, message: str = "Operación realizada con éxito", status_code: int = 200):
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data
        )

    @classmethod
    def error_response(cls, message: str = "Ocurrió un error", status_code: int = 400):
        return cls(
            success=False,
            statusCode=status_code,
            message=message,
            data=None
        )