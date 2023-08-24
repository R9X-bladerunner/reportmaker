from fastapi import APIRouter, Depends

from src.schemas.document import DocumentOut, DocumentIn
from src.schemas.patient import PatientOutWithRelType
from src.schemas.relative import RelativeOut
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


@relative_router.post("/{relative_id}/documents", response_model=DocumentOut)
def create_relative_document(relative_id:int,
                    document_data: DocumentIn,
                    service: RelativeService=Depends()):
    return service.create_document(relative_id, document_data)
@relative_router.get("/{patient_id}/documents", response_model=list[DocumentOut])
def get_relative_documents(relative_id: int,
                          service: RelativeService=Depends()):

    return service.get_relative_documents(relative_id)





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


