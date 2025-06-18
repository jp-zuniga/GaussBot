"""
GaussBot es una aplicación para realizar cálculos
de álgebra lineal, como resolver sistemas de ecuaciones,
operaciones con matrices y vectores, y análisis númerico.
"""

from . import utils
from . import gui
from . import models
from . import managers


__all__ = ["managers", "models", "utils", "gui"]
