from datetime import date

from pydantic import Field

from src.schemas.base import ApiModel

from strenum import StrEnum

class DocType(StrEnum):
    passport = 'passport'
    birth_cert_new  = 'birth_cert'
    birth_cert_old = 'birth_cert_old'

class DocumentId(ApiModel):
    id: int

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