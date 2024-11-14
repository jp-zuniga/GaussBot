"""
Implementación de MatricesManager.
Almacena matrices, realiza operaciones, retorna resultados.

Operaciones implementadas:
* suma
* resta
* multiplicación por escalar
* multiplicación matricial
* transponer
* calcular determinante
* invertir
"""

from fractions import Fraction

from gauss_bot.models import (
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
              isinstance(mats_ingresadas, dict) and
              all(isinstance(n, str) for n in mats_ingresadas.keys()) and
              all(isinstance(m, Matriz) for m in mats_ingresadas.values())
        ):
            self.mats_ingresadas = mats_ingresadas
        else:
            raise TypeError("Argumento inválido para 'mats_ingresadas'!")

        if sis_ingresados is None:
            self.sis_ingresados: dict[str, Matriz] = {}
        elif (
              isinstance(sis_ingresados, dict) and
              all(isinstance(n, str) for n in sis_ingresados.keys()) and
              all(isinstance(m, Matriz) for m in sis_ingresados.values())
        ):
            self.sis_ingresados = sis_ingresados
        else:
            raise TypeError("Argumento inválido para 'sis_ingresados'!")

    def get_matrices(self, calculada: int) -> str:
        """
        Obtiene las matrices guardadas en self.mats_ingresadas y las retorna como string.
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

        matrices = f"{header}\n"  # pylint: disable=possibly-used-before-assignment
        matrices += "---------------------------------------------"
        for nombre, mat in self.mats_ingresadas.items():
            if (
                calculada == 0 and len(nombre) > 1
                or
                calculada == 1 and len(nombre) == 1
            ):
                continue
            matrices += f"\n{nombre}:\n"
            matrices += str(mat)
        matrices += "---------------------------------------------"

        if "(" not in matrices:
            if calculada == 1:
                return "No se ha calculado ninguna matriz!"
            if calculada == 0:
                return "No se ha ingresado ninguna matriz!"
        return matrices

    def get_sistemas(self, calculado: int) -> str:
        """
        Obtiene las sistemas guardados en self.sis_ingresados y las retorna como string.
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

        sistemas = f"{header}\n"  # pylint: disable=possibly-used-before-assignment
        sistemas += "---------------------------------------------"
        for nombre, sis in self.sis_ingresados.items():
            if (
                calculado == 0 and len(nombre) > 1
                or
                calculado == 1 and len(nombre) == 1
            ):
                continue
            sistemas += f"\n{nombre}:\n"
            sistemas += str(sis)
        sistemas += "---------------------------------------------"

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
    ) -> tuple[str, Matriz]:

        """
        Suma o resta las dos matrices indicadas, dependiendo del
        argumento 'operacion'. True para sumar, False para restar.
        * ArithmeticError: si las matrices no tienen las mismas dimensiones

        Retorna una tupla con:
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
        return (nombre_mat_resultado, mat_resultado)

    def escalar_por_matriz(
        self,
        escalar: Fraction,
        nombre_mat: str
    ) -> tuple[str, Matriz]:

        """
        Realiza multiplicación escalar con
        la matriz y el escalar indicados.

        Retorna una tupla con:
        * str: nombre de la matriz resultante (e.g. 'kA')
        * Matriz(): objeto matriz resultante de la operación
        """

        mat = self.mats_ingresadas[nombre_mat]
        mat_mult = mat * escalar

        # formatear el escalar para el nombre
        if escalar == Fraction(1):
            escalar_str = ""
        elif escalar == Fraction(-1):
            escalar_str = "−"
        elif escalar.is_integer():
            escalar_str = str(escalar)
        else:
            escalar_str = f"({escalar}) • "

        nombre_mat_mult = f"{escalar_str}{nombre_mat}"
        return (nombre_mat_mult, mat_mult)

    def mult_matricial(
        self,
        nombre_mat1: str,
        nombre_mat2: str
    ) -> tuple[str, Matriz]:

        """
        Multiplica las matrices indicadas.
        * ArithmeticError: si las matrices no son compatibles para multiplicación

        Retorna una tupla con:
        * str: nombre de la matriz resultante (e.g. 'A • B')
        * Matriz(): objeto matriz resultante de la operación
        """

        mat1 = self.mats_ingresadas[nombre_mat1]
        mat2 = self.mats_ingresadas[nombre_mat2]

        mat_mult = mat1 * mat2
        nombre_mat_mult = f"{nombre_mat1} • {nombre_mat2}"
        return (nombre_mat_mult, mat_mult)

    def transponer_matriz(self, nombre_mat: str) -> tuple[str, Matriz]:
        """
        Retorna una tupla con el nombre de la
        transposición y el objeto Matriz() transpuesto.
        """

        mat = self.mats_ingresadas[nombre_mat]
        nombre_mat_transpuesta = f"{nombre_mat}_t"
        mat_transpuesta = mat.transponer()
        return (nombre_mat_transpuesta, mat_transpuesta)

    def invertir_matriz(
        self,
        nombre_mat: str
    ) -> tuple[str, "Matriz", "Matriz", Fraction]:

        """
        Encuentra la inversa de la matriz indicada.
        * ArithmeticError: si la matriz no es cuadrada
        * ZeroDivisionError: si el determinante es 0

        Retorna una tupla con:
        * str: nombre de la matriz inversa (e.g. 'A_i')
        * Matriz(): objeto de la matriz inversa
        * Matriz(): objeto de la matriz adjunta
        * Fraction(): determinante de la matriz

        Cuando se necesita el procedimiento, se utiliza toda la tupla,
        pero si solo se desea la inversa, se pueden descartar los otros elementos:
        * _, inversa, _, _ = MatricesManager().invertir_matriz(nombre_mat)
        """

        mat = self.mats_ingresadas[nombre_mat]
        nombre_mat_invertida = f"{nombre_mat}_i"
        inversa, adjunta, det = mat.invertir()
        return (nombre_mat_invertida, inversa, adjunta, det)

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
