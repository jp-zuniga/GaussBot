"""
Implementación de sistemas de ecuaciones lineales
representados por una matriz aumentada. Se pueden
resolver con la Regla de Cramer y el método Gauss-Jordan.
"""

from copy import deepcopy
from fractions import Fraction
from typing import Optional

from .matriz import Matriz
from ..utils import LOGGER, format_factor


class SistemaEcuaciones:
    """
    Representa un sistema de ecuaciones lineales como
    una matriz con una columna aumentada de constantes.
    """

    def __init__(self, matriz: Matriz) -> None:
        """
        Args:
            matriz: Sistema de ecuaciones con columna aumentada.

        Raises:
            TypeError: Si la matriz no tiene una columna aumentada.
        ---
        """

        if not matriz.aumentada:
            raise TypeError(
                "¡La matriz debe ser aumentada para "
                + "representar un sistema de ecuaciones!"
            )

        # se ocupa una deepcopy del objeto Matriz() recibido
        # para evitar cambios en la matriz original, ya que
        # este __init__ recibe una referencia a la matriz
        self.matriz = deepcopy(matriz)
        self.solucion = ""
        self.procedimiento = ""

    def __str__(self) -> str:
        """
        Utilizar la implementación de __str__() de Matriz().
        """

        return str(self.matriz)

    def cramer(self, nombre: str) -> None:
        """
        Resolver self ocupando la Regla de Cramer.

        Args:
            nombre: Nombre del sistemas de ecuaciones.

        Raises:
            ArithmeticError:   Si la matriz de variables del sistema no es cuadrada.
            ZeroDivisionError: Si el determinante de la matriz de variables es 0.
        ---
        """

        if not self.matriz.filas == self.matriz.columnas - 1:
            raise ArithmeticError(
                "La matriz de variables no es cuadrada.\n"
                + "Como su determinante es indefinido, "
                + "no se puede resolver el sistema mediante la Regla de Cramer."
            )

        # descomponer la matriz para obtener solo las variables
        mat_variables = Matriz(
            aumentada=False,
            filas=self.matriz.filas,
            columnas=self.matriz.columnas - 1,
            valores=[self.matriz[i, :-1] for i in range(self.matriz.filas)],
        )

        # descomponer para obtener solo las constantes
        col_aumentada = Matriz(
            aumentada=False,
            filas=self.matriz.filas,
            columnas=1,
            valores=[[self.matriz[i, -1]] for i in range(self.matriz.filas)],
        )

        sub_dets: list[Fraction] = []
        soluciones: list[Fraction] = []

        if mat_variables.filas <= 2 and mat_variables.columnas <= 2:
            det = mat_variables.calcular_det()
        else:
            det, _, _ = mat_variables.calcular_det()  # type: ignore

        if det == 0:
            raise ZeroDivisionError(
                "El determinante de la matriz de variables es 0;  por lo tanto, "
                + "el sistema no se puede resolver mediante la Regla de Cramer."
            )

        for i in range(self.matriz.columnas - 1):
            # encontrar la submatriz de la variable i
            submat = Matriz(
                False,
                self.matriz.filas,
                self.matriz.columnas - 1,
                [
                    [
                        self.matriz[j, k] if k != i else col_aumentada[j, 0]
                        for k in range(self.matriz.columnas - 1)
                    ]
                    for j in range(self.matriz.filas)
                ],
            )

            if submat.filas <= 2 and submat.columnas <= 2:
                det_submat = submat.calcular_det()
            else:
                det_submat, _, _ = submat.calcular_det()  # type: ignore

            # almacenar los determinantes de las submatrices,
            # y aplicar la formula para encontrar las soluciones
            sub_dets.append(det_submat)
            soluciones.append(det_submat / det)  # type: ignore

        if all(sol == 0 for sol in soluciones):
            tipo_sol: str = "trivial"
        else:
            tipo_sol: str = "no trivial"

        # almacenar el procedimiento
        self.procedimiento += "---------------------------------------------\n"
        self.procedimiento += f"{nombre}_var:\n{mat_variables}"
        self.procedimiento += f"\n\nb:\n{col_aumentada}"
        self.procedimiento += "\n---------------------------------------------\n"

        self.procedimiento += f"| {nombre}_var |  =  "
        self.procedimiento += f"{det if det > 0 else f'−{-det}'}\n\n"  # type: ignore

        for i, subdet in enumerate(sub_dets):
            self.procedimiento += f"| {nombre}_{i + 1} (b) |  =  "
            self.procedimiento += f"{subdet if det > 0 else f'−{-subdet}'}\n"  # type: ignore

        self.procedimiento += "---------------------------------------------\n"

        # almacenar la solucion
        self.solucion += f"\nSolución {tipo_sol} encontrada:\n"
        for i, sol in enumerate(soluciones):
            self.solucion += f"X{i + 1} = "
            self.solucion += f"{
                format_factor(
                    sol.limit_denominator(1000),
                    mult=False,
                    parenth_negs=False,
                    parenth_fracs=False,
                    skip_ones=False,
                )
            }\n"

    def gauss_jordan(self) -> None:
        """
        Resolver el sistema aplicando el método de Gauss-Jordan,
        realizando operaciones de fila para reducir
        la matriz y encontrar las soluciones.

        ---

        Procedimiento:
        - Validar si la matriz es cero o inconsistente de antemano.
        - Validar si la matriz está en su forma escalonada reducida.
        - Reducir la matriz a su forma escalonada y validar si resulta inconsistente.
        - Encontrar variables libres y determinar si existe una solución única.
        - Almacenar solución y operaciones realizadas.
        ---
        """

        self.procedimiento += "\nMatriz original:\n"
        self.procedimiento += str(self.matriz) + "\n"

        if self.matriz.es_matriz_cero():
            self.solucion += "\nSistema tiene soluciones infinitas!\n"
            self.procedimiento += "\nTodas las ecuaciones tienen la forma 0 = 0, "
            self.procedimiento += "lo cual siempre es verdadero.\n"
            self.procedimiento += "Por lo tanto, existen soluciones infinitas.\n"
            return

        test_inicial: tuple[bool, int] = self._validar_consistencia()
        if not test_inicial[0]:
            if self._validar_escalonada_reducida():
                self.procedimiento += (
                    "\nMatriz ya esta en su forma escalonada reducida!\n\n"
                )

            self.procedimiento += str(self.matriz)
            self._obtener_soluciones_gj(unica=False, libres=[], validacion=test_inicial)
            return

        if self._validar_escalonada_reducida():
            self.procedimiento += (
                f"\nMatriz ya esta en su forma escalonada reducida!\n\n{self.matriz}"
            )
        else:
            self._reducir_matriz()

        test_final: tuple[bool, int] = self._validar_consistencia()
        if not test_final[0]:
            self._obtener_soluciones_gj(unica=False, libres=[], validacion=test_final)
            return

        libres: list[int] = self._encontrar_variables_libres()
        solucion_unica: bool = self._validar_escalonada_reducida() and libres == []

        self._obtener_soluciones_gj(
            unica=solucion_unica,
            libres=([] if solucion_unica else libres),
            validacion=(True, -1),
        )

    def _reducir_matriz(self) -> None:
        """
        Reducir la matriz a su forma escalonada usando el método de reducción por filas.
        ---
        """

        self._eliminar_debajo()
        self._eliminar_encima()

    def _eliminar_debajo(self) -> None:
        """
        Para cada fila de la matriz:
        - Encontrar entradas pivotes maximas.
        - Normalizar fila pivote.
        - Eliminar elementos debajo del pivote.
        ---
        """

        fila_actual: int = 0
        for j in range(self.matriz.columnas - 1):
            fila_pivote: Optional[int] = None
            maximo = Fraction(0)

            # encontrar la fila pivote de la columna actual
            for i in range(fila_actual, self.matriz.filas):
                if abs(self.matriz[i, j]) > maximo:
                    maximo: Fraction = abs(self.matriz[i, j])
                    fila_pivote: Optional[int] = i

            # si las variables no han cambiado, saltar a la siguiente columna
            if fila_pivote is None or maximo == 0:
                continue

            # intercambiar filas si es necesario
            if fila_pivote != fila_actual:
                self.matriz.valores[fila_actual], self.matriz.valores[fila_pivote] = (
                    self.matriz[fila_pivote],
                    self.matriz[fila_actual],
                )

                self.procedimiento += (
                    f"\n\nF{fila_actual + 1}  <=>  F{fila_pivote + 1}:\n{self.matriz}"
                )

            # normalizar fila pivote (convertir elemento pivote en 1)
            pivote: Fraction = self.matriz[fila_actual, j]
            if pivote not in (1, 0):
                for k in range(self.matriz.columnas):
                    self.matriz.valores[fila_actual][k] /= pivote

                if pivote == -1:
                    self.procedimiento += (
                        f"\n\nF{fila_actual + 1}  =>  -F{fila_actual + 1}:\n"
                    )
                else:
                    self.procedimiento += f"\n\nF{fila_actual + 1}  =>  "
                    self.procedimiento += (
                        f"F{fila_actual + 1} / {format_factor(pivote, False)}:\n"
                    )
                self.procedimiento += str(self.matriz)

            # eliminar elementos debajo del pivote
            for f in range(fila_actual + 1, self.matriz.filas):
                factor: Fraction = self.matriz[f, j]
                if factor == 0:
                    continue

                for k in range(self.matriz.columnas):
                    self.matriz.valores[f][k] -= factor * self.matriz[fila_actual, k]

                self.procedimiento += (
                    f"\n\nF{fila_actual + 1}  =>  F{fila_actual + 1} − "
                )
                self.procedimiento += (
                    f"[ {format_factor(factor)}F{fila_pivote + 1} ]:\n{self.matriz}"
                )
            fila_actual += 1

    def _eliminar_encima(self) -> None:
        """
        Eliminar elementos encima de los pivotes,
        empezando desde la última fila y la última columna.
        ---
        """

        for i in reversed(range(self.matriz.filas)):
            try:
                # encontrar pivote en la fila actual
                columna_pivote: int = self.matriz[i].index(
                    next(filter(lambda x: x != 0, self.matriz[i]))
                )
            except StopIteration:
                # no hay pivote en la fila actual
                continue

            # para cada fila encima de la fila actual
            # eliminar elementos empezando desde abajo
            for f in reversed(range(i)):
                factor: Fraction = self.matriz[f, columna_pivote]
                if factor == 0:
                    continue

                for k in range(self.matriz.columnas):
                    self.matriz.valores[f][k] -= factor * self.matriz[i, k]

                self.procedimiento += f"\n\nF{f + 1}  =>  F{f + 1} − "
                self.procedimiento += f"[ {format_factor(factor)}F{i + 1} ]:\n"
                self.procedimiento += str(self.matriz)

    def _encontrar_variables_libres(self) -> list[int]:
        """
        Encontrar variables libres de self mediante las variables básicas.

        Returns:
            list[int]: Lista de índices de variables libres.
        ---
        """

        entradas_principales: list[int] = []
        for i in range(self.matriz.filas):
            try:
                # encontrar una entrada distinta de 0 en la fila
                entradas_principales.append(
                    next(
                        j
                        for j in range(self.matriz.columnas - 1)
                        if self.matriz[i, j] != 0
                    )
                )
            except StopIteration:
                # la fila es una fila cero
                continue

        # las variables libres no son entradas principales
        return [
            x for x in range(self.matriz.columnas - 1) if x not in entradas_principales
        ]

    def _despejar_variables(self, libres: list[int]) -> list[str]:
        """
        Despejar las variables de las ecuaciones de self.

        Args:
            libres: Lista de índices de columnas de variables libres.

        Returns:
            list[str]: Lista de ecuaciones despejadas.
        ---
        """

        # agregar variables libres
        ecuaciones: list[str] = [f"X{x + 1} es libre\n" for x in libres]

        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas - 1):
                # ignorar entradas distintas a 0
                if self.matriz[i, j] == 0:
                    continue

                expresion: str = self._despejar_expresion(i, j)
                ecuaciones.append(f"X{j + 1} = {expresion}\n")
                break

        # sort las ecuaciones por el indice de la variable (X1, X2, etc.)
        return sorted(ecuaciones, key=lambda x: x[1])

    def _despejar_expresion(self, fila: int, columna: int) -> str:
        """
        Despejar la variable principal de una ecuación.

        Examples:
            - (1, 0, -1/2 | 3)  # fila
            - X1 - 1/2*X3 = 3   # fila escrita como ecuación
            - X1 = 3 + 1/2*X3   # ecuación despejada (output)

        Args:
            fila:    Ecuación del sistema a despejar.
            columna: Variable principal de la ecuación.

        Returns:
            str: La ecuación despejada y formateada.
        ---
        """

        # validar si el resto de los elementos de la fila son 0
        if all(
            self.matriz[fila, x] == 0 for x in range(self.matriz.columnas) if x != fila
        ):
            return "0"

        constante: Fraction = self.matriz[fila, -1]

        # si la constante es 0, no agregar nada
        expresion = str(constante) if constante != 0 else ""

        for j in range(columna + 1, self.matriz.columnas - 1):
            # invertir el signo para "mover al otro lado"
            coeficiente = -self.matriz[fila, j]
            if coeficiente == 0:
                continue

            signo: str = " + " if coeficiente > 0 else " − "

            if coeficiente in (1, -1):
                variable = f"X{j + 1}"
            elif coeficiente.is_integer():
                variable = f"{abs(coeficiente)}X{j + 1}"
            else:
                variable = (
                    f"[ ({abs(coeficiente).limit_denominator(1000)}) • X{j + 1} ]"
                )

            expresion += (
                f"{signo}{variable}"
                if expresion != ""
                else f"{'−' if coeficiente < 0 else ''}{variable}"
            )

        return expresion

    def _validar_consistencia(self) -> tuple[bool, int]:
        """
        Validar si self es consistente o inconsistente.

        Returns:
            tuple[bool, int]: Si la matriz es consistente; el número
                              de fila donde se encontró la inconsistencia
                             (-1 si la matriz es consistente).
        ---
        """

        if self.matriz.es_matriz_cero():
            return (True, -1)

        variables_0: list[int] = [0 for _ in range(self.matriz.columnas - 1)]

        for i in range(self.matriz.filas):
            constante_es_0: bool = self.matriz[i, -1] == 0
            variables_actuales: list[Fraction] = self.matriz[i, :-1]

            # si la fila tiene la forma 0 = b (donde b != 0), es inconsistente
            if variables_actuales == variables_0 and not constante_es_0:
                return (False, i)

        return (True, -1)

    def _validar_escalonada(self) -> bool:
        """
        Validar si self está en su forma escalonada o no.

        ---

        Condiciones para que una matriz sea escalonada:
        1. Todas las filas no cero están encima de las filas cero.
        2. La entrada principal de cada fila está a la
           derecha de la entrada principal de la fila anterior.
        3. Todas las entradas debajo de la entrada principal de una fila son cero.

        ---

        Returns:
            bool: Si self es una matriz escalonada.
        ---
        """

        if self.matriz.es_matriz_cero():
            return False

        fila_cero: list[Fraction] = [Fraction(0) for _ in range(self.matriz.columnas)]
        for i in range(self.matriz.filas):
            if self.matriz[i] != fila_cero:
                continue

            # condición 1:
            if any(
                self.matriz[j] != fila_cero for j in range(i + 1, self.matriz.filas)
            ):
                return False

        entrada_anterior: int = -1
        for i in range(self.matriz.filas):
            try:
                # encontrar la entrada principal de la fila actual
                entrada_actual: int = next(
                    j for j in range(self.matriz.columnas - 1) if self.matriz[i, j] != 0
                )
            except StopIteration:
                # no hay entrada principal en la fila
                continue

            entradas_inferiores_no_cero = any(
                self.matriz[k, entrada_actual] != 0
                for k in range(i + 1, self.matriz.filas)
            )

            # condiciones 2 y 3
            if entrada_actual <= entrada_anterior or entradas_inferiores_no_cero:
                return False

            entrada_anterior: int = entrada_actual

        # las 3 condiciones se cumplieron, es escalonada
        return True

    def _validar_escalonada_reducida(self) -> bool:
        """
        Validar si la matriz está en su forma escalonada reducida o no.

        ---

        Condiciones para que una matriz sea escalonada reducida:
        1. La matriz está en su forma escalonada.
        2. La entrada principal de cada fila es 1.

        ---

        Returns:
            bool: Si self es una matriz escalonada reducida.
        ---
        """

        # condicion 1:
        if not self._validar_escalonada():
            return False

        for i in range(self.matriz.filas):
            try:
                entrada_principal: int = next(
                    j for j in range(self.matriz.columnas - 1) if self.matriz[i, j] == 1
                )
            except StopIteration:
                continue

            # condicion 2:
            entradas_inferiores_cero = any(
                self.matriz[k, entrada_principal] != 0 and k != i
                for k in range(self.matriz.filas)
            )

            if entradas_inferiores_cero:
                return False

        # ambas condiciones se cumplieron
        return True

    def _obtener_soluciones_gj(
        self, unica: bool, libres: list[int], validacion: tuple[bool, int]
    ) -> None:
        """
        Analizar la matriz para encontrar la solución del sistema de ecuaciones.

        ---

        Soluciones posibles:
            Sistema inconsistente: Se determina la fila inconsistente de la matriz.
            Solución única:        Se deduce si es una solución trivial o no.
            Solución general:      Se despejan las ecuaciones.

        ---

        Args:
            unica:      Si el sistema tiene una solución única.
            libres:     Lista de indices de las variables libres.
            validacion: Tupla retornada por self._validar_consistencia().
        ---
        """

        # unpack la validacion recibida:
        solucion, fila_inconsistente = validacion

        if not solucion and fila_inconsistente != -1:
            self.solucion += "\nSistema es inconsistente!"
            self.solucion += f"\nEn la ecuación #{fila_inconsistente + 1}:"
            self.solucion += f"\n0 != {self.matriz[fila_inconsistente, -1]}\n"
            self.procedimiento += f"\n{self.solucion}"
            return

        if unica:
            solucion_trivial = all(
                self.matriz[i, -1] == 0 for i in range(self.matriz.filas)
            )

            tipo_solucion: str = "trivial" if solucion_trivial else "no trivial"

            self.solucion += f"\nSolución {tipo_solucion} encontrada:\n"
            for i in range(self.matriz.filas):
                if all(x == 0 for x in self.matriz[i]):
                    LOGGER.warning("Saltando fila cero!")
                    continue

                self.solucion += f"X{i + 1} = {
                    format_factor(
                        self.matriz[i, -1].limit_denominator(1000),
                        mult=False,
                        parenth_negs=False,
                        parenth_fracs=False,
                        skip_ones=False,
                    )
                }\n"
            self.procedimiento += f"\n{self.solucion}"
            return

        ecuaciones: list[str] = self._despejar_variables(libres)

        self.solucion += "\nSistema no tiene solución única!\n"
        self.solucion += "\nSolución general encontrada:\n"
        for linea in ecuaciones:
            self.solucion += linea
        self.procedimiento += f"\n{self.solucion}"
