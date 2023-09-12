import random
import time
from datetime import date

from src.schemas.base import DocType


def random_date() -> date:
    d = random.randint(1, int(time.time()))
    return  date.fromtimestamp(d)

def random_valid_name() -> str:
    """Returns valid random string of rus alphas with random length in range  5 to 10"""
    rus_alpha = ''.join(chr(code) for code in range(ord('А'), ord('я')+1)) + "Ёё"
    name_length = random.randint(5, 10)
    name = ''.join(random.choice(rus_alpha) for _ in range(name_length))
    return name

def random_valid_series(document_type: DocType) -> str:
    """Returns valid random string of document series depending on the document_type"""
    match document_type:
        case DocType.passport:
            return ''.join(random.choice('0123456789') for _ in range(4))

        case DocType.birth_cert_new | DocType.birth_cert_old:
            return generate_birth_cert_series()

def random_number() -> str:
    return ''.join(random.choice('0123456789') for _ in range(6))


def generate_birth_cert_series() -> str:
    """Generates string corresponding to the regex pattern [IVXLC1УХЛС]{1,4}-[А-Я]{2}"""

    part_one_letters = 'IVXLC1УХЛС'
    part_one_length = random.randint(1, 4)
    series  = ''.join(random.choice(part_one_letters) for _ in range(part_one_length))
    series += '-'
    part_two_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    part_two_length = 2
    series += ''.join(random.choice(part_two_letters) for _ in range(part_two_length))

    return series





