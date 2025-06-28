"""
Implementación de matrices matemáticas de cualquier dimensión.
Se pueden realizar operaciones básicas como suma, resta y multiplicación
usando sobrecarga de operadores, y operaciónes más complejas con
métodos para transponer, calcular determinante, encontrar inversa, etc.
"""

from copy import deepcopy
from fractions import Fraction
from typing import overload

from .. import FRAC_PREC
from ..utils import format_factor


class Matriz:
    """
    Representa una matriz matemática de cualquier dimensión.
    """

    def __init__(
        self,
        filas: int,
        columnas: int,
        valores: list[list[Fraction]] | None = None,
        aumentada: bool = False,
    ) -> None:
        """
        Args:
            filas:     Número de filas de la matriz.
            columnas:  Número de columnas de la matriz.
            valores:   Lista de elementos.
            aumentada: Indica si representa un sistema de ecuaciones.

        Raises:
            ValueError: si las dimensiones de la matriz no son positivas.
        """

        if filas < 1 or columnas < 1:
            raise ValueError("¡Las dimensiones de la matriz deben ser positivas!")

        self._filas = filas
        self._columnas = columnas

        # si no se proporcionan valores, se inicializa una matriz cero
        if valores is None:
            self._valores = [
                [Fraction(0) for _ in range(columnas)] for _ in range(filas)
            ]
        else:
            self._valores = valores
        self._aumentada = aumentada

    @property
    def aumentada(self) -> bool:
        """
        Si la matriz representa un sistema de ecuaciones con una columna aumentada.
        """

        return self._aumentada

    @property
    def filas(self) -> int:
        """
        Número de filas en la matriz.
        """

        return self._filas

    @property
    def columnas(self) -> int:
        """
        Número de columnas en la matriz.
        """

        return self._columnas

    @property
    def valores(self) -> list[list[Fraction]]:
        """
        Lista 2D que contiene los valores de la matriz.
        """

        return self._valores

    @overload
    def __getitem__(self, indice: int) -> list[Fraction]: ...

    @overload
    def __getitem__(self, indice: slice) -> list[list[Fraction]]: ...

    @overload
    def __getitem__(self, indices: tuple[slice, int]) -> list[Fraction]: ...

    @overload
    def __getitem__(self, indices: tuple[int, slice]) -> list[Fraction]: ...

    @overload
    def __getitem__(self, indices: tuple[int, int]) -> Fraction: ...

    @overload
    def __getitem__(self, indices: tuple[slice, slice]) -> list[list[Fraction]]: ...

    def __getitem__(
        self,
        indice: int
        | slice
        | tuple[slice, int]
        | tuple[int, slice]
        | tuple[int, int]
        | tuple[slice, slice],
    ) -> Fraction | list[Fraction] | list[list[Fraction]]:
        """
        Acceso flexible a elementos de la matriz mediante índices y slices.
        Soporta todas las variantes de indexación que soportaría una lista 2D.

        Formatos soportados:
        - mat[i] .......... list[Fraction]
        - mat[i, j] ....... Fraction
        - mat[i, a:b] ..... list[Fraction]
        - mat[a:b, j] ..... list[Fraction]
        - mat[a:b, c:d] ... list[list[Fraction]]

        Args:
            indice: Índice de la lista 2D a extraer.

        Returns:
            Fraction:             Elemento único en self.
            list[Fraction]:       Fila/columna completa de self.
            list[list[Fraction]]: Submatriz de self.

        Raises:
            IndexError: Si los índices están fuera de rango.
            TypeError:  Si los índices son de tipo inválido.
        ---
        """

        if isinstance(indice, int) and -self.filas <= indice < self.filas:
            return self.valores[indice]

        if isinstance(indice, slice):
            start, stop, step = indice.indices(self.filas)
            if (
                step != 0
                and -self.filas <= start < self.filas
                and -self.filas <= stop <= self.filas
            ):
                return self.valores[indice]

        if isinstance(indice, tuple) and len(indice) == 2:
            fila, columna = indice
            if (
                isinstance(fila, int)
                and isinstance(columna, int)
                and -self.filas <= fila < self.filas
                and -self.columnas <= columna < self.columnas
            ):
                return self.valores[fila][columna]

            if isinstance(fila, slice) and isinstance(columna, int):
                start, stop, step = fila.indices(self.filas)
                if (
                    -self.filas <= start < self.filas
                    and -self.filas <= stop <= self.filas
                    and -self.columnas <= columna < self.columnas
                ):
                    # intercambiar start/stop si se esta recorriendo en reversa
                    if step < 0:
                        start, stop = stop + 1, start + 1
                    return [fila[columna] for fila in self.valores[fila]]

            if isinstance(fila, int) and isinstance(columna, slice):
                start, stop, step = columna.indices(self.columnas)
                if (
                    -self.columnas <= start < self.columnas
                    and -self.columnas <= stop <= self.columnas
                    and -self.filas <= fila < self.filas
                ):
                    # intercambiar start/stop si se esta recorriendo en reversa
                    if step < 0:
                        start, stop = stop + 1, start + 1
                    return self.valores[fila][columna]

            if isinstance(fila, slice) and isinstance(columna, slice):
                start_f, stop_f, step_f = fila.indices(self.filas)
                start_c, stop_c, step_c = columna.indices(self.columnas)
                if (
                    -self.filas <= start_f < self.filas
                    and -self.filas <= stop_f <= self.filas
                    and -self.columnas <= start_c < self.columnas
                    and -self.columnas <= stop_c <= self.columnas
                ):
                    # intercambiar start/stop si se esta recorriendo en reversa
                    if step_f < 0:
                        start_f, stop_f = stop_f + 1, start_f + 1
                    if step_c < 0:
                        start_c, stop_c = stop_c + 1, start_c + 1
                    return [fila[columna] for fila in self.valores[fila]]

        # si no se ha retornado, no se cumplieron las
        # condiciones y el indice que se recibio es invalido
        raise IndexError("¡Índice inválido para una matriz!")

    def __len__(self) -> int:
        """
        Encontrar la 'longitud' de la matriz, e.g. cuantas filas tiene.
        Equivalente a llamar Matriz().filas.

        Returns:
            int: Número de filas de self.
        """

        return len(self.valores)

    def __eq__(self, other: object) -> bool:
        """
        Comparar igualdad entre self y otro objeto.

        Args:
            other: Objeto a comparar.

        Returns:
            bool: Si self es igual a other.
        ---
        """

        # si no se recibe otra matriz, no son iguales
        if not isinstance(other, Matriz):
            return False

        # si las matrices no tienen las mismas dimensiones, no son iguales
        if self.filas != other.filas or self.columnas != other.columnas:
            return False

        # todos los valores deben ser iguales
        return all(
            a == b
            for fila1, fila2 in zip(self.valores, other.valores)
            for a, b in zip(fila1, fila2)
        )

    def __str__(self) -> str:
        """
        Genera una representación legible de self,
        con los valores alineados y separadores correspondientes.

        Returns:
            str: self representado en texto formateado y legible.
        ---
        """

        bounds: tuple[str, str] = ("[ ", " ]") if self.columnas == 1 else ("(", ")")

        # longitud maxima para alinear los valores
        max_len: int = max(
            len(
                str(
                    format_factor(
                        self[i, j].limit_denominator(FRAC_PREC["prec"]),
                        mult=False,
                        parenth_negs=False,
                        parenth_fracs=False,
                        skip_ones=False,
                    )
                    if isinstance(self[i, j], Fraction)
                    else self[i, j]
                )
            )
            for i in range(self.filas)
            for j in range(self.columnas)
        )

        matriz: str = ""
        for i in range(self.filas):
            for j in range(self.columnas):
                # .limit_denominator() para evitar fracciones gigantes
                # .center() alinea el valor dentro de max_len
                valor = str(
                    format_factor(
                        self[i, j].limit_denominator(FRAC_PREC["prec"]),
                        mult=False,
                        parenth_negs=False,
                        parenth_fracs=False,
                        skip_ones=False,
                    )
                    if isinstance(self[i, j], Fraction)
                    else self[i, j]
                ).center(max_len)

                # para matrices nx1, cerrar parentesis immediatamente
                if j == 0 and j == self.columnas - 1:
                    matriz += f"{bounds[0]}  {valor}  {bounds[1]}"

                # abrir parentesis para la primera columna
                elif j == 0:
                    matriz += f"{bounds[0]}  {valor} , "

                # imprimir separador antes de columna aumentada
                elif j == self.columnas - 2 and self.aumentada:
                    matriz += f"{valor}  ||  "

                # cerrar parentesis para la ultima columna
                elif j == self.columnas - 1:
                    matriz += f"{valor}  {bounds[1]}"
                else:
                    matriz += f"{valor}, "
            matriz += "\n"
        return matriz.rstrip()

    def __add__(self, mat2: "Matriz") -> "Matriz":
        """
        Overload de operador para sumar matrices.

        Args:
            mat2: Matriz a sumar.

        Raises:
            ArithmeticError: Si las matrices no tienen las mismas dimensiones.
        ---
        """

        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ArithmeticError("¡Las matrices deben tener las mismas dimensiones!")

        # sumar todos los valores correspondientes de las matrices
        mat_sumada: list[list[Fraction]] = [
            [a + b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]

        # retornar un nuevo objeto Matriz() con los valores sumados
        return Matriz(self.filas, self.columnas, valores=mat_sumada)

    def __sub__(self, mat2: "Matriz") -> "Matriz":
        """
        Overload de operador para restar matrices.

        Args:
            mat2: Matriz a restar.

        Raises:
            ArithmeticError: Si las matrices no tienen las mismas dimensiones.
        ---
        """

        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ArithmeticError("¡Las matrices deben tener las mismas dimensiones!")

        # restar todos los valores correspondientes de las matrices
        mat_restada: list[list[Fraction]] = [
            [a - b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]

        # retornar un nuevo objeto Matriz() con los valores sumados
        return Matriz(self.filas, self.columnas, valores=mat_restada)

    @overload
    def __mul__(self, mat2: "Matriz") -> "Matriz": ...

    @overload
    def __mul__(self, escalar: int | float | Fraction) -> "Matriz": ...

    def __mul__(self, multiplicador: "Matriz" | int | float | Fraction) -> "Matriz":
        """
        Overload de operador para realizar multiplicación con matrices.
        Si se multiplica por un número, se realiza multiplicación escalar.
        Si se multuplica por una matriz, se realiza multiplicación matricial.

        Formatos soportados:
        - Matriz() * Matriz()   -> Matriz()
        - Matriz() * Fraction() -> Matriz()

        Args:
            multiplicador: Escalar/matriz a multiplicar.

        Raises:
            ArithmeticError: Si las dimensiones de las matrices son inválidas.
            TypeError:       Si el tipo de dato del argumento es inválido.
        ---
        """

        if isinstance(multiplicador, Matriz):
            # validar que las matrices sean compatibles para multiplicación
            if self.columnas != multiplicador.filas:
                raise ArithmeticError(
                    "Las matrices no son compatibles para multiplicación.\n"
                    + "El número de columnas de la primera matriz debe ser\n"
                    + "igual al número de filas de la segunda matriz."
                )

            # inicializar una matriz cero con las dimensiones correctas
            mat_multiplicada: list[list[Fraction]] = [
                [Fraction(0) for _ in range(multiplicador.columnas)]
                for _ in range(self.filas)
            ]

            # multiplicar las matrices
            for i in range(self.filas):
                for j in range(multiplicador.columnas):
                    for k in range(self.columnas):
                        mat_multiplicada[i][j] += self[i, k] * multiplicador[k, j]

            return Matriz(self.filas, multiplicador.columnas, valores=mat_multiplicada)

        if isinstance(multiplicador, (int, float, Fraction)):
            # multiplicar todos los valores por el escalar
            mat_multiplicada: list[list[Fraction]] = [
                [Fraction(multiplicador * valor) for valor in fila]
                for fila in self.valores
            ]

            return Matriz(self.filas, multiplicador.columnas, valores=mat_multiplicada)

        raise TypeError("¡Tipo de dato inválido!")

    def __rmul__(self, multiplicador: int | float | Fraction) -> "Matriz":
        """
        Overload de operador para realizar multiplicación entre un escalar y una matriz.

        Utilizado cuando el escalar está a la izquierda del operador:
        - Union[int, float, Fraction] * Matriz() -> Matriz()

        Args:
            multiplicador: Escalar a multiplicar.

        Raises:
            TypeError: Si el tipo de dato del argumento es inválido.
        ---
        """

        if isinstance(multiplicador, (int, float, Fraction)):
            mat_multiplicada: list[list[Fraction]] = [
                [Fraction(multiplicador * valor) for valor in fila]
                for fila in self.valores
            ]

            return Matriz(self.filas, self.columnas, valores=mat_multiplicada)
        raise TypeError("¡Tipo de dato inválido!")

    def es_matriz_cero(self) -> bool:
        """
        Verificar si self es una matriz cero.

        Returns:
            bool: Si todos los elementos de self son cero.
        ---
        """

        return all(all(x == Fraction(0) for x in fila) for fila in self.valores)

    def es_cuadrada(self) -> bool:
        """
        Verificar si self es una matriz cuadrada.

        Returns:
            bool: Si la matriz es cuadrada.
        ---
        """

        return self.filas == self.columnas

    def es_identidad(self) -> bool:
        """
        Verificar si self representa una matriz identidad.

        Returns:
            bool: Si self es una matriz identidad.
        ---
        """

        diagonales_son_1 = all(self[i, i] == Fraction(1) for i in range(self.filas))

        resto_son_cero = all(
            self[i, j] == Fraction(0)
            for i in range(self.filas)
            for j in range(self.columnas)
            if i != j
        )

        return self.es_cuadrada() and diagonales_son_1 and resto_son_cero

    def hacer_triangular_superior(self) -> tuple["Matriz", bool]:
        """
        Realizar operaciones de fila para convertir
        la matriz en una matriz triangular superior.

        Returns:
            (Matriz, bool):
                Los valores modificados y
                una bandera indicando si hubo intercambio de filas.
        ---
        """

        # deepcopy() para no afectar los valores de self
        mat_triangular: list[list[Fraction]] = deepcopy(self.valores)
        intercambio = False

        for i in range(self.filas):
            max_f = i
            max_valor: Fraction = abs(mat_triangular[i][i])

            # encontrar fila con valor maximo en la columna actual
            for j in range(i + 1, self.filas):
                if abs(mat_triangular[j][i]) > max_valor:
                    max_valor: Fraction = abs(mat_triangular[j][i])
                    max_f = j

            # si la fila maxima no es la actual, intercambiarlas
            if max_f != i:
                mat_triangular[i], mat_triangular[max_f] = (
                    mat_triangular[max_f],
                    mat_triangular[i],
                )

                intercambio = not intercambio

            # hacer 0 los valores debajo de la diagonal principal
            for j in range(i + 1, self.filas):
                try:
                    factor = mat_triangular[j][i] / mat_triangular[i][i]
                except ZeroDivisionError:
                    pass
                for k in range(self.columnas):
                    mat_triangular[j][k] -= factor * mat_triangular[i][k]

        return (Matriz(self.filas, self.columnas, valores=mat_triangular), intercambio)

    def transponer(self) -> "Matriz":
        """
        Encontrar la transposición de self.

        Returns:
            Matriz: Transposición encontrada.
        ---
        """

        mat_transpuesta: list[list[Fraction]] = [
            [self[j, i] for j in range(self.filas)] for i in range(self.columnas)
        ]

        return Matriz(self.columnas, self.filas, valores=mat_transpuesta)

    def calcular_det(self) -> Fraction | tuple[Fraction, "Matriz", bool]:
        """
        Calcular el determinante de la instancia.

        Returns:
            Fraction:                 Determinante (para matrices 1x1 y 2x2).
            (Fraction, Matriz, bool):
                Determinante,
                matriz triangular superior y
                bandera de intercambio de filas
               (para matrices nxn, n >= 3).

        Raises:
            ArithmeticError: Si la matriz no es cuadrada.
        ---
        """

        if not self.es_cuadrada():
            raise ArithmeticError(
                "¡El determinante solo está definido para matrices cuadradas!"
            )

        # para matrices 1x1, el determinante es el mismo valor
        if self.filas == 1 and self.columnas == 1:
            return self[0, 0]

        # para matrices 2x2, aplicar la formula ad - bc
        if self.filas == 2 and self.columnas == 2:
            return (self[0, 0] * self[1, 1]) - (self[0, 1] * self[1, 0])

        # para matrices nxn (n >= 3),
        # encontrar la triangular superior,
        # y multiplicar todos los diagonales
        mat_triangular, intercambio = self.hacer_triangular_superior()
        det = Fraction(1)
        for i in range(mat_triangular.filas):
            det *= mat_triangular[i, i]

        # si hubo un intercambio de filas al obtener
        # la triangular superior, se debe cambiar el signo
        if intercambio:
            det *= -1
        return (det, mat_triangular, intercambio)

    def encontrar_adjunta(self) -> "Matriz":
        """
        Calcular la adjunta de self.
        La adjunta es la transposición de la matriz de cofactores de una matriz.

        Returns:
            Matriz: Adjunta de self.

        Raises:
            ArithmeticError: Si la matriz no es cuadrada.
        ---
        """

        # construir matriz de cofactores
        mat_cofactores: list[list[Fraction]] = []
        for i in range(self.filas):
            fila: list[Fraction] = []
            for j in range(self.columnas):
                # encontrar un minor de la matriz,
                # eliminando la fila y columna actual
                mat_minor = Matriz(
                    self.filas - 1,
                    self.columnas - 1,
                    valores=[
                        [self[m, n] for n in range(self.columnas) if n != j]
                        for m in range(self.filas)
                        if m != i
                    ],
                )

                # calcular el determinante del minor
                if len(mat_minor) <= 2 and len(mat_minor[0]) <= 2:
                    det_minor = mat_minor.calcular_det()
                else:
                    det_minor, _, _ = mat_minor.calcular_det()  # type: ignore

                # calcular y agregar el cofactor correspondiente
                # a la fila, columna, y minor actual:
                fila.append(((-1) ** (i + j)) * det_minor)
            mat_cofactores.append(fila)

        return Matriz(self.filas, self.columnas, valores=mat_cofactores).transponer()

    def invertir(self) -> tuple["Matriz", "Matriz", Fraction]:
        """
        Calcular la inversa de self.

        Returns:
            (Matriz, Matriz, Fraction): Inversa, adjunta, determinante.

        Raises:
            ArithmeticError:   Si la matriz no es cuadrada.
            ZeroDivisionError: Si el determinante de la matriz es 0.
        ---
        """

        if self.filas <= 2 and self.columnas <= 2:
            det = self.calcular_det()
        else:
            det, _, _ = self.calcular_det()

        if det == 0:
            raise ZeroDivisionError(
                "El determinante de la matriz es 0; "
                + "por lo tanto, no se puede encontrar su inversa."
            )

        adjunta: "Matriz" = self.encontrar_adjunta()
        inversa: "Matriz" = adjunta * Fraction(1 / det)
        return (inversa, adjunta, det)
