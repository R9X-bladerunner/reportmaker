import random
import uuid

import pytest

from src.dal.patients import PatientDal
from src.dal.relatives import RelativeDal
from src.db.models.tables import Patient, Relative
from src.schemas.base import Gender, RelationshipType, DocType
from conftest import test_session_ctx
from src.utils.other import random_date, random_valid_name, random_valid_series, random_number


def get_document_data(to_db=False) -> dict:
    rdm = uuid.uuid4().hex
    random_doctype = random.choice(list(DocType))
    random_series = random_valid_series(random_doctype)
    return {

        "document_type": random_doctype,
        "series": random_series,
        "number": random_number(),
        "issue_date": random_date() if to_db else random_date().isoformat(),
        "issuing_authority": "issuing_authority" + rdm

    }