from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    data: T | None = None


class ApiErrorResponse(BaseModel):
    success: bool = False
    statusCode: int
    message: str
    route: str
    keys: list[str] | None = None
    data: None = None