"""
Implementación de todos los frames relacionados con vectores.
"""

from typing import (
    TYPE_CHECKING,
    Union,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkScrollableFrame as ctkScrollFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.managers.mats_manager import MatricesManager

from gauss_bot.gui.frames.subframes.operaciones_vecs import (
    SumaRestaTab,
    MultiplicacionTab,
)

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI


class VectoresFrame(ctkFrame):
    """
    Frame que contiene un ctkTabview para todas
    las funcionalidades de vectores, donde cada
    una tiene su propia tab.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        vecs_manager: VectoresManager,
        mats_manager: MatricesManager,
    ) -> None:

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        self.mats_manager = mats_manager

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if not mat.aumentada
        ]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un ctkTabview con pestañas para cada funcionalidad.
        """

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[ctkFrame, ctkScrollFrame]] = []
        self.tabs = [
            ("Suma y Resta", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance = cls(self.app, tab, self, self.vecs_manager)
            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza los datos de todos los frames del tabview.
        """

        self.update_idletasks()
        self.mats_manager.mats_ingresadas = {
            nombre: mat
            for nombre, mat in sorted(self.mats_manager.mats_ingresadas.items())
        }

        self.vecs_manager.vecs_ingresados = {
            nombre: vec
            for nombre, vec in sorted(self.vecs_manager.vecs_ingresados.items())
        }

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if not mat.aumentada
        ]

        for tab in self.instances:
            tab.update_frame()  # type: ignore
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.update_idletasks()
