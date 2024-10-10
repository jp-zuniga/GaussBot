from fractions import Fraction
from typing import List

class Vector():
    def __init__(self, componentes: List[Fraction] = []) -> None:
        self.componentes = componentes

    def __len__(self) -> int:
        return len(self.componentes)

    def __getitem__(self, indice: int) -> Fraction:
        return self.componentes[indice]

    def __setitem__(self, indice: int, valor: Fraction) -> None:
        self.componentes[indice] = valor

    def __str__(self) -> str:
        return f"[{', '.join(str(c) for c in self.componentes)}]"

    def __add__(self, vec2: 'Vector') -> 'Vector':
        if len(self) != len(vec2):
            raise ValueError("Vectores deben tener la misma longitud")
        return Vector([a + b for a, b in zip(self.componentes, vec2.componentes)])

    def __sub__(self, vec2: 'Vector') -> 'Vector':
        if len(self) != len(vec2):
            raise ValueError("Vectores deben tener la misma longitud")
        return Vector([a - b for a, b in zip(self.componentes, vec2.componentes)])

    def __mul__(self, vec2: 'Vector') -> Fraction:
        if len(self) != len(vec2):
            raise ValueError("Vectores deben tener la misma longitud")
        return Fraction(sum(a * b for a, b in zip(self.componentes, vec2.componentes)))

    def mult_escalar(self, escalar: Fraction) -> 'Vector':
        return Vector([escalar * c for c in self.componentes])
