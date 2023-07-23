from enum import Enum

from telegram import Location

from classes.utils import MISSING


class Distance(Enum):
    SHORT = "<200"
    MEDIUM = "200-1000"
    LONG = ">1000m"
    RANDOM = "random"


class Rates(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    RANDOM = "random"


class Price(Enum):
    FREE = "0"
    INEXPENSIVE = "1"
    MODERATE = "2"
    EXPENSIVE = "3"
    VERY_EXPENSIVE = "4"
    RANDOM = "random"


class UserAnswers:
    def __init__(self):
        self.location: Location = MISSING
        self.distance: Distance = MISSING
        self.rates: Rates = MISSING
        self.price: Price = MISSING
        self.kinds = MISSING
