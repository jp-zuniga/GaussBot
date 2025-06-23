"""
GaussBot es una aplicación para realizar cálculos
de álgebra lineal, como resolver sistemas de ecuaciones,
operaciones con matrices y vectores, y análisis númerico.
"""

FRAC_PREC: dict[str, int] = {"prec": 100}

from . import gui, managers, models, utils  # noqa


__all__: list[str] = ["managers", "models", "utils", "gui"]
