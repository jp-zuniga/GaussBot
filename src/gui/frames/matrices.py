"""
Implementación de frame principal de operaciones de matrices.
"""

from typing import TYPE_CHECKING

from customtkinter import CTkButton, CTkFrame, CTkTabview

from src.gui.custom import ErrorFrame
from src.managers import MatricesManager, VectoresManager
from src.utils import INPUTS_ICON

from .subframes import (
    DeterminanteTab,
    InversaTab,
    MultiplicacionTab,
    SumaRestaTab,
    TransposicionTab,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.custom.adapted import CustomScrollFrame


class MatricesFrame(CTkFrame):
    """
    Frame que contiene un CTkTabview para todas
    las funcionalidades de matrices, donde cada
    una tiene su propia tab.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: "GaussUI",
        mats_manager: MatricesManager,
        vecs_manager: VectoresManager,
    ) -> None:
        """
        Inicializar diseño de frame principal para operaciones de matrices.
        """

        super().__init__(master, corner_radius=0, fg_color="transparent")

        self.app = app
        self.mats_manager = mats_manager
        self.vecs_manager = vecs_manager

        self.dummy_frame: CTkFrame  # para pack mensaje de error inicial
        self.msg_frame: CTkFrame | None = None
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        self.instances: list[
            SumaRestaTab
            | MultiplicacionTab
            | DeterminanteTab
            | TransposicionTab
            | InversaTab
        ]

        self.tabs: list[
            tuple[
                str,
                type[
                    SumaRestaTab
                    | MultiplicacionTab
                    | DeterminanteTab
                    | TransposicionTab
                    | InversaTab
                ],
            ]
        ]

        self.tabview: CTkTabview
        self.setup_tabview()

    def setup_tabview(self) -> None:
        """
        Crear CTkTabview con pestañas para cada funcionalidad.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.nombres_matrices) == 0:
            # si no hay matrices guardadas, mostrar mensaje de error y
            # agregar boton para dirigir al usuario adonde se agregan
            self.dummy_frame = CTkFrame(self, fg_color="transparent")
            self.msg_frame = ErrorFrame(
                self.dummy_frame,
                msg="¡No se ha guardado ninguna matriz!",
            )

            agregar_button = CTkButton(
                self.dummy_frame,
                height=30,
                text="Agregar matrices",
                image=INPUTS_ICON,
                command=lambda: (self.app.inputs_frame.ir_a_input_frame("Matrices")),
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

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        self.instances = []
        self.tabs = [
            ("Suma y Resta", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
            ("Calcular Determinante", DeterminanteTab),
            ("Transposición", TransposicionTab),
            ("Encontrar Inversa", InversaTab),
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
                self.mats_manager,
                border_width=3,
            )

            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)

    def update_all(self) -> None:
        """
        Actualizar todos los frames del tabview.
        """

        # sortear los diccionarios de datos para que esten alfabetizados
        self.mats_manager.mats_ingresadas = dict(
            sorted(self.mats_manager.mats_ingresadas.items()),
        )

        self.vecs_manager.vecs_ingresados = dict(
            sorted(self.vecs_manager.vecs_ingresados.items()),
        )

        # actualizar los atributos de nombres despues que cambiaron los dicts
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if (
            self.msg_frame is not None
            or len(self.nombres_matrices) == 0
            or self.instances == []
        ):
            # si hay un mensaje de error,
            # o no hay matrices ingresadas,
            # o no se han inicializado los frames,
            # correr el setup
            self.setup_tabview()
            return

        # si no, actualizar todos los subframes
        for tab in self.instances:
            tab.update_frame()
