"""
Implementación de un custom encoder/decoder
para leer y escribir objetos Fraction() a archivos .json.
"""

from fractions import Fraction
from json import (
    JSONEncoder,
    JSONDecoder
)

from typing import Any, Union


class FractionEncoder(JSONEncoder):
    """
    JSONEncoder subclass para escribir objetos Fraction()
    a archivos .json en un formato personalizado.
    """

    # override del metodo default() de JSONEncoder
    def default(self, o: Any) -> Union[dict[str, int], Any]:
        if isinstance(o, Fraction):
            return {
                "__type__": "Fraction",
                "numerator": o.numerator,
                "denominator": o.denominator
            }

        return super().default(o)


class FractionDecoder(JSONDecoder):
    """
    JSONDecoder subclass para leer objetos Fraction()
    de archivos .json, codificados por FractionEncoder.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.fraction_object_hook, *args, **kwargs)

    def fraction_object_hook(self, obj: dict) -> Union[Fraction, dict]:
        """
        Custom hook para decodificar objetos Fraction().
        """

        if "__type__" in obj and obj["__type__"] == "Fraction":
            return Fraction(obj["numerator"], obj["denominator"])
        return obj
