"""
Implementación de sistemas de ecuaciones lineales
representados por una matriz aumentada. Se pueden
resolver con la Regla de Cramer y el método Gauss-Jordan.
"""

from copy import deepcopy
from fractions import Fraction

from gauss_bot import LOGGER
from gauss_bot.models import Matriz


class SistemaEcuaciones:
    """
    Representa un sistema de ecuaciones lineales con una instancia de Matriz() aumentada.

    - cramer() y gauss_jordan() son los métodos principales para resolver un sistema.
    - La solución se almacena en el atributo .solucion,
      y el procedimiento realizado en .procedimiento
      (ambos como strings)
    """

    def __init__(self, matriz: Matriz) -> None:
        """
        Recibe una matriz para representar el sistema de ecuaciones,
        y almacena una deepcopy() para no afectar al objeto original.
        * TypeError: si la matriz dada no es aumentada
        """

        if not matriz.aumentada:
            raise TypeError(
                "Matriz debe ser aumentada para " +
                "representar un sistema de ecuaciones!"
            )

        # se ocupa una deepcopy del objeto Matriz() recibido
        # para evitar cambios en la matriz original, ya que
        # este __init__ recibe una referencia a la matriz
        self.matriz = deepcopy(matriz)
        self.solucion = ""
        self.procedimiento = ""

    def cramer(self, nombre: str) -> None:
        """
        Resuelve un sistema de ecuaciones ocupando la Regla de Cramer.
        """

        if not self.matriz.filas == self.matriz.columnas - 1:
            raise ArithmeticError(
                "La matriz de variables no es cuadrada; " +
                "su determinante es indefinido!"
            )

        # descomponer la matriz para obtener solo las variables
        mat_variables = Matriz(
            aumentada=False,
            filas=self.matriz.filas,
            columnas=self.matriz.columnas - 1,
            valores=[
                self.matriz[i, :-1]
                for i in range(self.matriz.filas)
            ]
        )

        # descomponer para obtener solo las constantes
        col_aumentada = Matriz(
            aumentada=False,
            filas=self.matriz.filas,
            columnas=1,
            valores=[
                [self.matriz[i, -1]]
                for i in range(self.matriz.filas)
            ]
        )

        sub_dets = []
        soluciones = []

        if mat_variables.filas <= 2 and mat_variables.columnas <= 2:
            det = mat_variables.calcular_det()  # type: ignore
        else:
            det, _, _ = mat_variables.calcular_det()  # type: ignore

        if det == 0:
            raise ZeroDivisionError(
                "El determinante de la matriz de variables es 0; " +
                "no se puede resolver el sistema mediante la Regla de Cramer!"
            )

        for i in range(self.matriz.columnas - 1):
            # encontrar la submatriz de la variable i
            submat_valores: list[list[Fraction]] = []
            for j in range(self.matriz.filas):
                submat_valores.append(
                    [
                        self.matriz[j, k]
                        if k != i
                        else col_aumentada[j, 0]
                        for k in range(self.matriz.columnas - 1)
                    ]
                )

            submat = Matriz(
                False,
                self.matriz.filas,
                self.matriz.columnas - 1,
                submat_valores
            )

            if submat.filas <= 2 and submat.columnas <= 2:
                det_submat = submat.calcular_det()  # type: ignore
            else:
                det_submat, _, _ = submat.calcular_det()  # type: ignore

            # almacenar los determinantes de las submatrices,
            # y aplicar la formula para encontrar las soluciones
            sub_dets.append(det_submat)
            soluciones.append(det_submat / det)  # type: ignore

        if all(sol == 0 for sol in soluciones):
            tipo_sol = "trivial"
        else:
            tipo_sol = "no trivial"

        # almacenar el procedimiento
        self.procedimiento += "\n---------------------------------------------"
        self.procedimiento += f"Variables de matriz {nombre}:"
        self.procedimiento += str(mat_variables)
        self.procedimiento += "Vector b:"
        self.procedimiento += str(col_aumentada)
        self.procedimiento += "---------------------------------------------\n"
        self.procedimiento += f"Determinante de la matriz de variables = {det}"
        for i, subdet in enumerate(sub_dets):
            self.procedimiento += f"Determinante de {nombre}_{i+1}(b) = {subdet}"
        self.procedimiento += "\n---------------------------------------------\n"

        # almacenar la solucion
        self.solucion += f"\nSolución {tipo_sol} encontrada:\n"
        for i, sol in enumerate(soluciones):
            self.solucion += f"X{i + 1} = {sol}\n"

    def gauss_jordan(self) -> None:
        """
        Resuelve un sistema de ecuaciones lineales aplicando
        el método de Gauss-Jordan. Realiza operaciones de fila
        para reducir la matriz y encontrar las soluciones.

        - Valida si la matriz es cero o inconsistente de antemano
        - Valida si la matriz ya esta en su forma escalonada
          reducida para no hacer operaciones innecesarias

        - Reduce la matriz a su forma escalonada y
          valida si resulta inconsistente

        - Encuentra variables libres y determina
          si el sistema tiene una solución única

        - Almacena la solución encontrada en .solucion
          y el procedimiento en .procedimiento
        """

        if self.matriz.es_matriz_cero():
            self.solucion += "\nSistema tiene soluciones infinitas!\n"
            self.procedimiento += str(self.matriz)
            self.procedimiento += "Todas las ecuaciones tienen la forma 0 = 0, "
            self.procedimiento += "lo cual siempre es verdadero.\n"
            self.procedimiento += "Por lo tanto, el sistema tiene soluciones infinitas."
            return

        test_inicial = self._validar_consistencia()
        if not test_inicial[0]:
            if self._validar_escalonada_reducida():
                self.procedimiento += "\nMatriz ya esta en su forma escalonada reducida!\n\n"
            self.procedimiento += str(self.matriz)
            self._obtener_soluciones_gj(
                unica=False, libres=[], validacion=test_inicial
            )
            return

        if self._validar_escalonada_reducida():
            self.procedimiento += "\nMatriz ya esta en su forma escalonada reducida!\n\n"
            self.procedimiento += str(self.matriz)
        self._reducir_matriz()

        test_final = self._validar_consistencia()
        if not test_final[0]:
            self._obtener_soluciones_gj(
                unica=False, libres=[], validacion=test_final
            )
            return

        libres = self._encontrar_variables_libres()
        solucion_unica = self._validar_escalonada_reducida() and libres == []
        if solucion_unica:
            self._obtener_soluciones_gj(unica=True, libres=[], validacion=(True, -1))
        else:
            self._obtener_soluciones_gj(unica=False, libres=libres, validacion=(True, -1))

    def _reducir_matriz(self) -> None:
        """
        * Reduce la matriz a su forma escalonada usando el método de reducción por filas
        * Actualiza .procedimiento con cada operación realizada

        Nota:
        -----

        Los métodos _eliminar_debajo() y _eliminar_encima() utilizan el
        __getitem__() de Matriz() para acceder a los valores de la matriz.
        Sin embargo, para asignar valores a la matriz, se accede directamente
        a la lista de valores, porque Matriz() no tiene una implementación
        de __setitem__(), para evitar cambios en la matriz original.

        Resolver sistemas de ecuaciones es un caso especial, entonces
        se accede a .valores directamente, porque se sabe que se esta
        trabajando con una deepcopy() del objeto original.
        (see: SistemasEcuaciones().__init__())
        """

        self._eliminar_debajo()
        self._eliminar_encima()


    def _eliminar_debajo(self) -> None:
        """
        Para cada fila en la matriz:
        * Encuentra entradas pivotes maximas
        * Normaliza fila pivote
        * Elimina elementos debajo del pivote
        """

        fila_actual: int = 0
        for j in range(self.matriz.columnas - 1):
            fila_pivote = None
            maximo = Fraction(0)

            # encontrar la fila pivote de la columna actual
            for i in range(fila_actual, self.matriz.filas):
                if abs(self.matriz[i, j]) > maximo:
                    maximo = abs(self.matriz[i, j])
                    fila_pivote = i

            # si las variables no han cambiado, saltar a la siguiente columna
            if fila_pivote is None or maximo == 0:
                continue

            # intercambiar filas si es necesario
            if fila_pivote != fila_actual:
                temp = self.matriz.valores[fila_actual]
                self.matriz.valores[fila_actual] = self.matriz.valores[fila_pivote]
                self.matriz.valores[fila_pivote] = temp
                del temp
                self.procedimiento += f"\nF{fila_actual+1} <==> F{fila_pivote+1}\n"
                self.procedimiento += str(self.matriz)

            # normalizar fila pivote (convertir elemento pivote en 1)
            pivote = self.matriz[fila_actual, j]
            if pivote not in (1, 0):
                for k in range(self.matriz.columnas):
                    self.matriz.valores[fila_actual][k] /= pivote

                if pivote == -1:
                    self.procedimiento += f"\nF{fila_actual+1} => -F{fila_actual+1}\n"
                else:
                    self.procedimiento += f"\nF{fila_actual+1} => "
                    self.procedimiento += f"F{fila_actual+1} / {pivote}\n"
                self.procedimiento += str(self.matriz)

            # eliminar elementos debajo del pivote
            for f in range(fila_actual + 1, self.matriz.filas):
                factor = self.matriz[f, j]
                if factor == 0:
                    continue
                for k in range(self.matriz.columnas):
                    self.matriz.valores[f][k] -= factor * self.matriz[fila_actual, k]

                self.procedimiento += f"\nF{fila_actual+1} => F{fila_actual+1} − "
                self.procedimiento += f"({factor} * F{fila_pivote+1})\n"
                self.procedimiento += str(self.matriz)
            fila_actual += 1

    def _eliminar_encima(self) -> None:
        """
        * Elimina elementos encima de los pivotes
         (empezando desde la ultima fila y la ultima columna)
        """

        for i in reversed(range(self.matriz.filas)):
            try:
                # encontrar pivote en la fila actual
                columna_pivote = self.matriz[i].index(
                    next(filter(lambda x: x != 0, self.matriz[i]))
                )
            except StopIteration:
                # no hay pivote en la fila actual
                continue

            # para cada fila encima de la fila actual
            # eliminar elementos empezando desde abajo
            for f in reversed(range(i)):
                factor = self.matriz[f, columna_pivote]
                if factor == 0:
                    continue
                for k in range(self.matriz.columnas):
                    self.matriz.valores[f][k] -= factor * self.matriz[i, k]

                self.procedimiento += f"\nF{f+1} => F{f+1} − "
                self.procedimiento += f"({factor} * F{i+1})\n"
                self.procedimiento += str(self.matriz)

    def _encontrar_variables_libres(self) -> list[int]:
        """
        Encuentra variables básicas del sistema, para retornar
        las variables libres (las que no se agregaron a la lista de básicas).

        Retorna:
        * list[int]: lista de índices de variables libres
        """

        entradas_principales = []
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
                # la fila no tiene entrada principal
                continue

        # las columnas no registradas en entradas_principales representan variables libres
        return [
            x for x in range(self.matriz.columnas - 1)
            if x not in entradas_principales
        ]

    def _despejar_variables(self, libres: list[int]) -> list[str]:
        """
        Ocupa _despejar_expresion() para mover
        terminos al lado derecho de la ecuación/fila
        * libres: lista de índices de columnas de variables libres
        """

        ecuaciones = [f"X{x+1} es libre\n" for x in libres]  # agregar variables libres

        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas - 1):
                if self.matriz[i, j] == 0:  # si no es la entrada principal:
                    continue

                expresion = self._despejar_expresion(fila=i, columna=j)
                ecuaciones.append(f"X{j+1} = {expresion}\n")
                break

        # sort las ecuaciones por el indice de la variable (X1, X2, etc.)
        return sorted(ecuaciones, key=lambda x: x[1])

    def _despejar_expresion(self, fila: int, columna: int) -> str:
        """
        'Despeja' una ecuación/fila de la matriz en términos de la variable principal:
        * (1, 0, -1/2 | 3)  # fila
        * X1 − 1/2*X3 = 3   # fila escrita como ecuación
        * X1 = 3 + 1/2*X3   # ecuación despejada (output)
        """

        # validar si el resto de los elementos de la fila son 0
        variable_igual_cero = all(
            self.matriz[fila, x] == 0
            for x in range(self.matriz.columnas)
            if x != fila
        )

        if variable_igual_cero:
            return "0"

        constante = self.matriz[fila, -1]

        # si la constante es 0, no agregar nada
        expresion = str(constante) if constante != 0 else ""

        for j in range(columna + 1, self.matriz.columnas - 1):
            # invertir el signo para "mover al otro lado"
            coeficiente = -self.matriz[fila, j]
            if coeficiente == 0:
                continue

            signo = " + " if coeficiente > 0 else " − "
            variable = (
                f"{abs(coeficiente)}*X{j+1}"
                if abs(coeficiente) not in (1, -1)
                else f"X{j+1}"
            )

            expresion += (
                f"{signo}{variable}"
                if expresion != ""
                else f"{"-" if coeficiente < 0 else ""}{variable}"
            )

        return expresion

    def _validar_consistencia(self) -> tuple[bool, int]:
        """
        Valida si la matriz es consistente o inconsistente.

        Retorna tuple[bool, int]:
        * bool = si la matriz es consistente
        * int = fila donde se encontro inconsistencia (-1 si no hay)
        """

        if self.matriz.es_matriz_cero():
            return (True, -1)

        variables_0 = [0 for _ in range(self.matriz.columnas - 1)]
        for i in range(self.matriz.filas):
            constante_es_0 = self.matriz[i, -1] == 0
            variables_actuales = self.matriz[i, :-1]

            # si la fila tiene la forma 0 = b (donde b != 0), es inconsistente
            if variables_actuales == variables_0 and not constante_es_0:
                return (False, i)
        return (True, -1)

    def _validar_escalonada(self) -> bool:
        """
        Valida si la matriz esta en su forma escalonada o no.

        Condiciones para que una matriz sea escalonada:
        - 1. Todas las filas no cero estan encima de las filas cero
        - 2. La entrada principal de cada fila esta a la derecha
             de la entrada principal de la fila anterior
        - 3. Todas las entradas debajo de la entrada principal de una fila son cero
        """

        if self.matriz.es_matriz_cero():
            return False

        fila_cero = [0 for _ in range(self.matriz.columnas)]
        for i in range(self.matriz.filas):
            if self.matriz[i] != fila_cero:
                continue

            # condicion 1:
            if any(
                self.matriz[j] != fila_cero
                for j in range(i + 1, self.matriz.filas)
            ):
                return False

        entrada_anterior = -1
        for i in range(self.matriz.filas):
            try:
                # encontrar la entrada principal de la fila actual
                entrada_actual = next(
                    j
                    for j in range(self.matriz.columnas - 1)
                    if self.matriz[i, j] != 0
                )
            except StopIteration:
                # no hay entrada principal en la fila
                continue

            entradas_inferiores_cero = any(
                self.matriz[k, entrada_actual] != 0
                for k in range(i + 1, self.matriz.filas)
            )

            # condiciones 2 y 3
            if entrada_actual <= entrada_anterior or entradas_inferiores_cero:
                return False

            entrada_anterior = entrada_actual
        return True

    def _validar_escalonada_reducida(self) -> bool:
        """
        Valida si la matriz esta en su forma escalonada reducida o no.
        Condiciones para que una matriz sea escalonada reducida:
        * 1. La matriz esta en su forma escalonada
        * 2. La entrada principal de cada fila es 1
        """

        # condicion 1:
        if not self._validar_escalonada():
            return False

        for i in range(self.matriz.filas):
            try:
                entrada_principal = next(
                    j
                    for j in range(self.matriz.columnas - 1)
                    if self.matriz[i, j] == 1
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
        return True

    def _obtener_soluciones_gj(
        self,
        unica: bool,
        libres: list[int],
        validacion: tuple[bool, int]
    ) -> None:

        """
        Analiza la matriz para encontrar la solución del sistema de ecuaciones.

        * unica = si el sistema tiene una solución única
        * libres = lista de indices de variables libres
        * validacion = tupla retornada por _validar_consistencia()

        Soluciones posibles:
        * Sistema inconsistente: se determina la fila inconsistente de la matriz
        * Solución única: se deduce si es una solución trivial o no
        * Solución general: se despejan las ecuaciones
        """

        # unpack la validacion recibida:
        solucion, fila_inconsistente = validacion

        if not solucion and fila_inconsistente != -1:
            self.solucion += f"\nEn F{fila_inconsistente+1}: 0 != "
            self.solucion += f"{self.matriz[fila_inconsistente, -1]}\n"
            self.solucion += "Sistema es inconsistente!\n"
            return

        if unica:
            solucion_trivial = all(
                self.matriz[i, -1] == 0
                for i in range(self.matriz.filas)
            )

            tipo_solucion = "trivial" if solucion_trivial else "no trivial"
            self.solucion += f"\nSolución {tipo_solucion} encontrada:\n"

            for i in range(self.matriz.filas):
                if all(x == 0 for x in self.matriz[i]):
                    LOGGER.warning("Saltando fila cero!")
                    continue
                self.solucion += (f"X{i+1} = {self.matriz[i, -1]}\n")
            return

        ecuaciones = self._despejar_variables(libres)
        self.solucion += "\nSistema no tiene solución única!\n"
        self.solucion += "Solución general encontrada:\n"
        for linea in ecuaciones:
            self.solucion += linea
