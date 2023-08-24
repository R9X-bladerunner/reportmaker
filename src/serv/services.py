from typing import List

from fastapi import Depends

from src.dal.patients import PatientDal
from src.dal.relationships import RelationshipDal
from src.dal.relatives import RelativeDal
from src.db.models.tables import Patient, Relative, Document
from src.schemas.document import DocumentIn
from src.schemas.patient import PatientIn, PatientUpdate, PatientOutWithRelType
from src.schemas.relative import RelativeIn, RelativeOut




class PatientService:
    def __init__(self, patient_dal: PatientDal = Depends()):
        self.dal = patient_dal

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

        relative, relation = self.dal.create_relative(patient_id, relative_data)
        return RelativeOut(
            relationship_type = relation.relationship_type,
            **vars(relative))

    def get_patient_relatives(self, patient_id: int) -> list[RelativeOut]:
        patient = self.dal.get_patient_w_relationship_a_relative(patient_id)

        return [RelativeOut(
            relationship_type = ra.relationship_type,
            **vars(ra.relative)
        ) for ra in patient.relative_association]


    def create_document(self, patient_id: int,
                        document_data: DocumentIn):
        return self.dal.create_document(patient_id, document_data)

    def get_patient_documents(self, patient_id: int) -> list[Document]:
        documents = self.dal.get_patient_documents(patient_id)
        return documents


class RelativeService:
    def __init__(self, relative_dal: RelativeDal = Depends()):
        self.dal = relative_dal

    def get_relatives(self) -> list[Relative]:
        return self.dal.get_relatives()

    def get_relative_by_id(self, relative_id: int) -> Relative:
        return self.dal.get_relative_by_id(relative_id)


    def get_relative_patients(self, relative_id: int) -> list[PatientOutWithRelType]:
        relative = self.dal.get_relative_w_relationship_a_patient(relative_id)
        return [PatientOutWithRelType(
            relative_to_patient_as=ra.relationship_type,
            **vars(ra.patient)
        ) for ra in relative.relative_association]



    # def get_patient_relatives(self, patient_id: int) -> list[RelativeOut]:
    #     patient = self.dal.get_patient_w_relationship_a_relative(patient_id)
    #
    #     return [RelativeOut(
    #         relationship_type=ra.relationship_type,
    #         **vars(ra.relative)
    #     ) for ra in patient.relative_association]




    def delete_relative(self, relative_id: int) -> None:
        return self.dal.delete_by_id(relative_id)

