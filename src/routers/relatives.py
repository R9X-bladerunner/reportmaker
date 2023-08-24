
from typing import Optional
from fastapi import APIRouter, Depends

from src.schemas.patient import PatientOutWithRelType
from src.schemas.relative import RelativeOut, RelativeIn
from src.serv.services import RelativeService

relative_router = APIRouter(prefix="/relatives", tags=["Relatives"])

@relative_router.get("", response_model=list[RelativeOut])
def get_relatives(service: RelativeService = Depends()):
    return service.get_relatives()


@relative_router.get("/{relative_id}", response_model=RelativeOut)
def get_relative(relative_id: int, service: RelativeService = Depends()):
    return service.get_relative_by_id(relative_id)


@relative_router.get("/{relative_id/patients}", response_model=list[PatientOutWithRelType])
def get_relative_patients(relative_id: int, service: RelativeService = Depends()):
    return service.get_relative_patients(relative_id)


# @relative_router.get("/{relative_id}")
# async def get_relative(
#         patient_id: int,
#         relative_id: int,
#         service: RelativeService = Depends()):
#     return None
#
# @relative_router.post("")
# async def create_relative(
#         patient_id: int,
#         relative: RelativeIn,
#         service: RelativeService = Depends(),
#         ):
#     pass


