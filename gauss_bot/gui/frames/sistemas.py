"""
Implementación de EcuacionesFrame,
el frame que contiene todos los
subframes relacionados a ecuaciones.
"""

from typing import (
    TYPE_CHECKING,
    Optional,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkTabview as ctkTabview,
)

from ...icons import INPUTS_ICON
from ...managers import MatricesManager
from ..custom import ErrorFrame
from .subframes import ResolverSisFrame

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class SistemasFrame(ctkFrame):
    """
    Frame para resolver sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        self.dummy_frame: ctkFrame  # para pack mensaje de error inicial
        self.msg_frame: Optional[ctkFrame] = None
        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        self.instances: list[ResolverSisFrame]
        self.tabs: dict[str, str]

        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crea un tabview con pestañas para cada método de resolver sistemas.
        Se encarga de validar si hay sistemas ingresados para que
        los setups de los frames individuales no lo tengan que hacer.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_sistemas) == 0:
            # si no hay sistemas guardados, mostrar mensaje de error y
            # agregar boton para dirigir al usuario adonde se agregan
            self.dummy_frame = ctkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame,
                msg="No hay sistemas guardados!",
            )

            agregar_button = ctkButton(
                self.dummy_frame,
                height=30,
                text="Agregar sistemas",
                image=INPUTS_ICON,
                command=lambda: (
                    self.app.inputs_frame.ir_a_input_sis(mostrar=False)  # type: ignore
                ),
            )

            self.dummy_frame.pack(expand=True, anchor="center")
            self.msg_frame.pack(pady=5, anchor="center")
            agregar_button.pack(pady=5, anchor="center")
            return

        # cleanup mensaje de error si todavia existe
        if self.msg_frame is not None:
            for widget in self.winfo_children():
                widget.destroy()
            self.msg_frame = None

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = {
            "Método Gauss−Jordan": "gj",
            "Regla de Cramer": "c",
            # "Factorización LU": "f",
        }

        for nombre, codigo in self.tabs.items():
            tab = self.tabview.add(nombre)
            tab_instance = ResolverSisFrame(
                self.app, tab, self, self.mats_manager, codigo  # type: ignore
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self):
        """
        Actualiza todos los frames del tabview.
        """

        # sortear los diccionarios de datos para que esten alfabetizados
        self.mats_manager.sis_ingresados = dict(
            sorted(
                self.mats_manager.sis_ingresados.items()
            )
        )

        # actualizar los atributos de nombres despues que cambiaron los dicts
        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        if (
            self.msg_frame is not None or
            len(self.nombres_sistemas) == 0 or
            not self.instances
        ):
            # si hay un mensaje de error,
            # o no hay sistemas ingresados,
            # o no se han inicializado los frames,
            # correr el setup
            self.setup_tabview()
            return

        # si no, actualizar todos los subframes
        for tab in self.instances:
            tab.update_frame()
