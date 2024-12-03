"""
Implementación de MatricesManager.
Almacena matrices, realiza operaciones, retorna resultados.

Operaciones implementadas:
* suma
* resta
* multiplicación por escalar
* multiplicación matricial
* transposiciones
* calcular determinante
* encontrar inversas
"""

from fractions import Fraction
from ..util_funcs import (
    format_factor,
    format_proc_num,
)

from ..models import (
    Matriz,
    SistemaEcuaciones,
)


class MatricesManager:
    """
    Se encarga de almacenar las matrices ingresadas por el usuario,
    realizar operaciones con ellas, y retornar los resultados.
    """

    def __init__(self, mats_ingresadas=None, sis_ingresados=None) -> None:
        """
        * TypeError: si mats_ingresadas/sis_ingresados no son un dict[str, Matriz]
        """

        if mats_ingresadas is None:
            self.mats_ingresadas: dict[str, Matriz] = {}

        elif (
              isinstance(mats_ingresadas, dict)
              and
              all(
                isinstance(k, str) and isinstance(v, Matriz)
                for k, v in mats_ingresadas.items()
            )
        ):
            self.mats_ingresadas = mats_ingresadas

        else:
            raise TypeError("Argumento inválido para 'mats_ingresadas'!")

        if sis_ingresados is None:
            self.sis_ingresados: dict[str, Matriz] = {}

        elif (
              isinstance(sis_ingresados, dict)
              and
              all(
                isinstance(k, str) and isinstance(v, Matriz)
                for k, v in sis_ingresados.items()
            )
        ):
            self.sis_ingresados = sis_ingresados

        else:
            raise TypeError("Argumento inválido para 'sis_ingresados'!")

    def get_matrices(self, calculada: int) -> str:
        """
        Obtiene las matrices guardadas en self.mats_ingresadas
        y las retorna como string.

        - calculada: 0 para no mostrar matrices calculadas,
                     1 para mostrar solo matrices calculadas,
                    -1 para mostrar todas las matrices guardadas

        * ValueError: si calculada no esta en (-1, 0, 1)

        Retorna un string con todas las matrices.
        """

        if calculada not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculada'!")
        if not self._validar_mats_ingresadas():
            return "No se ha guardado ninguna matriz!"

        if calculada == 1:
            header = "Matrices calculadas:"
        elif calculada == 0:
            header = "Matrices ingresadas:"
        elif calculada == -1:
            header = "Matrices guardadas:"

        matrices = f"\n{header}\n"  # pylint: disable=E0606
        matrices += "---------------------------------------------"
        for nombre, mat in self.mats_ingresadas.items():
            if (
                calculada == 0 and len(nombre) > 1
                or
                calculada == 1 and len(nombre) == 1
            ):
                continue
            matrices += f"\n{nombre}:\n"
            matrices += str(mat) + "\n"
        matrices += "---------------------------------------------\n"

        if "(" not in matrices:
            if calculada == 1:
                return "No se ha calculado ninguna matriz!"
            if calculada == 0:
                return "No se ha ingresado ninguna matriz!"
        return matrices

    def get_sistemas(self, calculado: int) -> str:
        """
        Obtiene las sistemas guardados en self.sis_ingresados
        y las retorna como string.

        - calculado: 0 para no mostrar sistemas calculados,
                     1 para mostrar solo sistemas calculados,
                    -1 para mostrar todas las sistemas guardados

        * ValueError: si calculado no esta en (-1, 0, 1)

        Retorna un string con todos las sistemas.
        """

        if calculado not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculado'!")
        if not self._validar_sis_ingresados():
            return "No se ha guardado ningún sistema de ecuaciones!"

        if calculado == 1:
            header = "Sistemas calculados:"
        elif calculado == 0:
            header = "Sistemas ingresados:"
        elif calculado == -1:
            header = "Sistemas guardados:"

        sistemas = f"\n{header}\n"  # pylint: disable=E0606
        sistemas += "---------------------------------------------"
        for nombre, sis in self.sis_ingresados.items():
            if (
                calculado == 0 and len(nombre) > 1
                or
                calculado == 1 and len(nombre) == 1
            ):
                continue
            sistemas += f"\n{nombre}:\n"
            sistemas += str(sis) + "\n"
        sistemas += "---------------------------------------------\n"

        if "(" not in sistemas:
            if calculado == 1:
                return "No se ha resuelto ningún sistema de ecuaciones!"
            if calculado == 0:
                return "No se ha ingresado ningún sistema de ecuaciones!"
        return sistemas

    def resolver_sistema(self, nombre_sis: str, metodo: str) -> SistemaEcuaciones:
        """
        Resuelve un sistema de ecuaciones representado por la matriz ingresada.
        * nombre_sis: nombre de la matriz que representa el sistema de ecuaciones
        * metodo: método a utilizar para resolver el sistema ("gj" o "c")

        Retorna:
        * SistemaEcuaciones: objeto SistemaEcuaciones después de resolver el sistema
        """

        sistema = SistemaEcuaciones(self.sis_ingresados[nombre_sis])

        if metodo == "gj":
            sistema.gauss_jordan()
        elif metodo == "c":
            sistema.cramer(nombre_sis)
        else:
            raise ValueError("Argumento inválido para 'metodo'!")

        return sistema

    def suma_resta_mats(
        self,
        operacion: bool,
        nombre_mat1: str,
        nombre_mat2: str
    ) -> tuple[str, str, Matriz]:

        """
        Suma o resta las dos matrices indicadas, dependiendo del
        argumento 'operacion'. True para sumar, False para restar.
        * ArithmeticError: si las matrices no tienen las mismas dimensiones

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre de la matriz resultante (e.g. 'A + B')
        * Matriz(): objeto matriz resultante de la operación
        """

        mat1 = self.mats_ingresadas[nombre_mat1]
        mat2 = self.mats_ingresadas[nombre_mat2]

        if operacion:
            mat_resultado = mat1 + mat2
            operador = "+"
        else:
            mat_resultado = mat1 - mat2
            operador = "−"
        nombre_mat_resultado = f"{nombre_mat1} {operador} {nombre_mat2}"

        mat_proc = Matriz(
            aumentada=False,
            filas=mat1.filas,
            columnas=mat1.columnas,
            valores=[
                [
                    f"{format_proc_num(  # type: ignore
                        (
                            mat1[f, c].limit_denominator(1000),
                            mat2[f, c].limit_denominator(1000),
                        ),
                        operador=operador,  # type: ignore
                    )}"
                    for c in range(mat1.columnas)
                ]
                for f in range(mat1.filas)
            ],
        )

        proc  =  "---------------------------------------------\n"
        proc += f"{nombre_mat1}:\n{mat1}\n\n"
        proc += f"{nombre_mat2}:\n{mat2}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_resultado}:\n{mat_proc}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_resultado}:\n{mat_resultado}"

        return (proc, nombre_mat_resultado, mat_resultado)

    def escalar_por_mat(
        self,
        escalar: Fraction,
        nombre_mat: str
    ) -> tuple[str, str, Matriz]:

        """
        Realiza multiplicación escalar con
        la matriz y el escalar indicados.

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre de la matriz resultante (e.g. 'kA')
        * Matriz(): objeto matriz resultante de la operación
        """

        mat = self.mats_ingresadas[nombre_mat]
        mat_mult = mat * escalar

        escalar_str = format_factor(escalar)
        nombre_mat_mult = f"{escalar_str}{nombre_mat}"

        mat_proc = Matriz(
            aumentada=False,
            filas=mat.filas,
            columnas=mat.columnas,
            valores=[
                [
                    f"{format_proc_num(  # type: ignore
                        (
                            escalar,
                            mat[f, c].limit_denominator(1000),
                        )
                    )}"
                    for c in range(mat.columnas)
                ]
                for f in range(mat.filas)
            ]
        )

        proc  =  "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_proc}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_mult}"

        return (proc, nombre_mat_mult, mat_mult)

    def mult_mats(
        self,
        nombre_mat1: str,
        nombre_mat2: str
    ) -> tuple[str, str, Matriz]:

        """
        Multiplica las matrices indicadas.
        * ArithmeticError: si las matrices no son compatibles para multiplicación

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre de la matriz resultante (e.g. 'A • B')
        * Matriz(): objeto matriz resultante de la operación
        """

        mat1 = self.mats_ingresadas[nombre_mat1]
        mat2 = self.mats_ingresadas[nombre_mat2]

        mat_mult = mat1 * mat2
        nombre_mat_mult = f"{nombre_mat1} • {nombre_mat2}"

        mat_proc = Matriz(
            aumentada=False,
            filas=mat1.filas,
            columnas=mat2.columnas,
            valores=[
                [
                    " + ".join(  # type: ignore
                        f"{format_proc_num(  # type: ignore
                            (
                                mat1[i, k].limit_denominator(1000),
                                mat2[k, j].limit_denominator(1000),
                            )
                        )}"
                        for k in range(mat1.columnas)
                    )
                    for j in range(mat2.columnas)
                ]
                for i in range(mat1.filas)
            ]
        )

        proc  =  "---------------------------------------------\n"
        proc += f"{nombre_mat1}:\n{mat1}\n\n"
        proc += f"{nombre_mat2}:\n{mat2}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_proc}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_mult}"

        return (proc, nombre_mat_mult, mat_mult)

    def calcular_determinante(self, nombre_mat: str) -> tuple[str, str, Fraction]:
        """
        Calcula el determinante de la matriz indicada.
        * ArithmeticError: si la matriz no es cuadrada

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: header de la operacion (e.g. '|  A  |')
        * Fraction: determinante de la matriz
        """

        mat = self.mats_ingresadas[nombre_mat]

        used_det_formula = mat.filas <=2 and mat.columnas <= 2
        if used_det_formula:
            det: Fraction = mat.calcular_det()  # type: ignore
        else:
            det, mat_triangular, intercambio = mat.calcular_det()  # type: ignore

        proc  =  "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc +=  "---------------------------------------------\n"

        if used_det_formula:
            proc +=  "El determinante de una matriz 2x2 se calcula con la fórmula:\n"
            proc +=  "ad - bc\n\n"
            proc += f"|  {nombre_mat}  |  =  "
            proc += f"{format_proc_num(
                (
                    mat[0, 0].limit_denominator(1000),
                    mat[1, 1].limit_denominator(1000),
                )
            )} − {format_proc_num(
                (
                    mat[0, 1].limit_denominator(1000),
                    mat[1, 0].limit_denominator(1000),
                )
            )}\n"

        else:
            proc +=  "El determinante de una matriz nxn (n > 2) se puede calcular\n"
            proc +=  "transformando la matriz en una matriz triangular superior,\n"
            proc +=  "y multiplicando todos elementos de la diagonal principal.\n\n"

            proc += f"Matriz triangular superior:\n{mat_triangular}\n\n"
            proc += f"|  {nombre_mat}  |  =  "

            diagonales = " • ".join(
                format_factor(
                    mat_triangular[i, i].limit_denominator(1000),
                    mult=False,
                    parenth_negs=True,
                    skip_ones=False,
                ) for i in range(mat_triangular.filas)
            )

            proc += f"[ {diagonales} ]\n"

        proc +=  "---------------------------------------------\n"
        proc += f"|  {nombre_mat}  |  =  "
        proc += f"{det if not used_det_formula and not intercambio else -det}"  # pylint: disable=E0606

        if not used_det_formula and intercambio:
            proc += "\n\n"
            proc += "Como hubo un intercambio de filas al "
            proc += "crear la matriz triangular superior,\n"
            proc += "se debe cambiar el signo del determinante:\n\n"
            proc += f"|  {nombre_mat}  |  =  {det}"

        return (proc, f"|  {nombre_mat}  |", det)

    def transponer_mat(self, nombre_mat: str) -> tuple[str, str, Matriz]:
        """
        Retorna una tupla con el procedimiento de transposición,
        nombre de la matriz transpuesta y el objeto Matriz() transpuesto.
        """

        mat = self.mats_ingresadas[nombre_mat]
        nombre_mat_transpuesta = f"{nombre_mat}_t"
        mat_transpuesta = mat.transponer()

        proc  =  "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc +=  "---------------------------------------------\n"
        proc +=  "Proceso de transposición:\n\n"

        if mat.filas > 5 or mat.columnas > 5:
            proc += f"Para una matriz {mat.filas}x{mat.columnas} como {nombre_mat},\n"
            proc +=  "la i-ésima fila se convierte en la j-ésima columna.\n"
            proc += f"\nPor lo tanto, la transposición de {nombre_mat} sería de "
            proc += f"{mat.columnas}x{mat.filas}.\n"

        else:
            for i in range(mat.filas):
                proc += f"− La fila {i + 1} se convierte en la columna {i + 1}\n"

            if mat.filas != mat.columnas:
                proc += f"\nLa transposición de {nombre_mat} sería "
                proc += f"de {mat.columnas}x{mat.filas}.\n"

        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_transpuesta}:\n{mat_transpuesta}"

        return (proc, nombre_mat_transpuesta, mat_transpuesta)

    def invertir_mat(
        self,
        nombre_mat: str
    ) -> tuple[str, str, "Matriz"]:

        """
        Encuentra la inversa de la matriz indicada.
        * ArithmeticError: si la matriz no es cuadrada
        * ZeroDivisionError: si el determinante es 0

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre de la matriz inversa (e.g. 'A_i')
        * Matriz(): objeto de la matriz inversa

        Cuando se necesita el procedimiento, se utiliza toda la tupla,
        pero si solo se desea la inversa, se pueden descartar los otros elementos:
        * _, inversa, _, _ = MatricesManager().invertir_matriz(nombre_mat)
        """

        mat = self.mats_ingresadas[nombre_mat]
        nombre_mat_invertida = f"{nombre_mat}_i"
        inversa, adjunta, det = mat.invertir()

        proc  =  "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"Matriz de cofactores de {nombre_mat}:\n{adjunta.transponer()}\n\n"
        proc += f"adj ({nombre_mat}):\n{adjunta}\n\n"
        proc += f"|  {nombre_mat}  |  =  {det}\n"
        proc +=  "---------------------------------------------\n"
        proc += f"{nombre_mat_invertida} = adj ({nombre_mat}) / det ({nombre_mat})\n\n"
        proc += f"{nombre_mat_invertida}:\n{inversa}"

        return (proc, nombre_mat_invertida, inversa)

    def _validar_mats_ingresadas(self) -> bool:
        """
        Valida si el diccionario de matrices ingresadas esta vacío o no.
        """

        if self.mats_ingresadas == {}:
            return False
        return True

    def _validar_sis_ingresados(self) -> bool:
        """
        Valida si el diccionario de sistemas de ecuaciones ingresados esta vacío o no.
        """

        if self.sis_ingresados == {}:
            return False
        return True
