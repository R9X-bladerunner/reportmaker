from datetime import date

from strenum import StrEnum

from src.schemas.base import ApiModel, IdModel


class DocType(StrEnum):
    passport = 'passport'
    birth_cert_new  = 'birth_cert'
    birth_cert_old = 'birth_cert_old'

class DocumentId(IdModel):
    pass


class DocumentBase(ApiModel):
    series: str
    number: str
    document_type: DocType
    issue_date: date
    issuing_authority: str


class DocumentIn(DocumentBase):
    pass

class DocumentOut(DocumentBase, DocumentId):
    pass

class DocumentUpdate(ApiModel):
    series: str | None = None
    number: str | None = None
    document_type: DocType | None = None
    issue_date: date | None = None
    issuing_authority: str | None = None
