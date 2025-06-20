"""
Main loop de la aplicación.
"""

from platform import system

from gauss_bot.gui import GaussUI
from gauss_bot.utils import log_setup


def main() -> None:
    log_setup()

    app = GaussUI()
    app.update_idletasks()

    if system() == "Linux":
        app.wm_attributes("-fullscreen", True)
    elif system() == "Windows":
        app.state("zoomed")

    app.mainloop()


if __name__ == "__main__":
    main()
