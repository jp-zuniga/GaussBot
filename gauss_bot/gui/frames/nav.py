"""
Implementación de la clase NavFrame,
la barra de navegación de la aplicación.
"""

from os import (
    path,
    remove,
)

from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

# from gauss_bot.gui.custom import CustomMessagebox
from gauss_bot import (
    DATA_PATH,
    LOGO,
    HOME_ICON,
    INPUTS_ICON,
    ECUACIONES_ICON,
    MATRIZ_ICON,
    VECTOR_ICON,
    CONFIG_ICON,
    QUIT_ICON,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI


class NavFrame(ctkFrame):
    """
    Barra de navigación que contiene botones
    para navegar entre los distintos frames de la aplicación.
    """

    def __init__(self, app: "GaussUI", master: "GaussUI") -> None:
        super().__init__(master, corner_radius=0)
        self.app = app

        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.configure(fg_color=self.app.theme_config["CTk"]["fg_color"])

        self.logo_label = ctkLabel(self, image=LOGO, text="")
        self.logo_text = ctkLabel(
            self, text="GaussBot",
            font=ctkFont(size=18, weight="bold"),
        )

        self.home_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Inicio", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=HOME_ICON, anchor="w",
            command=self.home_button_event,
        )

        self.inputs_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Datos", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=INPUTS_ICON, anchor="w",
            command=self.inputs_button_event,
        )

        self.ecuaciones_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Ecuaciones", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=ECUACIONES_ICON, anchor="w",
            command=self.ecuaciones_button_event,
        )

        self.matrices_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Matrices", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=MATRIZ_ICON, anchor="w",
            command=self.matrices_button_event,
        )

        self.vectores_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Vectores", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=VECTOR_ICON, anchor="w",
            command=self.vectores_button_event,
        )

        self.config_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Configuración", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=CONFIG_ICON, anchor="w",
            command=self.config_button_event,
        )

        self.quit_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Cerrar", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=QUIT_ICON, anchor="w",
            command=self.quit_event,
        )

        self.logo_label.grid(row=0, column=0, padx=5, pady=20, sticky="e")
        self.logo_text.grid(row=0, column=1, padx=5, pady=20, sticky="w")
        self.home_button.grid(row=1, column=0, columnspan=2, padx=10, sticky="ew")
        self.inputs_button.grid(row=2, column=0, columnspan=2, padx=10, sticky="ew")
        self.ecuaciones_button.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")
        self.matrices_button.grid(row=4, column=0, columnspan=2, padx=10, sticky="ew")
        self.vectores_button.grid(row=5, column=0, columnspan=2, padx=10, sticky="ew")
        self.config_button.grid(row=7, column=0, columnspan=2, padx=10, sticky="ew")
        self.quit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.frames = {
            "home": self.app.home_frame,  # type: ignore
            "inputs": self.app.inputs_frame,  # type: ignore
            "ecuaciones": self.app.ecuaciones,  # type: ignore
            "matrices": self.app.matrices,  # type: ignore
            "vectores": self.app.vectores,  # type: ignore
            "config": self.app.config_frame  # type: ignore
        }

        self.buttons = {
            "home": self.home_button,
            "inputs": self.inputs_button,
            "ecuaciones": self.ecuaciones_button,
            "matrices": self.matrices_button,
            "vectores": self.vectores_button,
            "config": self.config_button
        }

    def seleccionar_frame(self, nombre: str) -> None:
        """
        Muestra el frame correspondiente al nombre ingresado,
        y oculta los demás. Cambia el color del botón presionado.
        """

        for nombre_frame, button in self.buttons.items():
            button.configure(
                fg_color=("gray75", "gray25")
                if nombre == nombre_frame
                else "transparent"
            )

        for nombre_frame, frame in self.frames.items():
            if nombre == nombre_frame:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def home_button_event(self) -> None:
        self.seleccionar_frame("home")

    def inputs_button_event(self) -> None:
        self.seleccionar_frame("inputs")

    def ecuaciones_button_event(self) -> None:
        self.seleccionar_frame("ecuaciones")

    def matrices_button_event(self) -> None:
        self.seleccionar_frame("matrices")

    def vectores_button_event(self) -> None:
        self.seleccionar_frame("vectores")

    def config_button_event(self) -> None:
        self.seleccionar_frame("config")

    def quit_event(self) -> None:
        # confirmar_quit = CustomMessagebox(
        #     self.app,
        #     title="Confirmar salida",
        #     message="¿Estás seguro de que deseas salir?",
        #     option_1="No",
        #     option_2="Sí",
        #     icon="warning",
        # )

        self.app.ops_manager.save_sistemas()  # type: ignore
        self.app.ops_manager.save_matrices()  # type: ignore
        self.app.ops_manager.save_vectores()  # type: ignore
        self.app.save_config()
        self.app.quit()
        try:
            remove(path.join(DATA_PATH, "func.png"))
        except FileNotFoundError:
            pass
