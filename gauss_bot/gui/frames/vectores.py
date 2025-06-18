"""
Implementación de todos los frames relacionados con vectores.
"""

from typing import TYPE_CHECKING, Optional, Union

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from .subframes import MagnitudTab, VMTab, VSRTab
from ..custom import ErrorFrame
from ...managers import MatricesManager, VectoresManager
from ...utils import INPUTS_ICON

if TYPE_CHECKING:
    from .. import GaussUI
    from ..custom import CustomScrollFrame


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

        self.dummy_frame: ctkFrame  # para pack mensaje de error inicial
        self.msg_frame: Optional[ctkFrame] = None
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        self.instances: list[Union[MagnitudTab, VSRTab, VMTab]]

        self.tabs: list[tuple[str, Union[type[MagnitudTab], type[VSRTab], type[VMTab]]]]

        self.tabview: ctkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un ctkTabview con pestañas para cada funcionalidad.
        Se encarga de validar si hay vectores ingresados para que
        los setups de los frames individuales no lo tengan que hacer.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_vectores) == 0:
            # si no hay vectores guardados, mostrar mensaje de error y
            # agregar boton para que el usuario sepa donde agregarlos
            self.dummy_frame = ctkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame, msg="No se ha guardado ningún vector!"
            )

            agregar_button = ctkButton(
                self.dummy_frame,
                height=30,
                text="Agregar vectores",
                image=INPUTS_ICON,
                command=lambda: (
                    self.app.inputs_frame.ir_a_input_vecs(mostrar=False)  # type: ignore
                ),
            )

            self.dummy_frame.pack(expand=True, anchor="center")
            self.msg_frame.pack(pady=5, anchor="center")
            agregar_button.pack(pady=5, anchor="center")
            return

        # cleanup si el mensaje de error todavia existe
        if self.msg_frame is not None:
            for widget in self.winfo_children():
                widget.destroy()
            self.msg_frame = None

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Magnitud", MagnitudTab),
            ("Suma y Resta", VSRTab),
            ("Multiplicación", VMTab),
        ]

        # iterar sobre self.tabs para:
        # * agregar tabs al tabview
        # * inicializar los frames de cada tab
        # * añadir los frames a self.instances
        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance: "CustomScrollFrame" = cls(
                self.app, tab, self, self.vecs_manager
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza los datos de todos los frames del tabview.
        """

        # sort los diccionarios de datos para que esten alfabetizados
        self.mats_manager.mats_ingresadas = dict(
            sorted(self.mats_manager.mats_ingresadas.items())
        )

        self.vecs_manager.vecs_ingresados = dict(
            sorted(self.vecs_manager.vecs_ingresados.items())
        )

        # actualizar atributos de nombres despues que cambiaron los dicts
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if (
            self.msg_frame is not None
            or len(self.nombres_vectores) == 0
            or self.instances == []
        ):
            # si hay un mensaje de error,
            # o ahora no hay vectores,
            # o no se han inicializado los frames,
            # correr el setup
            self.setup_tabview()
            return

        # si no, actualizar todos los subframes
        for tab in self.instances:
            tab.update_frame()
