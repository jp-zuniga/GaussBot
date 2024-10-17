from fractions import Fraction

from gauss_bot.models.matriz import Matriz, Validacion
from gauss_bot.models.vector import Vector


class SistemaEcuaciones:
    """
    Representa un sistema de ecuaciones lineales con una instancia de Matriz() aumentada.

    - cramer() y gauss_jordan() son los métodos principales para resolver un sistema.
    - La solución se almacena en el atributo .solucion,
      y el procedimiento realizado en .procedimiento (ambos como strings)
    """

    def __init__(self, matriz: Matriz) -> None:
        """
        * TypeError: cuando la matriz dada no es aumentada
        """

        if not matriz.aumentada:
            raise TypeError("Matriz debe ser aumentada para representar un sistema de ecuaciones!")
        self.matriz = matriz
        self.solucion = ""
        self.procedimiento = ""
    
    def cramer(self, nombre: str) -> None:
        """
        Resuelve un sistema de ecuaciones ocupando la Regla de Cramer.
        """

        if not self.matriz.aumentada:
            raise TypeError("La matriz no es aumentada; no representa un sistema de ecuaciones!")
        if not self.matriz.filas == self.matriz.columnas - 1:
            raise ArithmeticError("La matriz de variables no es cuadrada; su determinante es indefinido!")

        mat_variables = Matriz(
            False,
            self.matriz.filas,
            self.matriz.columnas - 1,
            [self.matriz.valores[i][:-1] for i in range(self.matriz.filas)],
        )

        col_aumentada = Vector([self.matriz.valores[i][-1] for i in range(self.matriz.filas)])
        sub_dets = []
        soluciones = []

        det, _, _ = mat_variables.calcular_det()
        if det == 0:
            raise ValueError("El determinante de la matriz de variables es 0; no se puede resolver el sistema mediante la Regla de Cramer!")

        for i in range(self.matriz.columnas - 1):
            submat = []
            for j in range(self.matriz.filas):
                submat.append([self.matriz.valores[j][k] if k != i else col_aumentada[j] for k in range(self.matriz.columnas - 1)])
            det_submat, _, _ = Matriz(False, self.matriz.filas, self.matriz.columnas - 1, submat).calcular_det()
            sub_dets.append(det_submat)
            soluciones.append(det_submat / det)

        self.solucion += "\n---------------------------------------------"
        self.solucion += f"Variables de matriz {nombre}:"
        self.solucion += str(mat_variables)
        self.solucion += f"Vector b = {col_aumentada}"
        self.solucion += "---------------------------------------------"
        self.solucion += f"\nDeterminante de la matriz de variables = {det}"
        for i, subdet in enumerate(sub_dets):
            self.solucion += f"Determinante de {nombre}{i+1}(b) = {subdet}"
        self.solucion += "\n---------------------------------------------\n"
        self.solucion += "Soluciones:"
        for i, sol in enumerate(soluciones):
            self.solucion += f"X{i + 1} = {sol}"

    def gauss_jordan(self) -> None:
        """
        * Valida si la matriz es cero o inconsistente de antemano
        * Valida si la matriz ya esta en su forma escalonada reducida para no hacer operaciones innecesarias
        * Reduce la matriz a su forma escalonada y valida si resulta inconsistente
        * Encuentra variables libres y determina si el sistema tiene una solución única
        * Almacena la solución encontrada en .solucion y el procedimiento en .procedimiento
        """

        if self.matriz.es_matriz_cero():
            return

        test_inicial = self._validar_consistencia()
        if not test_inicial[0]:
            if self._validar_escalonada_reducida():
                self.procedimiento += "\nMatriz ya esta en su forma escalonada reducida!\n\n"
            self.procedimiento += str(self.matriz)
            self._obtener_soluciones(unica=False, libres=[], validacion=test_inicial)
            return

        if self._validar_escalonada_reducida():
            self.procedimiento += "\nMatriz ya esta en su forma escalonada reducida!\n\n"
            self.procedimiento += str(self.matriz)
        else:
            self._reducir_matriz()

        test_final = self._validar_consistencia()
        if not test_final[0]:
            self._obtener_soluciones(unica=False, libres=[], validacion=test_final)
            return

        libres = self._encontrar_variables_libres()
        solucion_unica = self._validar_escalonada_reducida() and libres == []
        if solucion_unica:
            self._obtener_soluciones(unica=True, libres=[], validacion=(True, -1))
            return

        # solucion general:
        self._obtener_soluciones(unica=False, libres=libres, validacion=(True, -1))

    def _reducir_matriz(self) -> None:
        """
        * Reduce la matriz a su forma escalonada usando el método de reducción por filas
        * Actualiza .procedimiento con cada operación realizada
        """

        self.procedimiento += "\nMatriz inicial:\n"
        self.procedimiento += str(self.matriz)
        self.procedimiento += "\nReduciendo la matriz a su forma escalonada:\n"

        fila_actual: int = 0

        # encontrar entradas pivotes maximas, normalizar fila pivote, eliminar elementos debajo del pivote
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
                self.matriz.valores[fila_actual], self.matriz.valores[fila_pivote] = self.matriz.valores[fila_pivote], self.matriz.valores[fila_actual]
                self.procedimiento += f"\nF{fila_actual+1} <==> F{fila_pivote+1}\n"
                self.procedimiento += str(self.matriz)

            pivote = self.matriz[fila_actual, j]
            if pivote not in (1, 0):  # normalizar fila pivote (convertir elemento pivote en 1)
                for k in range(self.matriz.columnas):
                    self.matriz[fila_actual, k] /= pivote

                if pivote == -1:
                    self.procedimiento += f"\nF{fila_actual+1} => -F{fila_actual+1}\n"
                else:
                    self.procedimiento += f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote)}\n"
                self.procedimiento += str(self.matriz)

            # eliminar elementos debajo del pivote
            for f in range(fila_actual + 1, self.matriz.filas):
                factor = self.matriz[f, j]
                if factor == 0:
                    continue
                for k in range(self.matriz.columnas):
                    self.matriz[f, k] -= factor * self.matriz[fila_actual, k]

                self.procedimiento += f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor)} * F{fila_pivote+1})\n"
                self.procedimiento += str(self.matriz)
            fila_actual += 1

        # empezando desde la ultima fila y la ultima columna, eliminar elementos encima del pivote
        for i in reversed(range(self.matriz.filas)):
            try:  # intentar encontrar una entrada no cero en la fila; si no hay, saltar a la siguiente fila
                columna_pivote = self.matriz[i].index(next(filter(lambda x: x != 0, self.matriz[i])))
            except StopIteration:
                continue

            for f in reversed(range(i)):
                factor = self.matriz[f, columna_pivote]
                if factor == 0:
                    continue
                for k in range(self.matriz.columnas):
                    self.matriz[f, k] -= factor * self.matriz[i, k]

                self.procedimiento += f"\nF{f+1} => F{f+1} - ({str(factor)} * F{i+1})\n"
                self.procedimiento += str(self.matriz)

    def _encontrar_variables_libres(self) -> list[int]:
        """
        Encuentra variables básicas del sistema, para retornar las variables libres
        * e.g. las que no se agregaron a la lista de básicas
        """

        entradas_principales = []
        for i in range(self.matriz.filas):
            try:  # append la proxima entrada distinta de 0 en la fila
                entradas_principales.append(next(j for j in range(self.matriz.columnas - 1) if self.matriz[i][j] != 0))
            except StopIteration:
                continue

        # las columnas no registradas en entradas_principales representan variables libres
        return [x for x in range(self.matriz.columnas - 1) if x not in entradas_principales]

    def _despejar_variables(self, libres: list[int]) -> list[str]:
        """
        Ocupa _despejar_expresion() para mover terminos al lado derecho de la ecuación/fila
        * libres = lista de indices de columnas de variables libres
        """

        ecuaciones = [f"| X{x+1} es libre\n" for x in libres]  # agregar variables libres

        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas - 1):
                if self.matriz[i, j] == 0:  # si no es la entrada principal:
                    continue

                expresion = self._despejar_expresion(fila=i, columna=j)
                ecuaciones.append(f"| X{j+1} = {expresion}\n")
                break

        # sort las ecuaciones por el indice de la variable (X1, X2, etc.)
        return sorted(ecuaciones, key=lambda x: x[3])

    def _despejar_expresion(self, fila: int, columna: int) -> str:
        """
        'Despeja' una ecuación/fila de la matriz en términos de la variable principal:
        * (1, 0, -1/2 | 3)
        * X1 - 1/2*X3 = 3
        * X1 = 3 + 1/2*X3
        """

        constante = self.matriz[fila, -1]

        # si la constante es 0, no agregar nada
        expresion = str(constante) if constante != 0 else ""

        for j in range(columna + 1, self.matriz.columnas - 1):
            # invertir el signo para "mover al otro lado de la ecuacion"
            coeficiente = -self.matriz[fila, j]
            if coeficiente == 0:
                continue

            signo = " + " if coeficiente > 0 else " - "
            variable = f"{abs(coeficiente)}*X{j+1}" if abs(coeficiente) not in (1, -1) else f"X{j+1}"
            expresion += (
                f"{signo}{variable}"
                if expresion != ""
                else f"{"-" if coeficiente < 0 else ""}{variable}"
            )

        # si la expresion sigue vacia, no se despejo nada y variable = 0
        return expresion if expresion != "" else "0"

    def _validar_consistencia(self) -> Validacion:
        """
        Valida si la matriz es consistente o inconsistente.

        Retorna "Validacion" definido en matriz.py:
        * Validacion = tuple[bool, int]
        * bool = si la matriz es consistente
        * int = fila donde se encontro inconsistencia (-1 si no hay)
        """

        if self.matriz.es_matriz_cero():
            return (True, -1)

        variables_0 = [0 for _ in range(self.matriz.columnas - 1)]
        for i in range(self.matriz.filas):
            constante_es_0 = self.matriz.valores[i][-1] == 0
            variables_actuales = self.matriz.valores[i][:-1]

            # si la fila tiene la forma 0 = b (donde b != 0), es inconsistente
            if variables_actuales == variables_0 and not constante_es_0:
                return (False, i)
        return (True, -1)

    def _validar_escalonada(self) -> bool:
        """
        Valida si la matriz esta en su forma escalonada o no.

        Requerimientos para una matriz escalonada:
        * 1. Todas las filas no cero estan encima de las filas cero
        * 2. La entrada principal de cada fila esta a la derecha de la entrada principal de la fila anterior
        * 3. Todas las entradas debajo de la entrada principal de una fila son cero
        """

        if self.matriz.es_matriz_cero():
            return False

        fila_cero = [0 for _ in range(self.matriz.columnas)]
        for i in range(self.matriz.filas):
            if self.matriz.valores[i] != fila_cero:
                continue

            # condicion 1 del docstring:
            if any(self.matriz.valores[j] != fila_cero for j in range(i + 1, self.matriz.filas)):
                return False

        entrada_anterior = -1
        for i in range(self.matriz.filas):
            try:
                # encontrar indice de la entrada principal de la fila actual
                entrada_actual = next(j for j in range(self.matriz.columnas - 1) if self.matriz.valores[i][j] != 0)
            except StopIteration:  # si no hay entrada principal:
                continue

            entradas_inferiores_cero = any(
                self.matriz.valores[k][entrada_actual] != 0
                for k in range(i + 1, self.matriz.filas)
            )

            # condiciones 2 y 3 del docstring
            if entrada_actual <= entrada_anterior or entradas_inferiores_cero:
                return False

            entrada_anterior = entrada_actual
        return True

    def _validar_escalonada_reducida(self) -> bool:
        """
        Valida si la matriz esta en su forma escalonada reducida o no.

        Requerimientos para una matriz escalonada reducida:
        * 1. La matriz esta en su forma escalonada
        * 2. La entrada principal de cada fila es 1
        """

        # condicion 1 del docstring:
        if not self._validar_escalonada():
            return False

        for i in range(self.matriz.filas):
            try:
                # encontrar indice de la entrada principal de la fila actual
                entrada_principal = next(j for j in range(self.matriz.columnas - 1) if self.matriz.valores[i][j] == 1)
            except StopIteration:
                continue

            # condicion 2 del docstring:
            entradas_inferiores_cero = any(
                self.matriz.valores[k][entrada_principal] != 0 and k != i
                for k in range(self.matriz.filas)
            )

            if entradas_inferiores_cero:
                return False
        return True

    def _obtener_soluciones(self, unica: bool, libres: list[int], validacion: Validacion) -> None:
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

        # unpack la validacion dada:
        solucion, fila_inconsistente = validacion

        if not solucion and fila_inconsistente != -1:  # señalar fila inconsistente
            self.solucion += f"\n| En F{fila_inconsistente+1}: 0 != "
            self.solucion += f"{str(self.matriz[fila_inconsistente, -1])}\n"
            self.solucion += "| Sistema es inconsistente!\n"
            return

        if unica:
            solucion_trivial = all(
                self.matriz[i, -1] == 0 for i in range(self.matriz.filas)
            )

            tipo_solucion = "trivial" if solucion_trivial else "no trivial"
            self.solucion += f"\n| Solución {tipo_solucion} encontrada:\n"
            for i in range(self.matriz.filas):
                if all(x == 0 for x in self.matriz[i]):
                    continue
                self.solucion += (f"| X{i+1} = {str(self.matriz[i, -1])}\n")
            return

        ecuaciones = self._despejar_variables(libres)
        self.solucion += "\n| Sistema no tiene solución única!\n"
        self.solucion += "| Solución general encontrada:\n"
        for linea in ecuaciones:
            self.solucion += linea
        return
