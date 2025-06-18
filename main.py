"""
Main loop de la aplicación.
"""

from platform import system

from gauss_bot.utils import log_setup
from gauss_bot.gui import GaussUI

if __name__ == "__main__":
    log_setup()

    app = GaussUI()
    app.update_idletasks()

    if system() == "Linux":
        app.wm_attributes("-zoomed", True)
    elif system() == "Windows":
        app.state("zoomed")

    app.mainloop()
