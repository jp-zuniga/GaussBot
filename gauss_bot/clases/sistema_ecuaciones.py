from fractions import Fraction

from gauss_bot.clases.matriz import Matriz, Validacion

class SistemaEcuaciones:
    def __init__(self, matriz: Matriz) -> None:
        self.matriz = matriz
        self.respuesta = ""
        self.procedimiento = ""

    def resolver_sistema(self) -> None:
        if self.matriz.es_matriz_cero():
            return None

        test_inicial = self._validar_consistencia()
        if not test_inicial[0]:
            if self._validar_escalonada_reducida():
                self.procedimiento += "\nMatriz ya esta en su forma escalonada reducida!\n\n"
                self.procedimiento += str(self.matriz)
            self._get_soluciones(unica=False, libres=[], validacion=test_inicial)
            return None

        if self._validar_escalonada_reducida():
            self.procedimiento += "\nMatriz ya esta en su forma escalonada reducida!\n\n"
            self.procedimiento += str(self.matriz)
        else:
            self._reducir_matriz()
            test_final = self._validar_consistencia()
            if not test_final[0]:
                self._get_soluciones(unica=False, libres=[], validacion=test_final)
                return None

        libres = self._encontrar_variables_libres()
        solucion_unica = self._validar_escalonada_reducida() and libres == []
        if solucion_unica:
            self._get_soluciones(unica=True, libres=[], validacion=(True, -1))
            return None
        else:
            self._get_soluciones(unica=False, libres=libres, validacion=(True, -1))
            return None

    def _reducir_matriz(self) -> None:
        self.procedimiento += "\nMatriz inicial:\n"
        self.procedimiento += str(self.matriz)
        self.procedimiento += "\nReduciendo la matriz a su forma escalonada:\n"

        fila_actual: int = 0
        for j in range(self.matriz.columnas - 1):
            fila_pivote = None
            maximo = Fraction(0)

            for i in range(fila_actual, self.matriz.filas):
                if abs(self.matriz[i, j]) > maximo:
                    maximo = abs(self.matriz[i, j])
                    fila_pivote = i

            if fila_pivote is None or maximo == 0:
                continue

            if fila_pivote != fila_actual:
                self.matriz.valores[fila_actual], self.matriz.valores[fila_pivote] = self.matriz.valores[fila_pivote], self.matriz.valores[fila_actual]
                self.procedimiento += f"\nF{fila_actual+1} <==> F{fila_pivote+1}\n"
                self.procedimiento += str(self.matriz)

            pivote = self.matriz[fila_actual, j]
            if pivote != 1 and pivote != 0:
                for k in range(self.matriz.columnas):
                    self.matriz[fila_actual, k] /= pivote

                if pivote == -1:
                    self.procedimiento += f"\nF{fila_actual+1} => -F{fila_actual+1}\n"
                else:
                    self.procedimiento += f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote.limit_denominator(100))}\n"

                self.procedimiento += str(self.matriz)

            for f in range(fila_actual + 1, self.matriz.filas):
                factor = self.matriz[f, j]
                if factor == 0:
                    continue
                for k in range(self.matriz.columnas):
                    self.matriz[f, k] -= factor * self.matriz[fila_actual, k]

                self.procedimiento += f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor.limit_denominator(100))} * F{fila_pivote+1})\n"
                self.procedimiento += str(self.matriz)

            fila_actual += 1

        for i in reversed(range(self.matriz.filas)):
            try:
                columna_pivote = self.matriz[i].index(next(filter(lambda x: x != 0, self.matriz[i])))
            except StopIteration:
                columna_pivote = None
            if columna_pivote is None:
                continue

            for f in reversed(range(i)):
                factor = self.matriz[f, columna_pivote]
                if factor == 0:
                    continue
                for k in range(self.matriz.columnas):
                    self.matriz[f, k] -= factor * self.matriz[i, k]

                self.procedimiento += f"\nF{f+1} => F{f+1} - ({str(factor.limit_denominator(100))} * F{i+1})\n"
                self.procedimiento += str(self.matriz)

        return None

    def _encontrar_variables_libres(self) -> list[int]:
        entradas_principales = []
        for i in range(self.matriz.filas):
            try:
                entradas_principales.append(next(j for j in range(self.matriz.columnas - 1) if self.matriz[i][j] != 0))
            except StopIteration:
                continue
        return [x for x in range(self.matriz.columnas - 1) if x not in entradas_principales]

    def _despejar_variables(self, libres: list[int]) -> list[str]:
        ecuaciones = [f"| X{x+1} es libre\n" for x in libres]
        for i in range(self.matriz.filas):
            for j in range(self.matriz.columnas - 1):
                if self.matriz[i, j] == 0:
                    continue

                expresion = self._despejar_expresion(i, j)
                ecuaciones.append(f"| X{j+1} = {expresion}\n")
                break

        return sorted(ecuaciones, key=lambda x: x[3])

    def _despejar_expresion(self, fila: int, columna: int) -> str:
        constante = self.matriz[fila, -1].limit_denominator(100)
        expresion = str(constante) if constante != 0 else ""

        for k in range(columna + 1, self.matriz.columnas - 1):
            coeficiente = -self.matriz[fila, k].limit_denominator(100)
            if coeficiente == 0:
                continue

            signo = " + " if coeficiente > 0 else " - "
            variable = f"{abs(coeficiente)}*X{k+1}" if abs(coeficiente) != 1 else f"X{k+1}"
            expresion += (
                f"{signo}{variable}"
                if expresion
                else f"{"-" if coeficiente < 0 else ""}{variable}"
            )

        return expresion if expresion else "0"

    def _validar_consistencia(self) -> Validacion:
        if self.matriz.valores == [] or self.matriz.es_matriz_cero():
            return (True, -1)

        variables_0 = [0 for _ in range(len(self.matriz.valores[0]) - 1)]
        for i in range(self.matriz.filas):
            constante_0 = self.matriz.valores[i][-1] == 0
            variables_actuales = self.matriz.valores[i][:-1]
            if variables_actuales == variables_0 and not constante_0:
                return (False, i)

        return (True, -1)

    def _validar_escalonada(self) -> bool:
        if self.matriz.valores == [] or self.matriz.es_matriz_cero():
            return False

        fila_cero = [0 for _ in range(self.matriz.columnas)]
        for i in range(self.matriz.filas):
            if self.matriz.valores[i] != fila_cero:
                continue
            if any(self.matriz.valores[j] != fila_cero for j in range(i + 1, self.matriz.filas)):
                return False

        entrada_anterior = -1
        for i in range(self.matriz.filas):
            try:
                entrada_actual = next(j for j in range(self.matriz.columnas - 1) if self.matriz.valores[i][j] != 0)
            except StopIteration:
                continue
            if entrada_actual <= entrada_anterior:
                return False
            if any(self.matriz.valores[k][entrada_actual] != 0 for k in range(i + 1, self.matriz.filas)):
                return False
            entrada_anterior = entrada_actual

        return True

    def _validar_escalonada_reducida(self) -> bool:
        if not self._validar_escalonada():
            return False

        for i in range(self.matriz.filas):
            try:
                entrada_principal = next(j for j in range(self.matriz.columnas - 1) if self.matriz.valores[i][j] == 1)
            except StopIteration:
                continue
            if any(self.matriz.valores[k][entrada_principal] != 0 and k != i for k in range(self.matriz.filas)):
                return False
        return True

    def _get_soluciones(self, unica: bool, libres: list[int], validacion: Validacion) -> None:
        solucion, fila_inconsistente = validacion
        if not solucion and fila_inconsistente != -1:
            self.respuesta += (f"\n| En F{fila_inconsistente+1}: 0 != {str(self.matriz[fila_inconsistente, -1].limit_denominator(100))}\n")
            self.respuesta += ("| Sistema es inconsistente!\n")
            return None
        elif unica:
            solucion_trivial = all(self.matriz[i, -1] == 0 for i in range(self.matriz.filas))
            mensaje_solucion = "trivial" if solucion_trivial else "no trivial"
            self.respuesta += (f"\n| Solución {mensaje_solucion} encontrada:\n")
            for i in range(self.matriz.filas):
                if all(x == 0 for x in self.matriz[i]):
                    continue
                self.respuesta += (f"| X{i+1} = {str(self.matriz[i, -1].limit_denominator(100))}\n")
            return None

        ecuaciones = self._despejar_variables(libres)
        self.respuesta += ("\n| Sistema no tiene solución única!\n")
        self.respuesta += ("| Solución general encontrada:\n")
        for linea in ecuaciones:
            self.respuesta += (linea)
        return None
