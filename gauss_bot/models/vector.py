"""
Implementación de vectores matemáticos de cualquier dimensión.
Se pueden realizar operaciones básicas como suma, resta,
y multiplicación usando sobrecarga de operadores.
"""

from fractions import Fraction
from typing import (
    Union,
    overload,
)

from . import Matriz


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
        indice: Union[int, slice],
    ) -> Union[Fraction, list[Fraction]]:
        """
        Para acceder a los componentes del vector
        directamente como si fuera lista: Vector()[indice].
        Acepta índices negativos y slices.
        """

        if (
            isinstance(indice, int)
            and -len(self) <= indice < len(self)  # para permitir indices negativos
        ):
            return self.componentes[indice]

        if isinstance(indice, slice):
            start, stop, step = indice.indices(len(self))
            if -len(self) <= start < len(self) and -len(self) <= stop <= len(self):
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

        return str(
            Matriz(
                aumentada=False,
                filas=len(self),
                columnas=1,
                valores=[[c] for c in self.componentes],
            )
        )

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
    def __mul__(self, escalar: Union[int, float, Fraction]) -> "Vector": ...

    def __mul__(
        self,
        multiplicador: Union["Vector", int, float, Fraction],
    ) -> Union[Fraction, "Vector"]:
        """
        Overloads para realizar producto punto o multiplicación por escalar:
        * Vector() * Vector() -> Fraction()
        * Vector() * Union[int, float, Fraction] -> Vector()

        Errores:
        * TypeError: si el tipo de dato es inválido
        * ArithmeticError: si los vectores no tienen la misma longitud
        """

        if isinstance(multiplicador, Vector):
            if len(self) != len(multiplicador):
                raise ArithmeticError("Los vectores deben tener la misma longitud!")
            return Fraction(
                sum(a * b for a, b in zip(self.componentes, multiplicador.componentes))
            )

        if isinstance(multiplicador, (int, float, Fraction)):
            return Vector([Fraction(c * multiplicador) for c in self.componentes])
        raise TypeError("Tipo de dato inválido!")

    def __rmul__(
        self,
        multiplicador: Union[int, float, Fraction],
    ) -> "Vector":
        """
        Realiza multiplicación por escalar:
        * Union[int, float, Fraction] * Vector() -> Vector()

        Errores:
        * TypeError: si el tipo de dato es inválido
        """

        if isinstance(multiplicador, (int, float, Fraction)):
            return Vector([Fraction(c * multiplicador) for c in self.componentes])
        raise TypeError("Tipo de dato inválido!")

    def magnitud(self) -> Fraction:
        """
        Calcula la magnitud de la instancia.
        """

        return Fraction(sum(c**2 for c in self.componentes) ** Fraction(1, 2))

    @staticmethod
    def prod_cruz(dimensiones: int, vecs: list["Vector"]) -> "Vector":
        """
        Calcula el producto cruz de (n - 1) vectores en R^n.

        Args:
        * dimensiones: valor de n para R^n
        * vecs: lista de vectores a multiplicar

        Errores:
        - ArithmethicError:
            - si no hay (n - 1) vectores en vecs
            - si los vectores no están en R^n

        Para n = 2, se retorna un vector unidimensional
        cuyo componente rerpresenta el área del
        paralelogramo formado por los dos vectores.
        """

        if not all(len(x) == dimensiones for x in vecs):
            raise ArithmeticError(f"Todos los vectores deben estar en R{dimensiones}!")

        if dimensiones == 2:
            a1, a2 = vecs[0].componentes
            b1, b2 = vecs[1].componentes
            return Vector([(a1 * b2) - (a2 * b1)])

        if len(vecs) != dimensiones - 1:
            raise ArithmeticError(
                f"Para encontrar un producto cruz en R{dimensiones}, "
                + f"se necesitan {dimensiones - 1} vectores!"
            )

        if dimensiones == 3:
            a1, a2, a3 = vecs[0].componentes
            b1, b2, b3 = vecs[1].componentes
            return Vector(
                [
                    (a2 * b3) - (a3 * b2),
                    (a3 * b1) - (a1 * b3),
                    (a1 * b2) - (a2 * b1),
                ]
            )

        mat_prod_cruz = (
            Matriz(
                aumentada=False,
                filas=len(vecs),
                columnas=dimensiones,
                valores=[vec.componentes for vec in vecs],
            )
            .encontrar_adjunta()
            .transponer()
        )

        return Vector([mat_prod_cruz[0, i] for i in range(mat_prod_cruz.columnas)])
