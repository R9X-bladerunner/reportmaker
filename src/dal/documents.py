from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dal.dal import Dal
from src.db.models.tables import Document, Patient, Relative
from src.schemas.document import DocumentUpdate
from src.utils.errors import ItemNotFoundError


class DocumentDal(Dal[Document]):
    model = Document

    def get_documents(self) -> list[Document] | None:
        filters = select(self.model)
        return self.fetch_all(filters)

    def get_document_by_id(self, document_id: int, options = None) -> Document:
        document = self.get_(document_id, options=options)
        if document is None:
            raise ItemNotFoundError

        return document
    def update_document_by_id(self, document_id: int, data: DocumentUpdate) -> Document:
        filters = {'id': document_id}
        patch = data.dict(exclude_unset=True)
        updated_document = self.update(filters, patch)
        if updated_document is None:
            raise ItemNotFoundError  # Посмотреть что должно возвращаться по соглашению
        return self.update(filters, patch)

    def delete_document(self, document_id: int) -> None:
        document = self.get_document_by_id(document_id)
        self.delete_orm(document)


    def get_owner(self, document_id: int) -> Patient | Relative:
        document = self.get_document_by_id(document_id, options=[
            joinedload(Document.patient),
            joinedload(Document.relative)
        ])

        if document.patient:
            return document.patient
        if document.relative:
            return document.relative

