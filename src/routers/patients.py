from typing import Union

from fastapi import APIRouter, Depends

from src.schemas.patient import PatientIn, PatientOut, PatientUpdate
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
def delete_patient(patient_id: int, service: PatientService =Depends()):
    return service.delete_patient(patient_id)