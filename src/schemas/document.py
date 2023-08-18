from datetime import date

from pydantic import Field

from src.schemas.base import ApiModel

from strenum import StrEnum

class DocType(StrEnum):
    passport = 'passport'
    birth_certificate_new  = 'birth_certificate_new'
    birth_certificate_old = 'birth_certificate_old'

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