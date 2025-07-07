"""
Implementación de frame principal de operaciones de sistemas de ecuaciones.
"""

from typing import TYPE_CHECKING

from customtkinter import CTkButton, CTkFrame

from src.gui.custom import ErrorFrame
from src.managers import MatricesManager
from src.utils import INPUTS_ICON

from .subframes import ResolverSisFrame

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.custom.adapted import CustomScrollFrame


class SistemasFrame(CTkFrame):
    """
    Frame para resolver sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        mats_manager: MatricesManager,
    ) -> None:
        """
        Inicializar diseño de frame principal para sistemas de ecuaciones.
        """

        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.mats_manager = mats_manager

        self.dummy_frame: CTkFrame  # para pack mensaje de error inicial

        self.resolver_frame: CustomScrollFrame | None = None
        self.msg_frame: CTkFrame | None = None

        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())
        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar frame y widgets.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_sistemas) == 0:
            # si no hay sistemas guardados, mostrar mensaje de error y
            # agregar boton para dirigir al usuario adonde se agregan
            self.dummy_frame = CTkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame,
                msg="¡No se ha guardado ningún sistema de ecuaciones!",
            )

            agregar_button = CTkButton(
                self.dummy_frame,
                height=30,
                text="Agregar sistemas",
                image=INPUTS_ICON,
                command=lambda: (
                    self.app.inputs_frame.ir_a_input_frame("Sistemas de Ecuaciones")
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

        self.resolver_frame = ResolverSisFrame(
            app=self.app,
            master_frame=self,
            mats_manager=self.mats_manager,
            border_width=3,
        )

        self.resolver_frame.pack(expand=True, fill="both", padx=30, pady=30)

    def update_all(self) -> None:
        """
        Actualizar las widgets del frame.
        """

        # sortear los diccionarios de datos para que esten alfabetizados
        self.mats_manager.sis_ingresados = dict(
            sorted(self.mats_manager.sis_ingresados.items()),
        )

        # actualizar los atributos de nombres despues que cambiaron los dicts
        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        if (
            self.msg_frame is not None
            or self.resolver_frame is None
            or len(self.nombres_sistemas) == 0
        ):
            # si hay un mensaje de error,
            # o no se han inicializado el frame,
            # o no hay sistemas ingresados,
            # correr el setup
            self.setup_frame()
            return

        self.resolver_frame.update_frame()  # type: ignore[reportAttributeAccessIssue]
