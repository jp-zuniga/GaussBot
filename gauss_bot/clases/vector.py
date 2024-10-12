from fractions import Fraction
from typing import overload

class Vector():
    def __init__(self, componentes: list[Fraction] = []) -> None:
        self._componentes = componentes

    @property
    def componentes(self) -> list[Fraction]:
        return self._componentes

    def __eq__(self, vec2: object) -> bool:
        if not isinstance(vec2, Vector):
            return False
        elif len(self) != len(vec2):
            return False
        return all(a == b for a, b in zip(self.componentes, vec2.componentes))

    def __len__(self) -> int:
        return len(self.componentes)

    def __getitem__(self, indice: int) -> Fraction:
        if indice >= len(self):
            raise IndexError("Índice inválido!")
        return self.componentes[indice]

    def __setitem__(self, indice: int, valor: Fraction) -> None:
        if indice >= len(self):
            raise IndexError("Índice inválido!")
        self.componentes[indice] = valor

    def __str__(self) -> str:
        return f"[{', '.join(str(c) for c in self.componentes)}]"

    def __add__(self, vec2: "Vector") -> "Vector":
        if len(self) != len(vec2):
            raise ArithmeticError("Vectores deben tener la misma longitud!")
        return Vector([a + b for a, b in zip(self.componentes, vec2.componentes)])

    def __sub__(self, vec2: "Vector") -> "Vector":
        if len(self) != len(vec2):
            raise ArithmeticError("Vectores deben tener la misma longitud!")
        return Vector([a - b for a, b in zip(self.componentes, vec2.componentes)])

    @overload
    def __mul__(self, vec2: "Vector") -> Fraction: ...

    @overload
    def __mul__(self, escalar: Fraction) -> "Vector": ...

    def __mul__(self, multiplicador: "Vector" | Fraction) -> Fraction | "Vector":
        if isinstance(multiplicador, Vector):
            if len(self) != len(multiplicador):
                raise ArithmeticError("Vectores deben tener la misma longitud!")
            return Fraction(sum(a * b for a, b in zip(self.componentes, multiplicador.componentes)))
        elif isinstance(multiplicador, Fraction):
            return Vector([c * multiplicador for c in self.componentes])
        else:
            raise TypeError("Tipo de dato inválido")
