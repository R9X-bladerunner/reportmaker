import random
import uuid

import pytest

from src.dal.patients import PatientDal
from src.dal.relatives import RelativeDal
from src.db.models.tables import Patient, Relative
from src.schemas.base import Gender, RelationshipType
from conftest import test_session_ctx
from src.schemas.relative import RelativeIn
from src.tests.data.patients import get_patient_data
from src.utils.other import random_date, random_valid_name


def get_relative_data(to_db=False, withreltype=True):

    rdm = uuid.uuid4().hex
    relative_data =  {
        'last_name': random_valid_name(),
        'first_name': random_valid_name(),
        'middle_name': random_valid_name(),
        'birthday': random_date() if to_db else random_date().isoformat(),
        'gender': random.choice(list(Gender)),
        'snils': 'snils' + rdm[:5]
    }
    if withreltype:
        relative_data['relationship_type'] = random.choice(list(RelationshipType))

    return relative_data




@pytest.fixture()
def relative() -> Relative:
    with test_session_ctx() as sess, sess.begin():
        p = PatientDal(sess).insert(
            get_patient_data()
        )
        r, rel = PatientDal(sess).create_relative(p.id, RelativeIn(**get_relative_data()))
        sess.expunge(p)
        sess.expunge(r)

    yield r

    with test_session_ctx() as sess, sess.begin():
        RelativeDal(sess).delete({"id": r.id})
        PatientDal(sess).delete({"id": p.id})
