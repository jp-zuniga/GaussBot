"""
Implementación de manejador de matrices.
"""

from fractions import Fraction
from typing import Literal

from src.models import Matriz, SistemaEcuaciones
from src.utils import format_factor, format_proc_num


class MatricesManager:
    """
    Manager de las matrices de la aplicación.
    Valida y almacena las matrices ingresadas por el usuario,
    realiza operaciones con ellas, y retorna sus resultados.
    """

    def __init__(
        self,
        mats_ingresadas: dict[str, Matriz] | None = None,
        sis_ingresados: dict[str, Matriz] | None = None,
    ) -> None:
        """
        Args:
            mats_ingresadas: Diccionario de matrices.
            sis_ingresados:  Diccionario de sistemas de ecuaciones.

        Raises:
            TypeError: Si mats_ingresadas o sis_ingresados no son un dict[str, Matriz].

        """

        if mats_ingresadas is None:
            self.mats_ingresadas: dict[str, Matriz] = {}
        elif isinstance(mats_ingresadas, dict) and all(
            isinstance(k, str) and isinstance(v, Matriz)
            for k, v in mats_ingresadas.items()
        ):
            self.mats_ingresadas = mats_ingresadas
        else:
            raise TypeError("Argumento inválido para 'mats_ingresadas'.")

        if sis_ingresados is None:
            self.sis_ingresados: dict[str, Matriz] = {}
        elif isinstance(sis_ingresados, dict) and all(
            isinstance(k, str) and isinstance(v, Matriz)
            for k, v in sis_ingresados.items()
        ):
            self.sis_ingresados = sis_ingresados
        else:
            raise TypeError("Argumento inválido para 'sis_ingresados'.")

    def get_matrices(self, calculada: Literal[-1, 0, 1]) -> str:
        """
        Formatear las matrices guardadas como un solo string.

        Args:
            calculada: Bandera para indicar cuales matrices mostrar.

        Raises:
            ValueError: Si calculada no -1, 0 o 1.

        Returns:
            str: String que contiene todas las matrices.

        """

        if calculada not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculada'.")
        if not self._validar_mats_ingresadas():
            return "¡No se ha guardado ninguna matriz!"

        if calculada == 1:
            header: str = "Matrices calculadas:"
        elif calculada == 0:
            header: str = "Matrices ingresadas:"
        else:
            header: str = "Matrices guardadas:"

        matrices = f"\n{header}\n"
        matrices += "---------------------------------------------"
        for nombre, mat in self.mats_ingresadas.items():
            if (calculada == 0 and len(nombre) > 1) or (
                calculada == 1 and len(nombre) == 1
            ):
                continue
            matrices += f"\n{nombre}:\n"
            matrices += str(mat) + "\n"
        matrices += "---------------------------------------------\n"

        return (
            matrices
            if "[" in matrices
            else f"¡No se ha {
                'calculado' if calculada == 1 else 'ingresado'
            } ninguna matriz!"
        )

    def get_sistemas(self, calculado: Literal[-1, 0, 1]) -> str:
        """
        Formatear los sistemas guardados como un solo string.

        Args:
            calculado: Bandera para indicar cuales sistemas mostrar.

        Raises:
            ValueError: Si calculada no -1, 0 o 1.

        Returns:
            str: String que contiene todos los sistemas.

        """

        if calculado not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculado'.")
        if not self._validar_sis_ingresados():
            return "¡No se ha guardado ningún sistema de ecuaciones!"

        if calculado == 0:
            header: str = "Sistemas ingresados:"
        elif calculado == 1:
            header: str = "Sistemas calculados:"
        else:
            header: str = "Sistemas guardados:"

        sistemas = f"\n{header}\n"
        sistemas += "---------------------------------------------"
        for nombre, sis in self.sis_ingresados.items():
            if (calculado == 0 and len(nombre) > 1) or (
                calculado == 1 and len(nombre) == 1
            ):
                continue
            sistemas += f"\n{nombre}:\n"
            sistemas += str(sis) + "\n"
        sistemas += "---------------------------------------------\n"

        return (
            sistemas
            if "[" in sistemas
            else f"¡No se ha {
                'calculado' if calculado == 1 else 'ingresado'
            } ningún sistema!"
        )

    def resolver_sistema(self, nombre_sis: str, metodo: str) -> SistemaEcuaciones:
        """
        Resolver un sistema con el método indicado.

        Args:
            nombre_sis: Nombre de la matriz que representa el sistema de ecuaciones.
            metodo:     Método a utilizar para resolver el sistema ("gj" o "c").

        Raises:
            ValueError: Si método no es "gj" o "c".

        Returns:
            SistemaEcuaciones: objeto con el sistema resuelto.

        """

        sistema = SistemaEcuaciones(self.sis_ingresados[nombre_sis])

        if metodo == "gj":
            sistema.gauss_jordan()
        elif metodo == "c":
            sistema.cramer(nombre_sis)
        else:
            raise ValueError("Argumento inválido para 'metodo'.")

        return sistema

    def suma_resta_mats(
        self,
        operacion: bool,
        nombre_mat1: str,
        nombre_mat2: str,
    ) -> tuple[str, str, Matriz]:
        """
        Sumar o restar las dos matrices indicadas.

        Args:
            operacion:   True para sumar, False para restar.
            nombre_mat1: Nombre de la primer matriz.
            nombre_mat2: Nombre de la segunda matriz.

        Raises:
            ArithmeticError: Si las matrices no tienen las mismas dimensiones.

        Returns:
            (str, str, Matriz): Procedimiento de la operación realizada,
                                nombre de la matriz resultante (e.g. 'A + B') y
                                matriz resultante de la operación.

        """

        mat1: Matriz = self.mats_ingresadas[nombre_mat1]
        mat2: Matriz = self.mats_ingresadas[nombre_mat2]

        if operacion:
            mat_resultado: Matriz = mat1 + mat2
            operador: str = "+"
        else:
            mat_resultado: Matriz = mat1 - mat2
            operador: str = "−"
        nombre_mat_resultado = f"{nombre_mat1} {operador} {nombre_mat2}"

        mat_proc = Matriz(
            aumentada=False,
            filas=mat1.filas,
            columnas=mat1.columnas,
            valores=[  # type: ignore[reportArgumentType]
                [
                    f"{
                        format_proc_num(
                            (
                                mat1[f, c].limit_denominator(1000),
                                mat2[f, c].limit_denominator(1000),
                            ),
                            operador=operador,
                        )
                    }"
                    for c in range(mat1.columnas)
                ]
                for f in range(mat1.filas)
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat1}:\n{mat1}\n\n"
        proc += f"{nombre_mat2}:\n{mat2}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_resultado}:\n{mat_proc}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_resultado}:\n{mat_resultado}"

        return (proc, nombre_mat_resultado, mat_resultado)

    def escalar_por_mat(
        self,
        escalar: Fraction,
        nombre_mat: str,
    ) -> tuple[str, str, Matriz]:
        """
        Multiplicar la matriz indicada por el escalar especificado.

        Args:
            escalar:    Número por el cual multiplicar la matriz.
            nombre_mat: Nombre de la matriz a multiplicar.

        Returns:
            (str, str, Matriz): Procedimiento de la operación realizada,
                                nombre de la matriz resultante (e.g. 'kA') y
                                matriz resultante de la operación.

        """

        mat: Matriz = self.mats_ingresadas[nombre_mat]
        mat_mult: Matriz = mat * escalar

        escalar_str = format_factor(escalar)
        nombre_mat_mult = f"{escalar_str}{nombre_mat}"

        mat_proc = Matriz(
            filas=mat.filas,
            columnas=mat.columnas,
            valores=[  # type: ignore[reportArgumentType]
                [
                    f"{format_proc_num((escalar, mat[f, c].limit_denominator(1000)))}"
                    for c in range(mat.columnas)
                ]
                for f in range(mat.filas)
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_proc}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_mult}"

        return (proc, nombre_mat_mult, mat_mult)

    def mult_mats(self, nombre_mat1: str, nombre_mat2: str) -> tuple[str, str, Matriz]:
        """
        Multiplicar las matrices indicadas.

        Args:
            nombre_mat1: Nombre de la primer matriz.
            nombre_mat2: Nombre de la segunda matriz.

        Raises:
            ArithmeticError: Si las matrices no son compatibles para multiplicación.

        Returns:
            (str, str, Matriz): Procedimiento de la operación realizada,
                                nombre de la matriz resultante (e.g. 'A • B') y
                                matriz resultante de la operación.

        """

        nombre_mat_mult = f"{nombre_mat1} • {nombre_mat2}"
        mat1: Matriz = self.mats_ingresadas[nombre_mat1]
        mat2: Matriz = self.mats_ingresadas[nombre_mat2]
        mat_mult: Matriz = mat1 * mat2

        mat_proc = Matriz(
            filas=mat1.filas,
            columnas=mat2.columnas,
            valores=[  # type: ignore[reportArgumentType]
                [
                    " + ".join(
                        f"{
                            format_proc_num(
                                (
                                    mat1[i, k].limit_denominator(1000),
                                    mat2[k, j].limit_denominator(1000),
                                )
                            )
                        }"
                        for k in range(mat1.columnas)
                    )
                    for j in range(mat2.columnas)
                ]
                for i in range(mat1.filas)
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat1}:\n{mat1}\n\n"
        proc += f"{nombre_mat2}:\n{mat2}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_proc}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_mult}:\n{mat_mult}"

        return (proc, nombre_mat_mult, mat_mult)

    def calcular_determinante(self, nombre_mat: str) -> tuple[str, str, Fraction]:
        """
        Calcular el determinante de la matriz indicada.

        Args:
            nombre_mat: Nombre de la matriz.

        Raises:
            ArithmeticError: Si la matriz no es cuadrada.

        Returns:
            (str, str, Fraction): Procedimiento de la operación realizada,
                                  nombre de la matriz resultante (e.g. '| A |') y
                                  determinante de la matriz.

        """

        nombre_det = f"| {nombre_mat} |"
        mat: Matriz = self.mats_ingresadas[nombre_mat]

        used_det_formula: bool = mat.filas <= 2 and mat.columnas <= 2
        if used_det_formula:
            det: Fraction = mat.calcular_det()  # type: ignore[reportAssignmentType]
            intercambio: bool = False
        else:
            det, mat_triangular, intercambio = mat.calcular_det()  # type: ignore[reportGeneralTypeIssues]

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc += "---------------------------------------------\n"

        if used_det_formula:
            proc += "El determinante de una matriz 2x2 se calcula con la fórmula:\n"
            proc += "ad - bc\n\n"
            proc += f"{nombre_det}  =  "
            proc += f"{
                format_proc_num(
                    (
                        mat[0, 0].limit_denominator(1000),
                        mat[1, 1].limit_denominator(1000),
                    )
                )
            } − {
                format_proc_num(
                    (
                        mat[0, 1].limit_denominator(1000),
                        mat[1, 0].limit_denominator(1000),
                    )
                )
            }\n"

        else:
            proc += "El determinante de una matriz nxn (n >= 3) se puede calcular\n"
            proc += "transformando la matriz en una matriz triangular superior,\n"
            proc += "y multiplicando todos elementos de la diagonal principal.\n\n"

            proc += f"Matriz triangular superior:\n{mat_triangular}\n\n"  # type: ignore[reportPossiblyUnboundVariable]
            proc += f"{nombre_det}  =  "

            diagonales: str = " • ".join(
                format_factor(
                    mat_triangular[i, i].limit_denominator(1000),  # type: ignore[reportPossiblyUnboundVariable]
                    mult=False,
                    parenth_negs=True,
                    skip_ones=False,
                )
                for i in range(mat_triangular.filas)  # type: ignore[reportPossiblyUnboundVariable]
            )

            proc += f"[ {diagonales} ]\n"

        proc += "---------------------------------------------\n"
        proc += f"{nombre_det}  =  "
        proc += f"{det if not used_det_formula and not intercambio else -det}"

        if not used_det_formula and intercambio:
            proc += "\n\n"
            proc += "Como hubo un intercambio de filas al "
            proc += "crear la matriz triangular superior,\n"
            proc += "se debe cambiar el signo del determinante:\n\n"
            proc += f"{nombre_det}  =  {det}"

        return (proc, nombre_det, det)

    def transponer_mat(self, nombre_mat: str) -> tuple[str, str, Matriz]:
        """
        Transponer la matriz especificada.

        Args:
            nombre_mat: Nombre de la matriz.

        Returns:
            (str, str, Matriz): Procedimiento de la operación realizada,
                                nombre de la matriz resultante (e.g. 'A_t') y
                                matriz resultante de la operación.

        """

        nombre_mat_transpuesta = f"{nombre_mat}_t"
        mat: Matriz = self.mats_ingresadas[nombre_mat]
        mat_transpuesta: Matriz = mat.transponer()

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc += "---------------------------------------------\n"
        proc += "Proceso de transposición:\n\n"

        if mat.filas > 5 or mat.columnas > 5:
            proc += f"Para una matriz {mat.filas}x{mat.columnas} como {nombre_mat},\n"
            proc += "la i-ésima fila se convierte en la j-ésima columna.\n"
            proc += f"\nPor lo tanto, la transposición de {nombre_mat} sería de "
            proc += f"{mat.columnas}x{mat.filas}.\n"

        else:
            for i in range(mat.filas):
                proc += f"− La fila {i + 1} se convierte en la columna {i + 1}\n"

            if mat.filas != mat.columnas:
                proc += f"\nLa transposición de {nombre_mat} sería "
                proc += f"de {mat.columnas}x{mat.filas}.\n"

        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_transpuesta}:\n{mat_transpuesta}"

        return (proc, nombre_mat_transpuesta, mat_transpuesta)

    def invertir_mat(self, nombre_mat: str) -> tuple[str, str, "Matriz"]:
        """
        Calcular la inversa de la matriz indicada.

        Args:
            nombre_mat: Nombre de la matriz.

        Raises:
            ArithmeticError:   Si la matriz no es cuadrada.
            ZeroDivisionError: Si el determinante es 0.

        Returns:
            (str, str, Matriz): Procedimiento de la operación realizada,
                                nombre de la matriz resultante (e.g. 'A_i') y
                                matriz resultante de la operación.

        """

        nombre_mat_invertida = f"{nombre_mat}_i"
        mat: Matriz = self.mats_ingresadas[nombre_mat]
        inversa, adjunta, det = mat.invertir()

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_mat}:\n{mat}\n"
        proc += "---------------------------------------------\n"
        proc += f"Matriz de cofactores de {nombre_mat}:\n{adjunta.transponer()}\n\n"
        proc += f"adj ({nombre_mat}):\n{adjunta}\n\n"
        proc += f"|  {nombre_mat}  |  =  {det}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_mat_invertida} = adj ({nombre_mat}) / det ({nombre_mat})\n\n"
        proc += f"{nombre_mat_invertida}:\n{inversa}"

        return (proc, nombre_mat_invertida, inversa)

    def _validar_mats_ingresadas(self) -> bool:
        """
        Validar el diccionario de matrices.

        Returns:
            bool: Si el diccionario está vacío o no.

        """

        return self.mats_ingresadas != {}

    def _validar_sis_ingresados(self) -> bool:
        """
        Validar el diccionario de sistemas.

        Returns:
            bool: Si el diccionario está vacío o no.

        """

        return self.sis_ingresados != {}
