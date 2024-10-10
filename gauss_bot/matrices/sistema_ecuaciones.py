from fractions import Fraction
from typing import Tuple, List

from gauss_bot.matrices.matriz import Matriz

# type annotations:
Validacion = Tuple[bool, int]

class SistemaEcuaciones:
    def __init__(self, matriz: Matriz) -> None:
        self.matriz = matriz
        self.filas = matriz.filas
        self.columnas = matriz.columnas

        self.respuesta: List[str] = []
        self.procedimiento: List[str] = []

    def resolver_sistema(self) -> None:
        self.reducir_matriz()
        if self.matriz.es_matriz_cero():
            return None

        libres = self.encontrar_variables_libres()
        if self.matriz.validar_escalonada_reducida() and not libres:  # solucion unica:
            self.imprimir_soluciones(unica=True, libres=[], validacion=(True, -1))
            return None

        # solucion general:
        self.imprimir_soluciones(unica=False, libres=libres, validacion=(True, -1))
        return None

    def reducir_matriz(self) -> None:
        test_inicial = self.matriz.validar_consistencia()
        if not test_inicial[0]:
            self.imprimir_soluciones(unica=False, libres=[], validacion=test_inicial)
            return None
        elif self.matriz.validar_escalonada_reducida():
            self.procedimiento.append("\nMatriz ya esta en su forma escalonada reducida!\n")
            return None

        self.procedimiento.append("\nMatriz inicial:\n")
        self.procedimiento.append(self.matriz.get_mat_str())
        self.procedimiento.append("\nReduciendo la matriz a su forma escalonada:\n")

        fila_actual = 0
        for j in range(self.columnas - 1):  # encontrar pivotes y eliminar elementos debajo
            fila_pivote = None
            maximo = Fraction(0)

            # buscar la entrada con el valor mas grande para usarla como pivote
            for i in range(fila_actual, self.filas):
                if abs(self.matriz[i, j]) > maximo:
                    maximo = abs(self.matriz[i, j])
                    fila_pivote = i

            # si las variables siguen iguales, no hay pivote y se pasa a la siguiente columna
            if fila_pivote is None or maximo == 0:
                continue

            # siempre trabajar con la fila pivote
            if fila_pivote != fila_actual:
                self.matriz.valores[fila_actual], self.matriz.valores[fila_pivote] = self.matriz.valores[fila_pivote], self.matriz.valores[fila_actual]
                self.procedimiento.append(f"\nF{fila_actual+1} <==> F{fila_pivote+1}\n")
                self.procedimiento.append(self.matriz.get_mat_str())

            pivote = self.matriz[fila_actual][j]
            if pivote != 1 and pivote != 0:  # hacer el pivote igual a 1
                for k in range(self.columnas):
                    self.matriz[fila_actual][k] /= pivote
                if pivote == -1:
                    self.procedimiento.append(f"\nF{fila_actual+1} => -F{fila_actual+1}\n")
                else:
                    self.procedimiento.append(f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote.limit_denominator(100))}\n")

                self.procedimiento.append(self.matriz.get_mat_str())

            # eliminar los elementos debajo del pivote
            for f in range(fila_actual + 1, self.filas):
                factor = self.matriz[f][j]
                if factor == 0:
                    continue
                for k in range(self.columnas):
                    self.matriz[f][k] -= factor * self.matriz[fila_actual][k]

                self.procedimiento.append(f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor.limit_denominator(100))} * F{fila_pivote+1})\n")
                self.procedimiento.append(self.matriz.get_mat_str())

            fila_actual += 1

        for i in reversed(range(self.filas)):  # eliminar elementos arriba de pivotes
            try:
                columna_pivote = self.matriz[i].index(next(filter(lambda x: x != 0, self.matriz[i])))
            except StopIteration:
                columna_pivote = None
            if columna_pivote is None:  # no hay entrada principal
                continue

            # eliminar los elementos encima del pivote
            for f in reversed(range(i)):
                factor = self.matriz[f][columna_pivote]
                if factor == 0:
                    continue
                for k in range(self.columnas):
                    self.matriz[f][k] -= factor * self.matriz[i][k]

                self.procedimiento.append(f"\nF{f+1} => F{f+1} - ({str(factor.limit_denominator(100))} * F{i+1})\n")
                self.procedimiento.append(self.matriz.get_mat_str())

        test_final = self.matriz.validar_consistencia()
        if not test_final[0]:
            self.imprimir_soluciones(unica=False, libres=[], validacion=test_final)
            return None
        return None

    def encontrar_variables_libres(self) -> List[int]:
        entradas = []

        # encontrar entradas principales
        for i in range(self.matriz.filas):
            try:
                entradas.append(next(j for j in range(self.matriz.columnas - 1) if self.matriz[i][j] != 0))
            except StopIteration:
                continue

        # si no son entradas principales, son variables libres
        return [x for x in range(self.matriz.columnas - 1) if x not in entradas]

    def despejar_variables(self, libres: List[int]) -> List[str]:
        ecuaciones = []
        for x in libres:
            ecuaciones.append(f"| X{x+1} es libre\n")

        for i in range(self.filas):
            for j in range(self.columnas - 1):
                if self.matriz[i, j] == 0:
                    continue

                constante = self.matriz[i, -1].limit_denominator(100)
                expresion = str(constante) if constante != 0 else ""
                for k in range(j + 1, self.columnas - 1):
                    if self.matriz[i, k] == 0:
                        continue

                    coeficiente = -self.matriz[i, k].limit_denominator(100)
                    signo = "+" if coeficiente >= 0 else "-"
                    if expresion:
                        signo = f" {signo} "
                    else:
                        signo = "" if signo == "+" else "-"

                    variable = (
                        f"{abs(coeficiente)}*X{k+1}"
                        if abs(coeficiente) != 1
                        else f"X{k+1}"
                    )

                    expresion += f"{signo}{variable}"

                if expresion == "":
                    expresion = "0"

                ecuaciones.append(f"| X{j+1} = {expresion}\n")
                break

        ecuaciones.sort(key=lambda x: x[3])
        return ecuaciones

    def imprimir_soluciones(self, unica: bool, libres: List[int], validacion: Validacion) -> None:
        solucion, fila_inconsistente = validacion
        if not solucion and fila_inconsistente != -1:
            self.respuesta.append(f"\n| En F{fila_inconsistente+1}: 0 != {str(self.matriz[fila_inconsistente, -1].limit_denominator(100))}\n")
            self.respuesta.append("| Sistema es inconsistente!\n")
            return None

        elif unica:
            solucion_trivial = all(self.matriz[i, -1] == 0 for i in range(self.filas))
            mensaje_solucion = "trivial" if solucion_trivial else "no trivial"

            self.respuesta.append(f"\n| Solución {mensaje_solucion} encontrada:\n")
            for i in range(self.filas):
                if all(x == 0 for x in self.matriz[i]):
                    continue
                self.respuesta.append(f"| X{i+1} = {str(self.matriz[i, -1].limit_denominator(100))}\n")
            return None

        ecuaciones = self.despejar_variables(libres)
        self.respuesta.append("\n| Sistema no tiene solución única!\n")
        self.respuesta.append("| Solución general encontrada:\n")
        for linea in ecuaciones:
            self.respuesta.append(linea)

        return None