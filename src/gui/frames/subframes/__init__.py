"""
Implementaciones de subframes de la aplicación,
que corresponden a las funcionalidades
específicas de cada módulo de la aplicación.
"""

from .derivadas import DerivadasFrame
from .input_funcs import AgregarFuncs, EliminarFuncs, MostrarFuncs
from .input_mats import AgregarMats, EliminarMats, MostrarMats
from .input_sis import AgregarSistemas, EliminarSistemas, MostrarSistemas
from .input_vecs import AgregarVecs, EliminarVecs, MostrarVecs
from .integrales import IntegralesFrame
from .operaciones_mats import (
    DeterminanteTab,
    InversaTab,
    MultiplicacionTab,
    SumaRestaTab,
    TransposicionTab,
)
from .operaciones_vecs import (
    MagnitudTab,
    MultiplicacionTab as VMTab,
    SumaRestaTab as VSRTab,
)
from .raices import RaicesFrame
from .resolver_sis import ResolverSisFrame

__all__: list[str] = [
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
    "IntegralesFrame",
    "InversaTab",
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
