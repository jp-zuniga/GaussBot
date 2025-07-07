"""
Implementaciones de los frames principales de la aplicación.
"""

from . import subframes
from .analisis import AnalisisFrame
from .config import ConfigFrame
from .home import HomeFrame
from .inputs import InputsFrame, ManejarFuncs, ManejarMats, ManejarSistemas, ManejarVecs
from .matrices import MatricesFrame
from .nav import NavFrame
from .sistemas import SistemasFrame
from .vectores import VectoresFrame

__all__: list[str] = [
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
    "subframes",
]
