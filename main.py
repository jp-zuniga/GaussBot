"""
Inicializa la interfaz gráfica y ejecuta la aplicación.
"""

from gauss_bot import log_setup
from gauss_bot.gui import GaussUI

if __name__ == "__main__":
    log_setup()  # configurar logging
    app = GaussUI()
    app.after(0, lambda: app.state("zoomed"))  # maximizar ventana
    app.mainloop()
