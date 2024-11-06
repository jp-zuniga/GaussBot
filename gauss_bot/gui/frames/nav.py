"""
Implementación de la clase NavFrame,
la barra de navegación de la aplicación.
"""

from os import path, remove
from typing import TYPE_CHECKING

from PIL.Image import open as open_img

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkImage as ctkImage,
)

from gauss_bot import ASSET_PATH

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI


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

        self.logo = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_logo.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_logo.png"))
        )

        self.home_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_home_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_home_icon.png"))
        )

        self.inputs_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_input_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_input_icon.png"))
        )

        self.ecuaciones_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_ecuaciones_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_ecuaciones_icon.png"))
        )

        self.matriz_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_matriz_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_matriz_icon.png"))
        )

        self.vector_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_vector_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_vector_icon.png"))
        )

        self.config_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_config_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_config_icon.png"))
        )

        self.quit_icon = ctkImage(
            dark_image=open_img(path.join(ASSET_PATH, "light_quit_icon.png")),
            light_image=open_img(path.join(ASSET_PATH, "dark_quit_icon.png"))
        )


        self.logo_label = ctkLabel(self, image=self.logo, text="")
        self.logo_text = ctkLabel(
            self, text="GaussBot",
            font=ctkFont(size=18, weight="bold"),
        )

        self.home_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Inicio", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.home_icon, anchor="w",
            command=self.home_button_event,
        )

        self.inputs_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Datos", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.inputs_icon, anchor="w",
            command=self.inputs_button_event,
        )

        self.ecuaciones_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Ecuaciones", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.ecuaciones_icon, anchor="w",
            command=self.ecuaciones_button_event,
        )

        self.matrices_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Matrices", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.matriz_icon, anchor="w",
            command=self.matrices_button_event,
        )

        self.vectores_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Menú de Vectores", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.vector_icon, anchor="w",
            command=self.vectores_button_event,
        )

        self.config_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Configuración", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.config_icon, anchor="w",
            command=self.config_button_event,
        )

        self.quit_button = ctkButton(
            self, corner_radius=0, height=40, border_spacing=10,
            text="Cerrar", fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.quit_icon, anchor="w",
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
        self.app.ops_manager.save_matrices()  # type: ignore
        self.app.ops_manager.save_vectores()  # type: ignore
        self.app.save_config()
        self.app.quit()
        remove(path.join(ASSET_PATH, "func.png"))
