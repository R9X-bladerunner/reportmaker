from fastapi import Path, Body

from src.db.tables.patients import Patient
from src.repositories.patients import PatientRepository
from src.schemas.patient import PatientIn
from src.schemas.relative import RelativeIn
from src.services.base import BaseService

class RelativeService(BaseService[PatientRepository, Patient]):
    repo_type = PatientRepository


    async def create_relative(self, patient_id: int, relative: RelativeIn):
        patient = repo.
        db_relative = Patient(**relative.dict(), is_patient=False)
        return {"pid": patient_id, "relative": relative}

