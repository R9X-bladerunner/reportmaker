from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dal.dal import Dal
from src.db.models.tables import Relative, Relationship, Document
from src.schemas.document import DocumentIn
from src.schemas.relative import RelativeUpdate
from src.utils.errors import ItemNotFoundError


class RelativeDal(Dal[Relative]):
    model = Relative

    def get_relatives(self) -> list[Relative] | None:   #check None
        filters = select(self.model)
        return self.fetch_all(filters)

    def get_relative_by_id(self, relative_id: int, options = None) -> Relative:
        relative = self.get_(relative_id, options=options)
        if relative is None:
            raise ItemNotFoundError
        return relative

    def get_relative_w_relationship_a_patient(self, relative_id: int):
        relative = self.get_relative_by_id(relative_id, options=[
            joinedload(Relative.relative_association).joinedload(Relationship.patient)])

        return relative

    def create_document(self, relative_id: int, document_data: DocumentIn) -> Document:
        relative = self.get_relative_by_id(relative_id)
        document = Document(**document_data.dict())
        relative.documents.append(document)
        self.sess.flush()
        self.sess.refresh(document)
        return document

    def get_relative_documents(self, patient_id: int) -> list[Document]:
        relative = self.get_relative_by_id(patient_id, options=[joinedload(Relative.documents)])
        print(relative.documents)
        return relative.documents

    def delete_by_id(self, relative_id: int) -> None:
        relative = self.get_relative_by_id(relative_id, options = [
            joinedload(Relative.relative_association),
            joinedload(Relative.documents)
        ])
        for relation in relative.relative_association:
            self.delete_orm(relation)
        for documents in relative.documents:
            self.delete_orm(documents)
        self.delete_orm(relative)


