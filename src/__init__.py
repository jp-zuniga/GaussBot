"""
GaussBot es una aplicación para realizar cálculos
de álgebra lineal, como resolver sistemas de ecuaciones,
operaciones con matrices y vectores, y análisis númerico.
"""

FRAC_PREC: dict[str, int] = {"prec": 100}

from platform import system

from . import gui, managers, models, utils


def main() -> None:
    """
    Main loop de la aplicación.
    """

    utils.log_setup()
    app = gui.GaussUI()

    if system() == "Windows":
        app.after(0, lambda: app.state("zoomed"))
    else:
        app.wm_attributes("-zoomed", True)

    app.mainloop()


__version__: str = "1.0.0"
__all__: list[str] = ["main", "managers", "models", "utils", "gui"]
