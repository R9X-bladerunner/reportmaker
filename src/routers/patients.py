from typing import Union

from fastapi import APIRouter, Depends, status

from src.schemas.document import DocumentOut, DocumentIn
from src.schemas.patient import PatientIn, PatientOut, PatientUpdate
from src.schemas.relative import RelativeIn, RelativeOut
from src.serv.services import PatientService

patient_router = APIRouter(prefix="/patients", tags=["Patients"])


@patient_router.get("", response_model=list[PatientOut])
def get_patients(service: PatientService = Depends()):
    return service.get_patients()

@patient_router.get("/{patient_id}", response_model=Union[PatientOut, None])
def get_patient(patient_id: int, service: PatientService = Depends()):
    return service.get_patient_by_id(patient_id)

@patient_router.post("", response_model=PatientOut)
def create_patient(
        patient: PatientIn,
        service: PatientService = Depends(),
        ):
    return service.create_patient(patient)

@patient_router.patch("", response_model=Union[PatientOut, None])
def update_patient(
        patient_id: int,
        data: PatientUpdate,
        service: PatientService = Depends()
):
    return service.update_patient_by_id(patient_id, data)

@patient_router.delete("/{patient_id}")
def delete_patient(patient_id: int, service: PatientService=Depends()):
    return service.delete_patient(patient_id)

@patient_router.post("/{patient_id}/relatives", response_model=RelativeOut)
def create_relative(patient_id:int,
                    relative_data: RelativeIn,
                    service: PatientService=Depends()):
    return service.create_relative(patient_id, relative_data)

@patient_router.get("/{patient_id}/relatives", response_model=list[RelativeOut])
def get_patient_relatives(patient_id: int,
                          service: PatientService=Depends()):

    return service.get_patient_relatives(patient_id)

@patient_router.post("/{patient_id}/documents", response_model=DocumentOut)
def create_document(patient_id:int,
                    document_data: DocumentIn,
                    service: PatientService=Depends()):
    return service.create_document(patient_id, document_data)
@patient_router.get("/{patient_id}/documents", response_model=list[DocumentOut])
def get_patient_documents(patient_id: int,
                          service: PatientService=Depends()):

    return service.get_patient_documents(patient_id)

