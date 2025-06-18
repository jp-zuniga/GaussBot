"""
GaussBot es una aplicación para realizar cálculos
de álgebra lineal, como resolver sistemas de ecuaciones,
operaciones con matrices y vectores, y análisis númerico.
"""

from .gui import GaussUI
from .utils import log_setup

if __name__ == "__main__":
    log_setup()  # configurar logger
    app = GaussUI()
    app.update_idletasks()
    app.wm_attributes("-zoomed", True)
    app.mainloop()
