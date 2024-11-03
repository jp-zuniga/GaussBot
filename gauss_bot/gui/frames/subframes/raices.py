"""

"""

from fractions import Fraction
from typing import (
    TYPE_CHECKING,
    Optional,
)

from tkinter import Variable
from customtkinter import (
    CTkButton as ctkButton,
    CTkCheckBox as ctkCheckBox,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from gauss_bot.gui.custom_frames import (
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI
    from gauss_bot.gui.frames.ecuaciones import EcuacionesFrame


class RaicesFrame(CustomScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "EcuacionesFrame"
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame

        self.fx = ctkLabel(self, text="f(x) = ")
        self.fx_terminos = ctkLabel(self, text="")

    def update_terminos(self):
        # update la representacion str de los terminos seleccionados
        ...

    def update_frame(self):
        self.update_scrollbar_visibility()
        self.update_idletasks()
