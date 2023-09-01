from datetime import date
from pydantic import validator

from src.schemas.base import ApiModel, IdModel, DocType, Validators


class DocumentId(IdModel):
    pass


class DocumentBase(ApiModel):
    document_type: DocType
    series: str
    number: str
    issue_date: date
    issuing_authority: str


class DocumentIn(DocumentBase):

    _date_validator = validator(
        'issue_date',
        allow_reuse=True)(Validators.validate_date)

    _series_validator = validator(
        'series',
        allow_reuse=True)(Validators.validate_document_series)

    _number_validator = validator(
        'number',
        allow_reuse=True)(Validators.validate_document_number)


class DocumentOut(DocumentBase, DocumentId):
    pass

class DocumentUpdate(ApiModel):
    document_type: DocType | None = None
    series: str | None = None
    number: str | None = None
    issue_date: date | None = None
    issuing_authority: str | None = None

    _date_validator = validator(
        'issue_date',
        allow_reuse=True)(Validators.validate_date)

    _series_validator = validator(
        'series',
        allow_reuse=True)(Validators.validate_document_series)

    _number_validator = validator(
        'number',
        allow_reuse=True)(Validators.validate_document_number)
