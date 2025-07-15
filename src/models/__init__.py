"""
Implementaciones de modelos fundamentales de la aplicación.
"""

from .fraction_encoding import FractionDecoder, FractionEncoder
from .func import Func
from .matriz import Matriz
from .sistema_ecuaciones import SistemaEcuaciones
from .vector import Vector

__all__: list[str] = [
    "FractionDecoder",
    "FractionEncoder",
    "Func",
    "Matriz",
    "SistemaEcuaciones",
    "Vector",
]
