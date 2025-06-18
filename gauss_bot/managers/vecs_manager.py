"""
Implementación de VectoresManager.
Almacena vectores, realiza operaciones y retorna resultados.

Operaciones implementadas:
* magnitud (en models/vector.py)
* suma
* resta
* producto escalar
* producto punto
* producto cruz (en models/vector.py)
"""

from fractions import Fraction

from ..models import Vector
from ..utils import (
    format_factor,
    format_proc_num,
)


class VectoresManager:
    """
    Se encarga de almacenar los vectores ingresados por el usuario,
    realizar operaciones con ellos, y retornar los resultados.
    """

    def __init__(self, vecs_ingresados=None) -> None:
        """
        * TypeError: si vecs_ingresados no es un dict[str, Vector]
        """

        if vecs_ingresados is None:
            self.vecs_ingresados: dict[str, Vector] = {}

        elif isinstance(vecs_ingresados, dict) and all(
            isinstance(k, str) and isinstance(v, Vector)
            for k, v in vecs_ingresados.items()
        ):
            self.vecs_ingresados = vecs_ingresados

        else:
            raise TypeError("Argumento inválido para 'vecs_ingresados'!")

    def get_vectores(self, calculado: int) -> str:
        """
        Obtiene los vectores guardados en self.vecs_ingresados
        y los retorna como string.

        - calculado: 0 para no mostrar calculados,
                     1 para mostrar solo calculados,
                    -1 para mostrar todos

        * ValueError: si calculado no estan en (-1, 0, 1)

        Retorna un string con todos los vectores.
        """

        if calculado not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculado'!")
        if not self._validar_vecs_ingresados():
            return "No se ha ingresado ningún vector!"

        if calculado == 1:
            header = "Vectores calculados:"
        elif calculado == 0:
            header = "Vectores ingresados:"
        elif calculado == -1:
            header = "Vectores guardados:"

        vectores = f"\n{header}\n"  # pylint: disable=E0606
        vectores += "---------------------------------------------"
        for nombre, vec in self.vecs_ingresados.items():
            if (
                calculado == 0
                and len(nombre) > 1
                or calculado == 1
                and len(nombre) == 1
            ):
                continue
            vectores += f"\n{nombre}:\n"
            vectores += str(vec) + "\n"
        vectores += "---------------------------------------------\n"

        if "[" not in vectores:
            if calculado == 1:
                return "No se ha calculado ningún vector!"
            if calculado == 0:
                return "No se ha ingresado ningún vector!"
        return vectores

    def suma_resta_vecs(
        self, operacion: bool, nombre_vec1: str, nombre_vec2: str
    ) -> tuple[str, str, Vector]:
        """
        Suma o resta los dos vectores indicados, dependiendo del
        argumento 'operacion'. True para sumar, False para restar.
        * ArithmeticError: si los vectores no tienen las mismas dimensiones

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre del vector resultante (e.g. 'u + v')
        * Vector(): objeto vector resultante de la operación
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
            componentes=[
                f"{
                    format_proc_num(  # type: ignore
                        (
                            vec1[i].limit_denominator(1000),
                            vec2[i].limit_denominator(1000),
                        ),
                        operador=operador,  # type: ignore
                    )
                }"
                for i in range(len(vec1))
            ],
        )

        proc = "---------------------------------------------\n"
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
        Multiplica un vector por un escalar.

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre del vector resultante (e.g. '2u')
        * Vector(): objeto vector resultante de la operación
        """

        vec = self.vecs_ingresados[nombre_vec]
        vec_multiplicado = vec * escalar

        escalar_str = format_factor(escalar)
        nombre_vec_multiplicado = f"{escalar_str}{nombre_vec}"

        vec_proc = Vector(
            componentes=[
                f"{
                    format_proc_num(  # type: ignore
                        (escalar, vec[i].limit_denominator(1000))
                    )
                }"
                for i in range(len(vec))
            ]
        )

        proc = "---------------------------------------------\n"
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
        Calcula el producto punto de los dos vectores indicados.
        * ArithmeticError: si los vectores no tienen la misma dimensión.

        Retorna una tupla con:
        * str: procedimiento de la operación realizada
        * str: nombre del producto punto (e.g. 'u.v')
        * Fraction(): resultado del producto punto
        """

        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        prod_punto = vec1 * vec2
        nombre_prod_punto = f"{nombre_vec1}.{nombre_vec2}"

        vec1_proc = Vector(
            componentes=[
                f"{
                    format_factor(  # type: ignore
                        vec1[i].limit_denominator(1000),
                        mult=False,
                    )
                }"
                for i in range(len(vec1))
            ]
        )

        vec2_proc = Vector(
            componentes=[
                f"{
                    format_factor(  # type: ignore
                        vec2[i].limit_denominator(1000),
                        mult=False,
                    )
                }"
                for i in range(len(vec2))
            ]
        )

        pp_proc = Vector(
            componentes=[
                f"{
                    format_proc_num(  # type: ignore
                        (
                            vec1[i].limit_denominator(1000),
                            vec2[i].limit_denominator(1000),
                        ),
                    )
                }"
                for i in range(len(vec1))
            ]
        )

        proc = "---------------------------------------------\n"
        proc += f"{nombre_vec1}:\n{vec1_proc}\n\n"
        proc += f"{nombre_vec2}:\n{vec2_proc}\n"
        proc += "---------------------------------------------\n"
        proc += "Para calcular el producto punto de dos vectores,\n"
        proc += "se debe sumar el producto de sus componentes.\n\n"

        proc += f"{nombre_prod_punto}  =\n"
        proc += f"{'\n+\n'.join(c for c in pp_proc.componentes)}\n"  # type: ignore
        proc += "---------------------------------------------\n"
        proc += f"{nombre_prod_punto}  =  {prod_punto}"

        return (proc, nombre_prod_punto, prod_punto)

    def _validar_vecs_ingresados(self) -> bool:
        """
        Valida si el diccionario de vectores ingresados esta vacío o no.
        """

        if self.vecs_ingresados == {}:
            return False
        return True
