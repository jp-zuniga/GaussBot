"""
Implementación de MatricesFrame, el parent frame
de todos los subframes relacionados con matrices.
"""

from typing import Union

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.managers.mats_manager import MatricesManager

from gauss_bot.gui.custom_frames import CustomScrollFrame

from gauss_bot.gui.frames.subframes.input_mats import ManejarMats
from gauss_bot.gui.frames.subframes.operaciones_mats import (
    SumaRestaTab,
    MultiplicacionTab,
    TransposicionTab,
    DeterminanteTab,
    InversaTab,
)


class MatricesFrame(ctkFrame):
    """
    Frame principal para la sección de matrices.
    Contiene un tabview con todas las operaciones disponibles.
    """

    def __init__(self, master, app, mats_manager: MatricesManager) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        self.nombres_vectores = list(self.app.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if not mat.aumentada
        ]

        self.nombres_sistemas = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if mat.aumentada
        ]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada operación con matrices.
        """

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[ctkFrame, CustomScrollFrame]] = []
        self.tabs = [
            ("Manejar Matrices", ManejarMats),
            ("Suma y Resta", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
            ("Transposición", TransposicionTab),
            ("Calcular Determinante", DeterminanteTab),
            ("Encontrar Inversa", InversaTab)
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: Union[ctkFrame, CustomScrollFrame] = (
                cls(self, tab, self.app, self.mats_manager)  # type: ignore
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza todos los frames del tabview.
        """

        self.mats_manager.mats_ingresadas = {
            nombre: mat
            for nombre, mat in sorted(self.mats_manager.mats_ingresadas.items())
        }

        self.app.vecs_manager.vecs_ingresados = {
            nombre: vec
            for nombre, vec in sorted(self.app.vecs_manager.vecs_ingresados.items())
        }

        self.nombres_vectores = list(self.app.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if not mat.aumentada
        ]

        self.nombres_sistemas = [
            nombre
            for nombre, mat in self.mats_manager.mats_ingresadas.items()
            if mat.aumentada
        ]

        for tab in self.instances:
            tab.update()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.app.ecuaciones.update_frame()
        self.update_idletasks()
