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
    MagnitudTab,
    SumaRestaTab as VSRTab,
    MultiplicacionTab as VMTab,
)

from .resolver_sis import ResolverSisFrame
from .raices import RaicesFrame
from .derivadas import DerivadasFrame
from .integrales import IntegralesFrame


__all__ = [
    "AgregarFuncs",
    "AgregarMats",
    "AgregarSistemas",
    "AgregarVecs",
    "DerivadasFrame",
    "DeterminanteTab",
    "EliminarFuncs",
    "EliminarMats",
    "EliminarSistemas",
    "EliminarVecs",
    "InversaTab",
    "IntegralesFrame",
    "MagnitudTab",
    "MostrarFuncs",
    "MostrarMats",
    "MostrarSistemas",
    "MostrarVecs",
    "MultiplicacionTab",
    "RaicesFrame",
    "ResolverSisFrame",
    "SumaRestaTab",
    "TransposicionTab",
    "VMTab",
    "VSRTab",
]
