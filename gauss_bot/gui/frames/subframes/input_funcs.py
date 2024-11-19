"""
Implementación de los subframes de ManejarFuncs.
"""

from os import path
from typing import (
    TYPE_CHECKING,
    Optional,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from sympy import (
    latex,
    parse_expr,
)

from gauss_bot import (
    DATA_PATH,
    ENTER_ICON,
    delete_msg_frame,
    get_dict_key,
    generate_sep,
)

from gauss_bot.models import Func
from gauss_bot.managers import FuncManager
from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomNumpad,
    CustomScrollFrame,
    IconButton,
    place_msg_frame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import InputsFrame


class AgregarFuncs(CustomScrollFrame):
    """
    Frame para agregar funciones para uso
    en el módulo de análisis númerico.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "InputsFrame",
        func_manager: FuncManager,
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.msg_frame: Optional[ctkFrame] = None

        self.func = ""
        self.func_frame = ctkFrame(self, fg_color="transparent")


class MostrarFuncs:
    """
    Frame para mostrar las funciones ingresadas.
    """


class EliminarFuncs:
    """
    Frame para eliminar funciones.
    """
