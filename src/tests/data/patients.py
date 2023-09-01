import random
import uuid

import pytest

from src.dal.patients import PatientDal
from src.db.models.tables import Patient
from src.schemas.base import Gender
from conftest import test_session_ctx
from src.utils.other import random_date, random_valid_name


def get_patient_data(to_db=False):
    rdm = uuid.uuid4().hex
    return {
        'last_name': random_valid_name(),
        'first_name': random_valid_name(),
        'middle_name': random_valid_name(),
        'birthday': random_date() if to_db else random_date().isoformat(),
        'gender': random.choice(list(Gender)),
        'snils': 'snils' + rdm[:5],
    }


@pytest.fixture()
def patient() -> Patient:
    with test_session_ctx() as sess, sess.begin():
        p = PatientDal(sess).insert(
            get_patient_data()
        )
        sess.expunge(p)

    yield p

    with test_session_ctx() as sess, sess.begin():
        PatientDal(sess).delete({"id": p.id})
