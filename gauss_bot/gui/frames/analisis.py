"""
Implementación de MatricesFrame, el parent frame
de todos los subframes relacionados con matrices.
"""

from typing import (
    TYPE_CHECKING,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.gui.frames.subframes import RaicesFrame

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class AnalisisFrame(ctkFrame):
    """
    Frame principal para el módulo de análisis númerico.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
    ) -> None:

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app

        self.instances: list[
            RaicesFrame,
        ]

        self.tabs: list[
            tuple[
                str,
                type[RaicesFrame],
            ]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada módulo de análisis.
        """

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Raíces de Funciones", RaicesFrame),
        ]

        # iterar sobre self.tabs para:
        # * agregar tabs al tabview
        # * inicializar los frames de cada tab
        # * añadir los frames a self.instances
        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: RaicesFrame = (
                cls(self.app, tab, self)
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza todos los frames del tabview.
        """

        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")  # type: ignore
