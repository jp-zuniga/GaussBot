"""
Implementación de VectoresManager.
Almacena vectores, realiza operaciones y retorna resultados.
"""

from fractions import Fraction

from src import FRAC_PREC
from src.models import Vector
from src.utils import format_factor, format_proc_num


class VectoresManager:
    """
    Manager de los vectores de la aplicación.
    Valida y almacena los vectores ingresados por el usuario,
    realiza operaciones con ellas, y retorna sus resultados.
    """

    def __init__(self, vecs_ingresados: dict[str, Vector] | None = None) -> None:
        """
        Args:
            vecs_ingresados: Diccionario de vectores.

        Raises:
            TypeError: Si vecs_ingresados no es un dict[str, Vector].

        """

        if vecs_ingresados is None:
            self.vecs_ingresados: dict[str, Vector] = {}
        elif isinstance(vecs_ingresados, dict) and all(
            isinstance(k, str) and isinstance(v, Vector)
            for k, v in vecs_ingresados.items()
        ):
            self.vecs_ingresados = vecs_ingresados
        else:
            raise TypeError("Argumento inválido para 'vecs_ingresados'.")

    def get_vectores(self, calculado: int) -> str:
        """
        Formatear los vectores guardados como un solo string.

        Args:
            calculado: Bandera para indicar cuales vectores mostrar.

        Raises:
            ValueError: Si calculado no -1, 0 o 1.

        Returns:
            str: String que contiene todos los vectores.

        """

        if calculado not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculado'.")
        if not self._validar_vecs_ingresados():
            return "¡No se ha ingresado ningún vector!"

        if calculado == 1:
            header: str = "Vectores calculados:"
        elif calculado == 0:
            header: str = "Vectores ingresados:"
        elif calculado == -1:
            header: str = "Vectores guardados:"

        vectores: str = f"\n{header}\n"
        vectores += "---------------------------------------------"
        for nombre, vec in self.vecs_ingresados.items():
            if (calculado == 0 and len(nombre) > 1) or (
                calculado == 1 and len(nombre) == 1
            ):
                continue
            vectores += f"\n{nombre}:\n"
            vectores += str(vec) + "\n"
        vectores += "---------------------------------------------\n"

        if "[" not in vectores:
            if calculado == 1:
                return "¡No se ha calculado ningún vector!"
            if calculado == 0:
                return "¡No se ha ingresado ningún vector!"
        return vectores

    def suma_resta_vecs(
        self,
        operacion: bool,
        nombre_vec1: str,
        nombre_vec2: str,
    ) -> tuple[str, str, Vector]:
        """
        Sumar o restar los dos vectores indicados.

        Args:
            operacion:   True para sumar, False para restar.
            nombre_vec1: Nombre del primer vector.
            nombre_vec2: Nombre del segunda vector.

        Raises:
            ArithmeticError: Si los vectores no tienen las mismas dimensiones.

        Returns:
            (str, str, Vector): Procedimiento de la operación realizada,
                                nombre del vector resultante (e.g. 'u + v') y
                                vector resultante de la operación.

        """

        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        if operacion:
            vec_resultado = vec1 + vec2
            operador = "+"
        else:
            vec_resultado = vec1 - vec2
            operador = "−"
        nombre_vec_resultado = f"{nombre_vec1} {operador} {nombre_vec2}"

        vec_proc = Vector(
            componentes=[  # type: ignore[reportArgumentType]
                f"{
                    format_proc_num(
                        (
                            vec1[i].limit_denominator(FRAC_PREC['prec']),
                            vec2[i].limit_denominator(FRAC_PREC['prec']),
                        ),
                        operador=operador,
                    )
                }"
                for i in range(len(vec1))
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_vec1}:\n{vec1}\n\n"
        proc += f"{nombre_vec2}:\n{vec2}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_vec_resultado}:\n{vec_proc}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_vec_resultado}:\n{vec_resultado}"

        return (proc, nombre_vec_resultado, vec_resultado)

    def escalar_por_vec(
        self,
        escalar: Fraction,
        nombre_vec: str,
    ) -> tuple[str, str, Vector]:
        """
        Multiplicar el vector indicada por el escalar especificado.

        Args:
            escalar:    Número por el cual multiplicar el vector.
            nombre_vec: Nombre del vector a multiplicar.

        Returns:
            (str, str, Vector): Procedimiento de la operación realizada,
                                nombre del vector resultante (e.g. '2u') y
                                vector resultante de la operación.

        """

        vec = self.vecs_ingresados[nombre_vec]
        vec_multiplicado = vec * escalar

        escalar_str = format_factor(escalar)
        nombre_vec_multiplicado = f"{escalar_str}{nombre_vec}"

        vec_proc = Vector(
            componentes=[  # type: ignore[reportArgumentType]
                f"{
                    format_proc_num(
                        (escalar, vec[i].limit_denominator(FRAC_PREC['prec']))
                    )
                }"
                for i in range(len(vec))
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_vec}:\n{vec}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_vec_multiplicado}:\n{vec_proc}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_vec_multiplicado}:\n{vec_multiplicado}"

        return (proc, nombre_vec_multiplicado, vec_multiplicado)

    def producto_punto(
        self,
        nombre_vec1: str,
        nombre_vec2: str,
    ) -> tuple[str, str, Fraction]:
        """
        Calcular el producto punto de los dos vectores indicados.

        Args:
            nombre_vec1: Nombre del primer vector.
            nombre_vec2: Nombre del segunda vector.

        Raises:
            ArithmeticError: Si los vectores no tienen las mismas dimensiones.

        Returns:
            (str, str, Fraction): Procedimiento de la operación realizada,
                                nombre del producto punto (e.g. 'u + v') y
                                vresultado de la operación.

        """

        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        prod_punto = vec1 * vec2
        nombre_prod_punto = f"{nombre_vec1}.{nombre_vec2}"

        vec1_proc = Vector(
            componentes=[  # type: ignore[reportArgumentType]
                f"{
                    format_factor(
                        vec1[i].limit_denominator(FRAC_PREC['prec']), mult=False
                    )
                }"
                for i in range(len(vec1))
            ],
        )

        vec2_proc = Vector(
            componentes=[  # type: ignore[reportArgumentType]
                f"{
                    format_factor(
                        vec2[i].limit_denominator(FRAC_PREC['prec']), mult=False
                    )
                }"
                for i in range(len(vec2))
            ],
        )

        pp_proc = Vector(
            componentes=[  # type: ignore[reportArgumentType]
                f"{
                    format_proc_num(
                        (
                            vec1[i].limit_denominator(FRAC_PREC['prec']),
                            vec2[i].limit_denominator(FRAC_PREC['prec']),
                        )
                    )
                }"
                for i in range(len(vec1))
            ],
        )

        proc: str = "---------------------------------------------\n"
        proc += f"{nombre_vec1}:\n{vec1_proc}\n\n"
        proc += f"{nombre_vec2}:\n{vec2_proc}\n"
        proc += "---------------------------------------------\n"
        proc += "Para calcular el producto punto de dos vectores,\n"
        proc += "se debe sumar el producto de sus componentes.\n\n"

        proc += f"{nombre_prod_punto}  =\n"
        proc += f"{'\n+\n'.join(str(c) for c in pp_proc.componentes)}\n"
        proc += "---------------------------------------------\n"
        proc += f"{nombre_prod_punto}  =  {prod_punto}"

        return (proc, nombre_prod_punto, prod_punto)

    def _validar_vecs_ingresados(self) -> bool:
        """
        Valida si el diccionario de vectores ingresados esta vacío o no.
        """

        return self.vecs_ingresados != {}
