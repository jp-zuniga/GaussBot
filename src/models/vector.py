"""
Implementación de vectores matemáticos de cualquier dimensión.
Se pueden realizar operaciones básicas como suma, resta,
y multiplicación usando sobrecarga de operadores.
"""

from __future__ import annotations

from fractions import Fraction
from typing import overload

from . import Matriz


class Vector:
    """
    Representa un vector matemático de cualquier dimensión.
    """

    def __init__(self, componentes: list[Fraction]) -> None:
        self._componentes = componentes

    @property
    def componentes(self) -> list[Fraction]:
        """
        Lista de elementos del vector.
        """

        return self._componentes

    @overload
    def __getitem__(self, indice: int) -> Fraction: ...

    @overload
    def __getitem__(self, indice: slice) -> list[Fraction]: ...

    def __getitem__(self, indice: int | slice) -> Fraction | list[Fraction]:
        """
        Acceso flexible a elementos del vector mediante índices y slices.
        Soporta todas las variantes de indexación que soportaría una lista.

        Formatos soportados:
        - vec[i] ......... Fraction
        - vec[a:b] ....... list[Fraction]
        - vec[a:b:c] ..... list[Fraction]

        Args:
            indice: Índice a extraer.

        Returns:
            Fraction:       Componente único del vector.
            list[Fraction]: Subconjunto de componentes del vector.

        Raises:
            IndexError: Si el índice está fuera de rango.
            TypeError:  Si el índice es de tipo inválido.
        ---
        """

        if isinstance(indice, int) and -len(self) <= indice < len(self):
            return self.componentes[indice]

        if isinstance(indice, slice):
            start, stop, step = indice.indices(len(self))
            if -len(self) <= start < len(self) and -len(self) <= stop <= len(self):
                # si se esta recorriendo en reversa, intercambiar start/stop
                if step < 0:
                    start, stop = stop + 1, start + 1
                return self.componentes[indice]

        raise IndexError("Índice inválido.")

    def __len__(self) -> int:
        """
        Encontrar la longitud del vector.
        """

        return len(self.componentes)

    def __eq__(self, other: object) -> bool:
        """
        Comparar igualdad entre self y otro objeto.

        Args:
            other: Objeto a comparar.

        Returns:
            bool: Si self es igual a other.
        ---
        """

        if not isinstance(other, Vector):
            return False
        if len(self) != len(other):
            return False

        return all(a == b for a, b in zip(self.componentes, other.componentes))

    def __str__(self) -> str:
        """
        Usa la implementación de __str__() de Matriz().
        """

        return str(
            Matriz(filas=len(self), columnas=1, valores=[[c] for c in self.componentes])
        )

    def __add__(self, vec2: Vector) -> Vector:
        """
        Overload de operador para sumar vectores.

        Args:
            vec2: Vector a sumar.

        Raises:
            ArithmeticError: Si los vectores no tienen las mismas dimensiones.
        ---
        """

        if len(self) != len(vec2):
            raise ArithmeticError("Los vectores deben tener la misma longitud.")
        return Vector([a + b for a, b in zip(self.componentes, vec2.componentes)])

    def __sub__(self, vec2: Vector) -> Vector:
        """
        Overload de operador para restar vectores.

        Args:
            vec2: Vector a restar.

        Raises:
            ArithmeticError: Si los vectores no tienen las mismas dimensiones.
        ---
        """

        if len(self) != len(vec2):
            raise ArithmeticError("Los vectores deben tener la misma longitud.")
        return Vector([a - b for a, b in zip(self.componentes, vec2.componentes)])

    @overload
    def __mul__(self, vec2: Vector) -> Fraction: ...

    @overload
    def __mul__(self, escalar: int | float | Fraction) -> Vector: ...

    def __mul__(
        self, multiplicador: Vector | int | float | Fraction
    ) -> Fraction | Vector:
        """
        Overload del operador para realizar producto punto o multiplicación escalar.

        Formatos soportados:
        - Producto Punto:         Vector() * Vector()               -> Fraction
        - Multiplicación Escalar: Vector() * int | float | Fraction -> Vector

        Args:
            multiplicador: Vector o escalar a multiplicar.

        Returns:
            Fraction: Producto punto de los vectores.
            Vector:   Vector multiplicado por el escalar.

        Raises:
            ArithmeticError: Si los vectores no tienen la misma longitud.
            TypeError:       Si el tipo de dato del argumento es inválido.
        ---
        """

        if isinstance(multiplicador, Vector):
            if len(self) != len(multiplicador):
                raise ArithmeticError("Los vectores deben tener la misma longitud.")
            return Fraction(
                sum(a * b for a, b in zip(self.componentes, multiplicador.componentes))
            )

        if isinstance(multiplicador, (int, float, Fraction)):
            return Vector([Fraction(c * multiplicador) for c in self.componentes])
        raise TypeError("Tipo de dato inválido.")

    def __rmul__(self, multiplicador: int | float | Fraction) -> Vector:
        """
        Overload del operador para realizar multiplicación escalar por la derecha.

        Utilizado cuando el escalar está a la izquierda del operador:
        - int | float | Fraction * Vector() -> Vector()

        Args:
            multiplicador: Escalar a multiplicar por cada componente del vector.

        Returns:
            Vector: Vector multiplicado por el escalar.

        Raises:
            TypeError: Si el tipo de dato del argumento es inválido.
        ---
        """

        if isinstance(multiplicador, (int, float, Fraction)):
            return Vector([Fraction(c * multiplicador) for c in self.componentes])
        raise TypeError("Tipo de dato inválido.")

    def magnitud(self) -> Fraction:
        """
        Calcular la magnitud de self.

        Utiliza la fórmula:
        - || a || = √(x^2 + y^2 + z^2 + ...)

        Returns:
            Fraction: Magnitud de self.
        ---
        """

        return Fraction(sum(c**2 for c in self.componentes) ** Fraction(1, 2))

    @staticmethod
    def prod_cruz(dimensiones: int, vecs: list[Vector]) -> Vector:
        """
        Calcula el producto cruz de (n - 1) vectores en R^n.

        Args:
            dimensiones: Valor de n para R^n.
            vecs:        Lista de vectores a multiplicar.

        Returns:
            Vector: Producto cruz de los vectores dados.

        Raises:
            ArithmeticError: Si no hay (n - 1) vectores en vecs.
            ArithmeticError: Si los vectores no están en R^n.
        ---
        """

        if not all(len(x) == dimensiones for x in vecs):
            raise ArithmeticError(f"Todos los vectores deben estar en R{dimensiones}.")

        if dimensiones == 2:
            a1, a2 = vecs[0].componentes
            b1, b2 = vecs[1].componentes
            return Vector([(a1 * b2) - (a2 * b1)])

        if len(vecs) != dimensiones - 1:
            raise ArithmeticError(
                f"Para encontrar un producto cruz en R{dimensiones}, "
                + f"se necesitan {dimensiones - 1} vectores."
            )

        if dimensiones == 3:
            a1, a2, a3 = vecs[0].componentes
            b1, b2, b3 = vecs[1].componentes
            return Vector(
                [(a2 * b3) - (a3 * b2), (a3 * b1) - (a1 * b3), (a1 * b2) - (a2 * b1)]
            )

        mat_prod_cruz = (
            Matriz(
                filas=len(vecs),
                columnas=dimensiones,
                valores=[vec.componentes for vec in vecs],
            )
            .encontrar_adjunta()
            .transponer()
        )

        return Vector([mat_prod_cruz[0, i] for i in range(mat_prod_cruz.columnas)])
