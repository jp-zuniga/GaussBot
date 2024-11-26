"""
Implementación de los parents frame de
los módulos de la aplciación.
"""

from .nav import NavFrame
from .inputs import (
    InputsFrame,
    ManejarMats,
    ManejarVecs,
    ManejarFuncs,
    ManejarSistemas,
)

from .home import HomeFrame
from .matrices import MatricesFrame
from .vectores import VectoresFrame
from .analisis import AnalisisFrame
from .sistemas import SistemasFrame
from .config import ConfigFrame

__all__ = [
    "AnalisisFrame",
    "ConfigFrame",
    "HomeFrame",
    "InputsFrame",
    "ManejarFuncs",
    "ManejarMats",
    "ManejarSistemas",
    "ManejarVecs",
    "MatricesFrame",
    "NavFrame",
    "SistemasFrame",
    "VectoresFrame",
]
