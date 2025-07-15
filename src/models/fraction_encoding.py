"""
Implementación de un custom encoder/decoder
para leer y escribir objetos Fraction() a archivos .json.
"""

from fractions import Fraction
from json import JSONDecoder, JSONEncoder
from typing import override


class FractionEncoder(JSONEncoder):
    """
    JSONEncoder subclass para escribir objetos Fraction()
    a archivos .json en un formato personalizado.
    """

    @override
    def default(self, o: object) -> dict:
        """
        Serializar objetos Fraction.
        """

        if isinstance(o, Fraction):
            # si el objeto encontrado es una instancia de Fraction,
            # se serializa como un diccionario, que incluye
            # el tipo del objeto, el numerador, y el denominador.
            return {
                "__type__": "Fraction",
                "numerator": o.numerator,
                "denominator": o.denominator,
            }

        # si no, llamar al metodo default() de JSONEncoder para tirar el error
        return super().default(o)


class FractionDecoder(JSONDecoder):
    """
    JSONDecoder subclass para leer objetos Fraction()
    de archivos .json, codificados por FractionEncoder.
    """

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """
        Args:
            args:   Argumentos posicionales para JSONDecoder.__init__().
            kwargs: Argumentos de palabra clave para JSONDecoder.__init__().

        """

        # inicializar con fraction_object_hook() como hook por defecto
        super().__init__(*args, object_hook=self.fraction_object_hook, **kwargs)

    def fraction_object_hook(self, obj: dict) -> Fraction | dict:
        """
        Custom hook para decodificar objetos Fraction().
        """

        # si el diccionario encontrado contiene la llave "__type__",
        # y su valor == "Fraction", se asume que representa un objeto Fraction(),
        # y se retorna una instancia de Fraction() con los valores del diccionario.
        if "__type__" in obj and obj["__type__"] == "Fraction":
            return Fraction(obj["numerator"], obj["denominator"])

        # si no, retornar el diccionario a como se encuentra
        return obj
