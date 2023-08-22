from typing import List

from fastapi import Depends

from src.dal.patients import PatientDal
from src.dal.relationships import RelationshipDal
from src.db.models.tables import Patient, Relative
from src.schemas.patient import PatientIn, PatientUpdate
from src.schemas.relative import RelativeIn, RelativeOut




class PatientService:
    def __init__(self, patient_dal: PatientDal = Depends(), relationship_dal: RelationshipDal = Depends()):
        self.dal = patient_dal
        self.rel_dal = relationship_dal

    def get_patients(self):
        return self.dal.get_patients()

    def get_patient_by_id(self, patient_id: int):
        return self.dal.get_patient_by_id(patient_id)

    def create_patient(self, patient: PatientIn):
        return self.dal.create(patient)

    def update_patient_by_id(self, patient_id: int, data: PatientUpdate) -> Patient | None:
        return self.dal.update_by_id(patient_id, data)

    def delete_patient(self, patient_id: int) -> None:
        return self.dal.delete_by_id(patient_id)

    def create_relative(self, patient_id: int,
                        relative_data: RelativeIn) -> RelativeOut:

        relative = self.dal.create_relative(patient_id, relative_data)
        relation = self.rel_dal.get_relation(patient_id, relative.id)
        relative_out = RelativeOut(
            id=relative.id,
            last_name=relative.last_name,
            first_name=relative.first_name,
            middle_name=relative.middle_name,
            birthday=relative.birthday,
            gender=relative.gender,
            snils=relative.snils,
            relationship_type=relation.relationship_type)
        return relative_out

    def get_patient_relatives(self, patient_id: int):
        return self.dal.get_relatives(patient_id)





