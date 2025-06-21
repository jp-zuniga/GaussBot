"""
Modelos fundamentales de la aplicación.
Implementaciones de matrices, vectores y sistemas de ecuaciones.
"""

from .fraction_encoding import FractionDecoder, FractionEncoder
from .func import Func
from .matriz import Matriz
from .sistema_ecuaciones import SistemaEcuaciones
from .vector import Vector

__all__: list[str] = [
    "FractionEncoder",
    "FractionDecoder",
    "Func",
    "Matriz",
    "SistemaEcuaciones",
    "Vector",
]
