"""
Modelos fundamentales de la aplicación.
Implementaciones de matrices, vectores y sistemas de ecuaciones.
"""

from .fraction_encoding import (
    FractionEncoder,
    FractionDecoder,
)

from .func import Func
from .matriz import Matriz
from .sistema_ecuaciones import SistemaEcuaciones
from .vector import Vector

__all__ = [
    "FractionEncoder",
    "FractionDecoder",
    "Func",
    "Matriz",
    "SistemaEcuaciones",
    "Vector",
]
