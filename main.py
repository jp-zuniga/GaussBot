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

    if system() == "Windows":
        app.after(0, lambda: app.state("zoomed"))
    else:
        app.wm_attributes("-fullscreen", True)

    app.mainloop()


if __name__ == "__main__":
    main()
