"""
Inicializa la interfaz gráfica y ejecuta la aplicación.
"""

from gauss_bot.gui import GaussUI
from gauss_bot.util_funcs import log_setup

if __name__ == "__main__":
    log_setup()  # configurar logger
    app = GaussUI()
    # app.after(0, lambda: app.state("zoomed"))  # maximizar ventana
    app.mainloop()
