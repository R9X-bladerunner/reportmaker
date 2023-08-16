from fastapi import APIRouter, Depends, Path

from src.schemas.patient import PatientIn, PatientOut
from src.services.patients import PatientService

patient_router = APIRouter(prefix="/patients", tags=["Patients"])

@patient_router.get("", response_model=list[PatientOut])
async def get_patients(service: PatientService = Depends()):
    return await service.get_patients()

@patient_router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(
        patient_id: int = Path(gt=0),
        service: PatientService = Depends()
):
    return await service.get_patient_by_id(patient_id)

@patient_router.post("", response_model=PatientOut)
async def create_patient(
        patient: PatientIn,
        service: PatientService = Depends(),
        ):
    return await service.create_patient(patient)

