from enum import Enum


class States(Enum):
    ASKING_LOCATION = 1
    ASKING_DISTANCE = 2
    ASKING_RATES = 3
    ASKING_PRICES = 4
    ASKING_KEYWORDS = 5
    RESULT = 6
