"""
Implementación de EcuacionesFrame,
el frame que contiene todos los
subframes relacionados a ecuaciones.
"""

from typing import (
    TYPE_CHECKING,
    Union,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.managers import MatricesManager
from gauss_bot.gui.frames.subframes import (
    SistemasFrame,
    RaicesFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class EcuacionesFrame(ctkFrame):
    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager
        self.nombres_sistemas = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if mat.aumentada
        ]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[SistemasFrame, RaicesFrame]] = []
        self.tabs: list[tuple[str, type]] = [
            ("Sistemas de Ecuaciones", SistemasFrame),
            ("Raíces de Funciones", RaicesFrame),
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            if nombre.startswith("Sistemas"):
                tab_instance: SistemasFrame = (
                    cls(self.app, tab, self, self.mats_manager)
                )
            else:
                tab_instance: RaicesFrame = cls(self.app, tab, self)  # type: ignore

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self):
        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()
