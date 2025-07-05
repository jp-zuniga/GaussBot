"""
Implementación de MatricesFrame, el parent frame
de todos los subframes relacionados con matrices.
"""

from typing import TYPE_CHECKING, Optional, Union

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from .subframes import DerivadasFrame, IntegralesFrame, RaicesFrame
from ..custom import ErrorFrame
from ...managers import FuncManager
from ...utils import INPUTS_ICON

if TYPE_CHECKING:
    from .. import GaussUI
    from ..custom.adapted import CustomScrollFrame


class AnalisisFrame(ctkFrame):
    """
    Frame principal para el módulo de análisis númerico.
    """

    def __init__(
        self, app: "GaussUI", master: "GaussUI", func_manager: FuncManager
    ) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.func_manager = func_manager
        self.nombres_funciones = list(func_manager.funcs_ingresadas.keys())

        self.dummy_frame: ctkFrame
        self.msg_frame: Optional[ctkFrame] = None

        self.instances: list[Union[RaicesFrame, DerivadasFrame, IntegralesFrame],]

        self.tabs: list[
            tuple[
                str,
                Union[type[RaicesFrame], type[DerivadasFrame], type[IntegralesFrame]],
            ]
        ]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada módulo de análisis númerico.
        """

        for widget in self.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        if len(self.nombres_funciones) == 0:
            # si no hay funciones guardadas, mostrar mensaje de error y
            # agregar boton para dirigir al usuario adonde se agregan
            self.dummy_frame = ctkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame, msg="¡No se ha guardado ninguna función!"
            )

            agregar_button = ctkButton(
                self.dummy_frame,
                height=30,
                text="Agregar funciones",
                image=INPUTS_ICON,
                command=lambda: (
                    self.app.inputs_frame.ir_a_input_funcs(mostrar=False)  # type: ignore
                ),
            )

            self.dummy_frame.pack(expand=True, anchor="center")
            self.msg_frame.pack(pady=5, anchor="center")
            agregar_button.pack(pady=5, anchor="center")
            return

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Raíces de Funciones", RaicesFrame),
            ("Derivadas", DerivadasFrame),
            ("Integrales", IntegralesFrame),
        ]

        # iterar sobre self.tabs para:
        # * agregar tabs al tabview
        # * inicializar los frames de cada tab
        # * añadir los frames a self.instances
        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: "CustomScrollFrame" = cls(
                self.app, tab, self, self.func_manager, border_width=3
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza todos los frames del tabview.
        """

        self.func_manager.funcs_ingresadas = dict(
            sorted(self.func_manager.funcs_ingresadas.items())
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
                widget.configure(bg_color="transparent")  # type: ignore
        self.tabview.configure(fg_color="transparent")  # type: ignore
