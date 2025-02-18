"""
Implementación de matrices matemáticas de cualquier dimensión.
Se pueden realizar operaciones básicas como suma, resta y multiplicación
usando sobrecarga de operadores, y operaciónes más complejas con
métodos para transponer, calcular determinante, encontrar inversa, etc.
"""

from copy import deepcopy
from fractions import Fraction
from typing import (
    overload,
    Optional,
    Union,
)

from ..util_funcs import format_factor


class Matriz:
    """
    Representa una matriz matemática de cualquier dimensión.
    Los valores se almacenan una lista bidimensional de objetos Fraction().
    Si la matriz representa un sistema de ecuaciones lineales,
    se puede indicar que incluye una columna aumentada.
    """

    def __init__(
        self,
        aumentada: bool,
        filas: int,
        columnas: int,
        valores: Optional[list[list[Fraction]]] = None,
    ) -> None:

        """
        Args:
        - aumentada: indica si la matriz representa un sistema de ecuaciones,
                     para añadirle la columna de constantes
        - filas/columnas: dimensiones de la matriz (ints positivos)
        - valores: lista 2D de objetos Fraction() (opcional)

        Errores:
        * ValueError: si las dimensiones de la matriz no son positivas
        """

        if filas < 1 or columnas < 1:
            raise ValueError("Las dimensiones de la matriz deben ser positivas!")

        self._aumentada = aumentada
        self._filas = filas
        self._columnas = columnas

        # si no se proporcionan valores, se inicializa una matriz cero
        if valores is None:
            self._valores = [
                [Fraction(0) for _ in range(columnas)]
                for _ in range(filas)
            ]
        else:
            self._valores = valores

    @property
    def aumentada(self) -> bool:
        """
        Propiedad para acceder al atributo privado '_aumentada'.
        """

        return self._aumentada

    @property
    def filas(self) -> int:
        """
        Propiedad para acceder al atributo privado '_filas'.
        """

        return self._filas

    @property
    def columnas(self) -> int:
        """
        Propiedad para acceder al atributo privado '_columnas'.
        """

        return self._columnas

    @property
    def valores(self) -> list[list[Fraction]]:
        """
        Propiedad para acceder al atributo privado '_valores'.
        """

        return self._valores

    @overload
    def __getitem__(self, indice: int) -> list[Fraction]: ...

    @overload
    def __getitem__(self, indices: slice) -> list[list[Fraction]]: ...

    @overload
    def __getitem__(self, indices: tuple[slice, int]) -> list[Fraction]: ...

    @overload
    def __getitem__(self, indices: tuple[int, slice]) -> list[Fraction]: ...

    @overload
    def __getitem__(self, indices: tuple[int, int]) -> Fraction: ...

    @overload
    def __getitem__(self, indices: tuple[slice, slice]) -> list[list[Fraction]]: ...

    def __getitem__(  # pylint: disable=too-many-branches
        self,
        indice: Union[
            int,
            slice,
            tuple[slice, int],
            tuple[int, slice],
            tuple[int, int],
            tuple[slice, slice]
        ]
    ) -> Union[ Fraction, list[Fraction],list[list[Fraction]]]:

        """
        Overloads para acceder a los elementos de la matriz
        sin tener que acceder al atributo 'valores' directamente.
        Acepta cualquier índice que una lista aceptaría, asi que
        se pueden acceder a los valores de la matriz con slices, e.g.
        * Matriz()[0:2, 1:3]
        * en lugar de:
        * Matriz().valores[0:2][1:3]
        """

        if (
            isinstance(indice, int) and
           -self.filas <= indice < self.filas
        ):
            return self.valores[indice]

        if isinstance(indice, slice):
            start, stop, step = indice.indices(self.filas)
            if (
                step != 0 and
               -self.filas <= start < self.filas and
               -self.filas <= stop <= self.filas
            ):
                return self.valores[indice]

        if isinstance(indice, tuple) and len(indice) == 2:
            fila, columna = indice
            if (
                isinstance(fila, int) and
                isinstance(columna, int) and
               -self.filas <= fila < self.filas and
               -self.columnas <= columna < self.columnas
            ):
                return self.valores[fila][columna]

            if isinstance(fila, slice) and isinstance(columna, int):
                start, stop, step = fila.indices(self.filas)
                if (
                   -self.filas <= start < self.filas and
                   -self.filas <= stop <= self.filas and
                   -self.columnas <= columna < self.columnas
                ):

                    # intercambiar start/stop si se esta recorriendo en reversa
                    if step < 0:
                        start, stop = stop + 1, start + 1
                    return [fila[columna] for fila in self.valores[fila]]

            if isinstance(fila, int) and isinstance(columna, slice):
                start, stop, step = columna.indices(self.columnas)
                if (
                   -self.columnas <= start < self.columnas and
                   -self.columnas <= stop <= self.columnas and
                   -self.filas <= fila < self.filas
                ):

                    # intercambiar start/stop si se esta recorriendo en reversa
                    if step < 0:
                        start, stop = stop + 1, start + 1
                    return self.valores[fila][columna]

            if isinstance(fila, slice) and isinstance(columna, slice):
                start_f, stop_f, step_f = fila.indices(self.filas)
                start_c, stop_c, step_c = columna.indices(self.columnas)
                if (
                   -self.filas <= start_f < self.filas and
                   -self.filas <= stop_f <= self.filas and
                   -self.columnas <= start_c < self.columnas and
                   -self.columnas <= stop_c <= self.columnas
                ):

                    # intercambiar start/stop si se esta recorriendo en reversa
                    if step_f < 0:
                        start_f, stop_f = stop_f + 1, start_f + 1
                    if step_c < 0:
                        start_c, stop_c = stop_c + 1, start_c + 1
                    return [fila[columna] for fila in self.valores[fila]]

        # si no se ha retornado, no se cumplieron las
        # condiciones y el indice que se recibio es invalido
        raise IndexError("Índice inválido!")

    def __eq__(self, mat2: object) -> bool:
        """
        Para comparar dos objetos Matriz() con el operador ==.
        """

        # si no se recibe otra matriz, no son iguales
        if not isinstance(mat2, Matriz):
            return False

        # si las matrices no tienen las mismas dimensiones, no son iguales
        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            return False

        # todos los valores deben ser iguales
        return all(
            a == b
            for fila1, fila2 in zip(self.valores, mat2.valores)
            for a, b in zip(fila1, fila2)
        )

    def __str__(self) -> str:
        """
        Genera una representación en legible de la matriz,
        con los valores alineados y separadores correspondientes.
        """

        bounds = ("[ ", " ]") if self.columnas == 1 else ("(", ")")

        # longitud maxima para alinear los valores
        max_len = max(
            len(
                str(
                    format_factor(
                        self[i, j].limit_denominator(1000),
                        mult=False,
                        parenth_negs=False,
                        parenth_fracs=False,
                        skip_ones=False,
                    ) if isinstance(self[i, j], Fraction) else
                    self[i, j]
                )
            )

            for i in range(self.filas)
            for j in range(self.columnas)
        )

        matriz = ""
        for i in range(self.filas):
            for j in range(self.columnas):
                # .limit_denominator() para evitar fracciones gigantes
                # .center() alinea el valor dentro de max_len
                valor = str(
                    format_factor(
                        self[i, j].limit_denominator(1000),
                        mult=False,
                        parenth_negs=False,
                        parenth_fracs=False,
                        skip_ones=False,
                    ) if isinstance(self[i, j], Fraction) else
                    self[i, j]
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
        Para sumar matrices de la forma Matriz() + Matriz()
        * ArithmeticError: si las matrices no tienen las mismas dimensiones
        """

        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ArithmeticError("Las matrices deben tener las mismas dimensiones!")

        # sumar todos los valores correspondientes de las matrices
        mat_sumada = [
            [a + b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]

        # retornar un nuevo objeto Matriz() con los valores sumados
        return Matriz(self.aumentada, self.filas, self.columnas, mat_sumada)

    def __sub__(self, mat2: "Matriz") -> "Matriz":
        """
        Para restar matrices de la forma Matriz() - Matriz()
        * ArithmeticError: si las matrices no tienen las mismas dimensiones
        """

        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ArithmeticError(
                "Las matrices deben tener las mismas dimensiones!"
            )

        # restar todos los valores correspondientes de las matrices
        mat_restada = [
            [a - b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]

        # retornar un nuevo objeto Matriz() con los valores sumados
        return Matriz(self.aumentada, self.filas, self.columnas, mat_restada)

    @overload
    def __mul__(self, mat2: "Matriz") -> "Matriz": ...

    @overload
    def __mul__(self, escalar: Union[int, float, Fraction]) -> "Matriz": ...

    def __mul__(
        self,
        multiplicador: Union["Matriz", int, float, Fraction],
    ) -> "Matriz":

        """
        Overloads para multiplicar matrices o multiplicar matrices por escalares:
        * Matriz() * Matriz() -> Matriz()
        * Matriz() * Fraction() -> Matriz()

        Errores:
        * TypeError: si el tipo de dato es inválido
        * ArithmeticError: si las dimensiones de las matrices son inválidas
        """

        if isinstance(multiplicador, Matriz):
            # validar que las matrices sean compatibles para multiplicación
            if self.columnas != multiplicador.filas:
                raise ArithmeticError(
                    "El número de columnas de la primera matriz debe " +
                    "ser igual al número de filas de la segunda matriz!"
                )

            # inicializar una matriz cero con las dimensiones correctas
            mat_multiplicada = [
                [Fraction(0) for _ in range(multiplicador.columnas)]
                for _ in range(self.filas)
            ]

            # multiplicar las matrices
            for i in range(self.filas):
                for j in range(multiplicador.columnas):
                    for k in range(self.columnas):
                        mat_multiplicada[i][j] += (
                            self[i, k] * multiplicador[k, j]
                        )

            return Matriz(
                self.aumentada,
                self.filas,
                multiplicador.columnas,
                mat_multiplicada,
            )

        if isinstance(multiplicador, (int, float, Fraction)):
            # multiplicar todos los valores por el escalar
            mat_multiplicada = [
                [Fraction(multiplicador * valor) for valor in fila]
                for fila in self.valores
            ]

            return Matriz(
                self.aumentada,
                self.filas,
                self.columnas,
                mat_multiplicada,
            )

        raise TypeError("Tipo de dato inválido!")

    def __rmul__(self, multiplicador: Union[int, float, Fraction]) -> "Matriz":
        """
        Realiza multiplicación por escalar:
        * Union[int, float, Fraction] * Matriz() -> Matriz()

        Errores:
        * TypeError: si el tipo de dato es inválido
        """

        if isinstance(multiplicador, (int, float, Fraction)):
            mat_multiplicada = [
                [Fraction(multiplicador * valor) for valor in fila]
                for fila in self.valores
            ]

            return Matriz(
                self.aumentada,
                self.filas,
                self.columnas,
                mat_multiplicada,
            )
        raise TypeError("Tipo de dato inválido!")

    def es_matriz_cero(self) -> bool:
        """
        Verifica si todos los valores de la instancia son 0.
        """

        return all(
            all(x == Fraction(0) for x in fila)
            for fila in self.valores
        )

    def es_cuadrada(self) -> bool:
        """
        Verifica si la instancia es cuadrada.
        """

        return self.filas == self.columnas

    def es_identidad(self) -> bool:
        """
        Verifica si la instancia representa una matriz identidad:
        * Debe ser cuadrada
        * Todos los elementos de la diagonal principal deben ser 1
        * Todos los demás elementos deben ser 0
        """

        diagonales_son_1 = all(
            self[i, i] == Fraction(1)
            for i in range(self.filas)
        )

        resto_son_cero = all(
            self[i, j] == Fraction(0)
            for i in range(self.filas)
            for j in range(self.columnas)
            if i != j
        )

        return self.es_cuadrada() and diagonales_son_1 and resto_son_cero

    def hacer_triangular_superior(self) -> tuple["Matriz", bool]:
        """
        Usada para calcular determinantes. Realiza operaciones de fila
        para convertir la matriz en una matriz triangular superior.

        Retorna:
        * Matriz(): los valores modificados
        * bool: si hubo intercambio de filas
        """

        # deepcopy() para no afectar self
        mat_triangular: list[list[Fraction]] = deepcopy(self.valores)
        intercambio = False

        for i in range(self.filas):
            max_f = i
            max_valor = abs(mat_triangular[i][i])

            # encontrar fila con valor maximo en la columna actual
            for j in range(i + 1, self.filas):
                if abs(mat_triangular[j][i]) > max_valor:
                    max_valor = abs(mat_triangular[j][i])
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

        return (
            Matriz(
                self.aumentada,
                self.filas,
                self.columnas,
                mat_triangular,
            ),
            intercambio,
        )

    def transponer(self) -> "Matriz":
        """
        Crea una nueva lista bidimensional con los valores de la
        instancia transpuestos, y los retorna como un nuevo objeto Matriz().
        """

        mat_transpuesta = [
            [self[j, i] for j in range(self.filas)]
            for i in range(self.columnas)
        ]

        return Matriz(self.aumentada, self.columnas, self.filas, mat_transpuesta)

    def calcular_det(self) -> Union[Fraction, tuple[Fraction, "Matriz", bool]]:
        """
        Calcula el determinante de la instancia.
        * ArithmeticError: si la matriz no es cuadrada

        Para matrices 1x1 y 2x2, solo retorna el determinante.
        Para matrices de nxn (n > 2), retorna:
        * Fraction(): determinante
        * Matriz(): matriz triangular superior
        * bool:     bandera de intercambio de filas

        La matriz triangular superior y la bandera de intercambio
        se utilizan para mostrar el procedimiento, pero si solo se necesita
        el determinante, se pueden descartar los otros elementos de la tupla:
        * det, _, _ = Matriz().calcular_det()
        """

        if not self.es_cuadrada():
            raise ArithmeticError(
                "El determinante solo esta definido para matrices cuadradas!"
            )

        # para matrices 1x1, el determinante es el mismo valor
        if self.filas == 1 and self.columnas == 1:
            return self[0, 0]

        # para matrices 2x2, aplicar la formula ad - bc
        if self.filas == 2 and self.columnas == 2:
            return (self[0, 0] * self[1, 1]) - (self[0, 1] * self[1, 0])

        # para matrices nxn (n > 2),
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
        Encuentra y retorna la adjunta de la instancia.
        La adjunta es la transposición de la matriz de cofactores de una matriz.
        * ArithmeticError: si la matriz no es cuadrada
        """

        # construir matriz de cofactores
        mat_cofactores = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                # encontrar un minor de la matriz,
                # eliminando la fila y columna actual
                minor = [
                    [
                        self[m, n]
                        for n in range(self.columnas)
                        if n != j
                    ]
                    for m in range(self.filas)
                    if m != i
                ]

                # calcular el determinante del minor
                if len(minor) <= 2 and len(minor[0]) <= 2:
                    det_minor = Matriz(
                        False, self.filas - 1, self.columnas - 1, minor
                    ).calcular_det()  # type: ignore
                else:
                    det_minor, _, _ = Matriz(
                        False, self.filas - 1, self.columnas - 1, minor
                    ).calcular_det()  # type: ignore

                # calcular el cofactor correspondiente
                # a la fila, columna, y minor:
                cofactor = ((-1) ** (i + j)) * det_minor
                fila.append(cofactor)
            mat_cofactores.append(fila)

        return Matriz(
            self.aumentada,
            self.filas,
            self.columnas,
            mat_cofactores
        ).transponer()

    def invertir(self) -> tuple["Matriz", "Matriz", Fraction]:
        """
        Encuentra la inversa de la instancia,
        ocupando la formula: 1/det(A) * adj(A)
        * ArithmeticError: si la matriz no es cuadrada
        * ZeroDivisionError: si el determinante de la matriz es 0

        Retorna una tupla con:
        * Matriz(): inversa
        * Matriz(): adjunta
        * Fraction(): determinante
        """

        if self.filas <= 2 and self.columnas <= 2:
            det = self.calcular_det()  # type: ignore
        else:
            det, _, _ = self.calcular_det()  # type: ignore

        if det == 0:
            raise ZeroDivisionError(
                "El determinante de la matriz es 0; no es invertible!"
            )

        adjunta = self.encontrar_adjunta()
        inversa = adjunta * Fraction(1 / det)  # type: ignore
        return (inversa, adjunta, det)  # type: ignore
