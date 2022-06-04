from enum import IntEnum


class Genders(IntEnum):
    Male = 1
    Female = 2
    Others = 3

    @classmethod
    def choices(cls):
        # print(tuple((i.name, i.value) for i in cls))
        return(tuple((i.name, i.value) for i in cls))

