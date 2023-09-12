from fastapi import APIRouter, Depends, status

from src.schemas.document import DocumentOut, DocumentIn
from src.schemas.patient import PatientOutWithRelType
from src.schemas.relative import RelativeOut, RelativeUpdate
from src.services.services import RelativeService

relative_router = APIRouter(prefix="/relatives", tags=["Relatives"])

@relative_router.get("", response_model=list[RelativeOut])
def get_relatives(service: RelativeService = Depends()):
    return service.get_relatives()


@relative_router.get("/{relative_id}", response_model=RelativeOut)
def get_relative(relative_id: int, service: RelativeService = Depends()):
    return service.get_relative_by_id(relative_id)


@relative_router.get("/{relative_id}/patients", response_model=list[PatientOutWithRelType])
def get_relative_patients(relative_id: int, service: RelativeService = Depends()):
    return service.get_relative_patients(relative_id)


@relative_router.post("/{relative_id}/documents",
                      response_model=DocumentOut,
                      status_code=status.HTTP_201_CREATED
                      )
def create_relative_document(relative_id:int,
                    document_data: DocumentIn,
                    service: RelativeService=Depends()):
    return service.create_document(relative_id, document_data)
@relative_router.get("/{relative_id}/documents", response_model=list[DocumentOut])
def get_relative_documents(relative_id: int,
                          service: RelativeService=Depends()):

    return service.get_relative_documents(relative_id)


@relative_router.patch("/{relative_id}",
                       response_model=RelativeOut,
                       response_model_exclude_unset=True,
                       status_code=status.HTTP_200_OK)
def update_relative(relative_id: int, patch: RelativeUpdate,
                    service: RelativeService=Depends()):

    return service.update_relative_by_id(relative_id, patch)

@relative_router.delete("/{relative_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_relative(relative_id: int, service: RelativeService=Depends()):

    return service.delete_relative_by_id(relative_id)
