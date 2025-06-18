"""
Managers de la aplicación.
Se encargan de guardar los datos y de
realizar las operaciones matemáticas.
"""

from .binding_manager import KeyBindingManager
from .func_manager import MARGEN_ERROR, MAX_ITERACIONES, FuncManager
from .mats_manager import MatricesManager
from .ops_manager import OpsManager
from .vecs_manager import VectoresManager

__all__ = [
    "MARGEN_ERROR",
    "MAX_ITERACIONES",
    "FuncManager",
    "KeyBindingManager",
    "MatricesManager",
    "OpsManager",
    "VectoresManager",
]
