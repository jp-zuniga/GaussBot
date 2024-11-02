"""
Implementación de VectoresManager.
Almacena vectores, realiza operaciones y retorna resultados.

Operaciones implementadas:
* suma
* resta
* producto escalar
* producto punto
"""

from fractions import Fraction

from gauss_bot.models.vector import Vector


class VectoresManager:
    """
    Se encarga de almacenar los vectores ingresados por el usuario,
    realizar operaciones con ellos, y retornar los resultados.
    """

    def __init__(self, vecs_ingresados=None) -> None:
        if vecs_ingresados is None:
            self.vecs_ingresados: dict[str, Vector] = {}
        elif (isinstance(vecs_ingresados, dict)
              and all(isinstance(n, str) for n in vecs_ingresados.keys())
              and all(isinstance(v, Vector) for v in vecs_ingresados.values())):
            self.vecs_ingresados = vecs_ingresados
        else:
            raise TypeError("Argumento inválido para 'vecs_ingresados'!")

    def get_vectores(self, calculado: int) -> str:
        """
        Obtiene los vectores guardados en self.vecs_ingresados y los retorna como string.
        - calculado: 0 para no mostrar calculados,
                     1 para mostrar solo calculados,
                    -1 para mostrar todos

        * ValueError: si calculado no estan en (-1, 0, 1)
        """

        if calculado not in (-1, 0, 1):
            raise ValueError("Argumento inválido para 'calculado'!")

        if not self._validar_vecs_ingresados():
            return "No hay vectores ingresados!"

        if calculado == 1:
            header = "Vectores calculados:"
        elif calculado == 0:
            header = "Vectores ingresados:"
        elif calculado == -1:
            header = "Vectores guardados:"

        vectores = f"{header}\n"
        vectores += "---------------------------------------------"
        for nombre, vec in self.vecs_ingresados.items():
            if (calculado == 0 and len(nombre) > 1) or (calculado == 1 and len(nombre) == 1):
                continue
            vectores += f"\n{nombre}:\n"
            vectores += str(vec) + "\n"
        vectores += "---------------------------------------------"

        if vectores.count("[") == 0:
            if calculado == 1:
                return "No hay vectores calculados!"
            elif calculado == 0:
                return "No hay vectores ingresados!"
            elif calculado == -1:
                return "No hay vectores guardados!"
        return vectores

    def sumar_vecs(self, nombre_vec1: str, nombre_vec2: str) -> tuple[str, Vector]:
        """
        Suma los dos vectors indicados.
        * ArithmeticError: si los vectores no tienen la misma dimensión.
        """

        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        vec_suma = vec1 + vec2
        nombre_vec_suma = f"{nombre_vec1} + {nombre_vec2}"
        return (nombre_vec_suma, vec_suma)

    def restar_vecs(self, nombre_vec1: str, nombre_vec2: str) -> tuple[str, Vector]:
        """
        Resta los dos vectores indicados.
        * ArithmeticError: si los vectores no tienen la misma dimensión.
        """

        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        vec_resta = vec1 - vec2
        nombre_vec_resta = f"{nombre_vec1} − {nombre_vec2}"
        return (nombre_vec_resta, vec_resta)

    def escalar_por_vector(self, escalar: Fraction, nombre_vec: str) -> tuple[str, Vector]:
        """
        Multiplica un vector por un escalar.
        """

        vec = self.vecs_ingresados[nombre_vec]
        vec_multiplicado = vec * escalar

        if escalar == Fraction(1):
            escalar_str = ""
        elif escalar == Fraction(-1):
            escalar_str = "-"
        elif escalar.is_integer():
            escalar_str = str(escalar)
        else:
            escalar_str = f"({escalar}) * "

        nombre_vec_multiplicado = f"{escalar_str}{nombre_vec}"
        return (nombre_vec_multiplicado, vec_multiplicado)

    def producto_punto(self, nombre_vec1: str, nombre_vec2: str) -> tuple[str, Fraction]:
        """
        Calcula el producto punto de los dos vectores indicados.
        * ArithmeticError: si los vectores no tienen la misma dimensión.
        """

        vec1 = self.vecs_ingresados[nombre_vec1]
        vec2 = self.vecs_ingresados[nombre_vec2]

        prod_punto = vec1 * vec2
        nombre_prod_punto = f"{nombre_vec1}.{nombre_vec2}"
        return (nombre_prod_punto, prod_punto)

    def _validar_vecs_ingresados(self) -> bool:
        """
        Valida si el diccionario de vectores ingresados esta vacío o no.
        """

        if self.vecs_ingresados == {}:
            return False
        return True
