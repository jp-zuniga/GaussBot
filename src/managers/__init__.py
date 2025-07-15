"""
Implementaciones de los managers de la aplicación.
Se encargan de almacenar datos y realizar operaciones matemáticas.
"""

from .binding_manager import KeyBindingManager
from .mats_manager import MatricesManager
from .vecs_manager import VectoresManager
from .ops_manager import OpsManager
from .func_manager import MARGEN_ERROR, MAX_ITERACIONES, FuncManager

__all__: list[str] = [
    "MARGEN_ERROR",
    "MAX_ITERACIONES",
    "FuncManager",
    "KeyBindingManager",
    "MatricesManager",
    "OpsManager",
    "VectoresManager",
]
