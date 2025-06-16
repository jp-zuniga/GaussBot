"""
GaussBot es una aplicación para realizar cálculos
de álgebra lineal, como resolver sistemas de ecuaciones,
operaciones con matrices y vectores, y análisis númerico.
"""

from os import path

__all__ = [
    "ASSET_PATH",
    "CONFIG_PATH",
    "DATA_PATH",
    "FUNCIONES_PATH",
    "MATRICES_PATH",
    "SISTEMAS_PATH",
    "THEMES_PATH",
    "VECTORES_PATH",
]


################################################################################
###################   Paths y directorios de la aplicación   ###################
################################################################################


ASSET_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "assets"
)

DATA_PATH = path.join(
    path.expanduser("~"),
    "GaussBot",
    "data",
)

CONFIG_PATH = path.join(DATA_PATH, "config.json")
FUNCIONES_PATH = path.join(DATA_PATH, "funciones.json")
MATRICES_PATH = path.join(DATA_PATH, "matrices.json")
SISTEMAS_PATH = path.join(DATA_PATH, "sistemas.json")
VECTORES_PATH = path.join(DATA_PATH, "vectores.json")

THEMES_PATH = path.join(ASSET_PATH, "themes")
