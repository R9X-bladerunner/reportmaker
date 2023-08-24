from typing import Union

from fastapi import APIRouter, Depends

from src.schemas.document import DocumentOut, DocumentUpdate
from src.schemas.patient import PatientOut
from src.schemas.relative import RelativeOut
from src.services.services import DocumentService

document_router = APIRouter(prefix="/documents", tags=["Documents"])

@document_router.get("", response_model=list[DocumentOut])
def get_documents(service: DocumentService = Depends()):
    return service.get_documents()


@document_router.get("/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, service: DocumentService = Depends()):
    return service.get_document_by_id(document_id)


@document_router.patch("/{document_id}", response_model=DocumentOut)
def update_document(document_id: int,
                    data: DocumentUpdate,
                    service: DocumentService = Depends()):
    return service.update_document_by_id(document_id, data)

@document_router.get("/{document_id}/owner", response_model=Union[PatientOut, RelativeOut])
def get_owner(document_id: int, service: DocumentService = Depends()):
    return service.get_owner(document_id)


@document_router.delete("/{document_id}", response_model=None)
def delete_document(document_id: int, service: DocumentService = Depends()):
    return service.delete_document(document_id)