from dataclasses import dataclass


@dataclass
class Book:
    libro_id: int
    titulo: str
    autor: str
    disponible: bool
    categoria: str = ''

    def to_dict(self):
        return self.__dict__
