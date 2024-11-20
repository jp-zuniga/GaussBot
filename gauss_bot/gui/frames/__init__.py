"""
Implementación de los parents frame de
los módulos de la aplciación.
"""

from .nav import NavFrame
from .inputs import (
    InputsFrame,
    ManejarFuncs,
    ManejarSistemas,
    ManejarMats,
    ManejarVecs,
)

from .home import HomeFrame
from .matrices import MatricesFrame
from .vectores import VectoresFrame
from .analisis import AnalisisFrame
from .ecuaciones import SistemasFrame
from .config import ConfigFrame

__all__ = [
    "NavFrame",
    "InputsFrame",
    "ManejarFuncs",
    "ManejarSistemas",
    "ManejarMats",
    "ManejarVecs",
    "HomeFrame",
    "MatricesFrame",
    "VectoresFrame",
    "AnalisisFrame",
    "SistemasFrame",
    "ConfigFrame",
]
