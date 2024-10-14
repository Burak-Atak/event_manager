from enumfields import Enum


class Day(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    def __str__(self):
        return self.name.capitalize()


class Month(Enum):
    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12

    def __str__(self):
        return self.name.capitalize()


class Frequency(Enum):
    yearly = 0
    monthly = 1
    weekly = 2
    daily = 3

    def __str__(self):
        return self.name.capitalize()