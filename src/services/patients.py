from src.db.tables.patients import Patient
from src.repositories.patients import PatientRepository
from src.schemas.patient import PatientIn
from src.services.base import BaseService



class PatientService(BaseService[PatientRepository, Patient]):
    repo_type = PatientRepository

    async def create_patient(self, patient: PatientIn):
        return await self.base_create(patient.dict())

    async def get_patients(self):
        return await self.base_fetch_all()

    async def get_patient_by_id(self, patient_id: int):
        return await self.base_fetch_one(patient_id)
