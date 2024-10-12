from fractions import Fraction
from typing import Union, overload


class Vector:
    """
    Representa un vector matemático de cualquier dimensión.
    Los componentes se almacenan en una lista de objetos Fraction().

    Las operaciones vectoriales básicas estan definidas con dunder methods:
    * __add__(): suma de vectores
    * __sub__(): resta de vectores
    * __mul__(): overloads para producto punto y producto por escalar

    De tal manera que se pueda decir:
    * a + b = Vector([a1 + b1, a2 + b2, ..., an + bn])
    * a - b = Vector([a1 - b1, a2 - b2, ..., an - bn])
    * a * b = a1*b1 + a2*b2 + ... + an*bn
    * a * k = Vector([a1*k, a2*k, ..., an*k])

    Donde a y b sean objetos Vector() y k sea un objeto Fraction().

    También se implementan los dunder methods:
    * __getitem__(): para acceder a los componentes del vector
    * __eq__(): para comparar vectores
    * __len__(): para obtener la longitud del vector
    * __str__(): para representar el vector como string
    """

    def __init__(self, componentes: list[Fraction]) -> None:
        self._componentes = componentes

    @property
    def componentes(self) -> list[Fraction]:
        return self._componentes

    def __getitem__(self, indice: int) -> Fraction:
        if indice >= len(self):
            raise IndexError("Índice inválido!")
        return self.componentes[indice]

    def __eq__(self, vec2: object) -> bool:
        if not isinstance(vec2, Vector):
            return False
        if len(self) != len(vec2):
            return False
        return all(a == b for a, b in zip(self.componentes, vec2.componentes))

    def __len__(self) -> int:
        return len(self.componentes)

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

    def __mul__(self, multiplicador: Union["Vector", Fraction]) -> Union[Fraction, "Vector"]:
        if isinstance(multiplicador, Vector):
            if len(self) != len(multiplicador):
                raise ArithmeticError("Vectores deben tener la misma longitud!")
            return Fraction(sum(a * b for a, b in zip(self.componentes, multiplicador.componentes)))
        if isinstance(multiplicador, Fraction):
            return Vector([c * multiplicador for c in self.componentes])
        raise TypeError("Tipo de dato inválido!")
