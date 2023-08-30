from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dal.dal import Dal
from src.db.models.tables import Patient, Relative, Relationship, Document
from src.schemas.document import DocumentIn
from src.schemas.patient import PatientIn, PatientUpdate
from src.schemas.relative import RelativeIn
from src.utils.errors import ItemNotFoundError



class PatientDal(Dal[Patient]):
    model = Patient

    def get_patients(self) -> list[Patient] | None:
        filters = select(self.model)
        return self.fetch_all(filters)

    def get_patient_by_id(self, patient_id: int, options = None) -> Patient:
        patient = self.get_(patient_id, options=options)
        if patient is None:
            raise ItemNotFoundError

        return patient

    def create(self, schema: PatientIn) -> Patient:
        patient = Patient(**schema.dict())
        return self.add_orm(patient)

    #
    def update_patient_by_id(self, patient_id: int, data: PatientUpdate) -> Patient:
        filters = {'id': patient_id}
        patch = data.dict(exclude_unset=True)
        updated_patient = self.update(filters, patch)
        if updated_patient is None:
            raise ItemNotFoundError
        return updated_patient

    def delete_by_id(self, patient_id: int) -> None:
        patient = self.get_patient_by_id(patient_id, options = [
            joinedload(Patient.relative_association),
            joinedload(Patient.documents)
        ])
        for relation in patient.relative_association:
            self.delete_orm(relation)
        for documents in patient.documents:
            self.delete_orm(documents)
        self.delete_orm(patient)


    def create_relative(self, patient_id: int, relative_data: RelativeIn) -> (Relative, Relationship):
        patient = self.get_patient_by_id(patient_id)
        relation = Relationship(**relative_data.dict(include={"relationship_type"}))
        relative = Relative(**relative_data.dict(exclude={"relationship_type"}))
        relation.relative = relative
        patient.relative_association.append(relation)
        self.sess.flush()
        self.sess.refresh(relative)
        self.sess.refresh(relation)
        return relative, relation

    def get_patient_w_relationship_a_relative(self, patient_id: int) -> Patient:
        patient = self.get_patient_by_id(patient_id, options=[
            joinedload(Patient.relative_association).joinedload(Relationship.relative)])

        return patient


    def create_document(self, patient_id: int, document_data: DocumentIn) -> Document:
        patient = self.get_patient_by_id(patient_id)
        document = Document(**document_data.dict())
        patient.documents.append(document)
        self.sess.flush()
        self.sess.refresh(document)
        return document

    def get_patient_documents(self, patient_id: int) -> list[Document]:
        patient = self.get_patient_by_id(patient_id, options=[joinedload(Patient.documents)])
        print(patient.documents)
        return patient.documents



