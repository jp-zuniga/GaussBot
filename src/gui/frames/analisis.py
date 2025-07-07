"""
Implementación de frame principal de análisis númerico.
"""

from typing import TYPE_CHECKING

from customtkinter import CTkButton, CTkFrame, CTkTabview

from src.gui.custom import ErrorFrame
from src.managers import FuncManager
from src.utils import INPUTS_ICON

from .subframes import DerivadasFrame, IntegralesFrame, RaicesFrame

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.custom.adapted import CustomScrollFrame


class AnalisisFrame(CTkFrame):
    """
    Frame principal para el módulo de análisis númerico.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        func_manager: FuncManager,
    ) -> None:
        """
        Inicializar diseño de frame principal de análisis númerico.
        """

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.func_manager = func_manager
        self.nombres_funciones = list(func_manager.funcs_ingresadas.keys())

        self.dummy_frame: CTkFrame
        self.msg_frame: CTkFrame | None = None

        self.instances: list[RaicesFrame | DerivadasFrame | IntegralesFrame]

        self.tabs: list[
            tuple[str, type[RaicesFrame | DerivadasFrame | IntegralesFrame]]
        ]

        self.tabview: CTkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crear tabview con pestañas para cada módulo de análisis númerico.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_funciones) == 0:
            # si no hay funciones guardadas, mostrar mensaje de error y
            # agregar boton para dirigir al usuario adonde se agregan
            self.dummy_frame = CTkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame,
                msg="¡No se ha guardado ninguna función!",
            )

            agregar_button = CTkButton(
                self.dummy_frame,
                height=30,
                text="Agregar funciones",
                image=INPUTS_ICON,
                command=lambda: (self.app.inputs_frame.ir_a_input_frame("Funciones")),
            )

            self.dummy_frame.pack(expand=True, anchor="center")
            self.msg_frame.pack(pady=5, anchor="center")
            agregar_button.pack(pady=5, anchor="center")
            return

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Raíces de Funciones", RaicesFrame),
            ("Derivadas", DerivadasFrame),
            ("Integrales", IntegralesFrame),
        ]

        # iterar sobre self.tabs para:
        # - agregar tabs al tabview
        # - inicializar los frames de cada tab
        # - añadir los frames a self.instances

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: CustomScrollFrame = cls(
                self.app,
                tab,
                self,
                self.func_manager,
                border_width=3,
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self) -> None:
        """
        Actualizar todos los frames del tabview.
        """

        self.func_manager.funcs_ingresadas = dict(
            sorted(self.func_manager.funcs_ingresadas.items()),
        )

        self.nombres_funciones = list(self.func_manager.funcs_ingresadas.keys())

        if (
            self.msg_frame is not None
            or len(self.nombres_funciones) == 0
            or self.instances == []
        ):
            # si hay un mensaje de error,
            # o no hay funciones ingresadas,
            # o no se han inicializado los frames,
            # correr el setup
            self.setup_tabview()
            return

        for tab in self.instances:
            tab.update_frame()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")
        self.tabview.configure(fg_color="transparent")
