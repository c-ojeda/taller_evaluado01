from fastapi import APIRouter

from app.pets.pets_schemas import CreatePetDto, Pet, UpdatePetDto
from app.pets.pets_service import pets_service
from app.shared.response import ApiResponse

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)

@router.get("")
def find_all(studentId: str) -> ApiResponse[list[Pet]]:
    data = pets_service.find_all_for_student(studentId)
    return ApiResponse.success_response(
        data=data,
        message="Mascotas obtenidas exitosamente"
    )

@router.post("", status_code=201)
def create(studentId: str, body: CreatePetDto) -> ApiResponse[Pet]:
    data = pets_service.create(studentId, body)
    return ApiResponse.success_response(
        data=data,
        message="Mascota creada exitosamente",
        status_code=201
    )

@router.patch("/{petId}")
def update(studentId: str, petId: str, body: UpdatePetDto) -> ApiResponse[Pet]:
    data = pets_service.update(studentId, petId, body)
    return ApiResponse.success_response(
        data=data,
        message="Mascota actualizada exitosamente"
    )

@router.delete("/{petId}")
def delete(studentId: str, petId: str) -> ApiResponse[Pet]:
    data = pets_service.delete(studentId, petId)
    return ApiResponse.success_response(
        data=data,
        message="Mascota eliminada exitosamente"
    )