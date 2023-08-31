import random
import time
from datetime import date


def random_date() -> date:
    d = random.randint(1, int(time.time()))
    return date.fromtimestamp(d)
