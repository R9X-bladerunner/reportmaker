from typing import List

from fastapi import Depends

from src.dal.patients import PatientDal
from src.db.models.tables import Patient
from src.dal.repositories import PatientRepository
from src.schemas.patient import PatientIn, PatientUpdate


class PatientService:
    def __init__(self, patient_dal: PatientDal = Depends()):
        self.dal = patient_dal

    def get_patients(self):
        return self.dal.get_patients()

    def get_patient_by_id(self, patient_id: int):
        return self.dal.get_patient_by_id(patient_id)

    def create_patient(self, patient: PatientIn):
        return self.dal.create(patient)

    def update_patient_by_id(self, patient_id: int, data: PatientUpdate):
        return self.dal.update_by_id(patient_id, data)

    def delete_patient(self, patient_id: int):
        pass




