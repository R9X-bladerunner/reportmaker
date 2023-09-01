import random
import time
from datetime import date


def random_date() -> date:
    d = random.randint(1, int(time.time()))
    return  date.fromtimestamp(d)

def random_valid_name() -> str:
    rus_alpha = ''.join(chr(code) for code in range(ord('А'), ord('я')+1)) + "Ёё"
    name_length = random.randint(5, 10)
    name = ''.join(random.choice(rus_alpha) for _ in range(name_length))
    return name  # returns random sequence of rus alphas with random length in range  5 to 10