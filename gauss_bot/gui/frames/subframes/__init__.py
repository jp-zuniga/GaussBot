"""
Implementaciones de subframes de la aplicación,
que corresponden a las funcionalidades
específicas de cada módulo de la aplicación.
"""

from .input_funcs import (
    AgregarFuncs,
    MostrarFuncs,
    EliminarFuncs,
)

from .input_sis import (
    AgregarSistemas,
    MostrarSistemas,
    EliminarSistemas,
)

from .input_mats import (
    AgregarMats,
    MostrarMats,
    EliminarMats,
)

from .input_vecs import (
    AgregarVecs,
    MostrarVecs,
    EliminarVecs,
)

from .operaciones_mats import (
    SumaRestaTab,
    MultiplicacionTab,
    TransposicionTab,
    DeterminanteTab,
    InversaTab,
)

from .operaciones_vecs import (
    VSumaRestaTab,
    VMultiplicacionTab,
)

from .raices import RaicesFrame

__all__ = [
    "AgregarFuncs",
    "EditarFuncs",
    "EliminarFuncs",
    "AgregarSistemas",
    "MostrarSistemas",
    "EliminarSistemas",
    "AgregarMats",
    "MostrarMats",
    "EliminarMats",
    "AgregarVecs",
    "MostrarVecs",
    "EliminarVecs",
    "SumaRestaTab",
    "MultiplicacionTab",
    "TransposicionTab",
    "DeterminanteTab",
    "InversaTab",
    "VSumaRestaTab",
    "VMultiplicacionTab",
    "RaicesFrame",
]
