"""
Implementación de vectores matemáticos de cualquier dimensión.
Se pueden realizar operaciones básicas como suma, resta,
y multiplicación usando sobrecarga de operadores.
"""

from fractions import Fraction
from typing import (
    overload,
    Union,
)


class Vector:
    """
    Representa un vector matemático de cualquier dimensión.
    Los componentes se almacenan en una lista de objetos Fraction().
    """

    def __init__(self, componentes: list[Fraction]) -> None:
        self._componentes = componentes

    @property
    def componentes(self) -> list[Fraction]:
        """
        Propiedad para acceder al atributo privado '_componentes'.
        """

        return self._componentes

    @overload
    def __getitem__(self, indice: int) -> Fraction: ...

    @overload
    def __getitem__(self, indice: slice) -> list[Fraction]: ...

    def __getitem__(
        self,
        indice: Union[int, slice]
    ) -> Union[Fraction, list[Fraction]]:

        """
        Para acceder a los componentes del vector
        directamente como si fuera lista: Vector()[indice].
        Acepta índices negativos y slices.
        """

        if (
            isinstance(indice, int) and
           -len(self) <= indice < len(self)  # para permitir indices negativos
        ):
            return self.componentes[indice]

        if isinstance(indice, slice):
            start, stop, step = indice.indices(len(self))
            if (-len(self) <= start < len(self) and
               -len(self) <= stop <= len(self)
            ):
                # si se esta recorriendo en reversa, intercambiar start/stop
                if step < 0:
                    start, stop = stop + 1, start + 1
                return self.componentes[indice]

        raise IndexError("Índice inválido!")

    def __eq__(self, vec2: object) -> bool:
        """
        Para comparar dos objetos Vector() con el operador ==.
        """

        if not isinstance(vec2, Vector):
            return False
        if len(self) != len(vec2):
            return False
        return all(a == b for a, b in zip(self.componentes, vec2.componentes))

    def __len__(self) -> int:
        """
        Para obtener la longitud del vector como si fuera lista.
        """

        return len(self.componentes)

    def __str__(self) -> str:
        """
        Para imprimir vectores con un formato más legible.
        """

        return f"[ {', '.join(str(c) for c in self.componentes)} ]"

    def __add__(self, vec2: "Vector") -> "Vector":
        """
        Para sumar vectores de la forma Vector() + Vector()
        * ArithmeticError: si los vectores no tienen la misma longitud
        """

        if len(self) != len(vec2):
            raise ArithmeticError("Vectores deben tener la misma longitud!")
        return Vector([a + b for a, b in zip(self.componentes, vec2.componentes)])

    def __sub__(self, vec2: "Vector") -> "Vector":
        """
        Para restar vectores de la forma Vector() - Vector()
        * ArithmeticError: si los vectores no tienen la misma longitud
        """

        if len(self) != len(vec2):
            raise ArithmeticError("Vectores deben tener la misma longitud!")
        return Vector([a - b for a, b in zip(self.componentes, vec2.componentes)])

    @overload
    def __mul__(self, vec2: "Vector") -> Fraction: ...

    @overload
    def __mul__(self, escalar: Fraction) -> "Vector": ...

    def __mul__(
        self,
        multiplicador: Union["Vector", Fraction]
    ) -> Union[Fraction, "Vector"]:

        """
        Overloads para realizar producto punto o multiplicación por escalar:
        * Vector() * Vector() -> Fraction()
        * Vector() * Fraction() -> Vector()
        * TypeError: si el tipo de dato no es válido
        * ArithmeticError: si los vectores no tienen la misma longitud

        Nota: Para la multiplicación escalar, ocurre lo mismo que con
        objetos Matriz(), asi que se debe escribir el escalar antes del vector
        para que no de error: 2 * Vector() en lugar de Vector() * 2
        """

        if isinstance(multiplicador, Vector):
            if len(self) != len(multiplicador):
                raise ArithmeticError("Los vectores deben tener la misma longitud!")
            return Fraction(
                sum(
                    a * b
                    for a, b in zip(self.componentes, multiplicador.componentes)
                )
            )

        if isinstance(multiplicador, Fraction):
            return Vector([c * multiplicador for c in self.componentes])
        raise TypeError("Tipo de dato inválido!")
