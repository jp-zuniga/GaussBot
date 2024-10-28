"""
Implementación de la clase NavFrame,
la barra de navegación de la aplicación.
"""

from os import path

from PIL import Image
from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkImage as ctkImage,
)

from gauss_bot import ASSET_PATH


class NavFrame(ctkFrame):
    """
    Barra de navigación que contiene botones
    para navegar entre los distintos frames de la aplicación.
    """

    def __init__(self, master, app) -> None:
        super().__init__(master, corner_radius=0)
        self.app = app

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)
        self.configure(fg_color=self.app.theme_config["CTk"]["fg_color"])

        self.logo = ctkImage(
            dark_image=Image.open(path.join(ASSET_PATH, "light_logo.png")),
            light_image=Image.open(path.join(ASSET_PATH, "dark_logo.png"))
        )

        self.ecuaciones_icon = ctkImage(
            dark_image=Image.open(path.join(ASSET_PATH, "light_ecuaciones_icon.png")),
            light_image=Image.open(path.join(ASSET_PATH, "dark_ecuaciones_icon.png"))
        )

        self.matriz_icon = ctkImage(
            dark_image=Image.open(path.join(ASSET_PATH, "light_matriz_icon.png")),
            light_image=Image.open(path.join(ASSET_PATH, "dark_matriz_icon.png"))
        )

        self.vector_icon = ctkImage(
            dark_image=Image.open(path.join(ASSET_PATH, "light_vector_icon.png")),
            light_image=Image.open(path.join(ASSET_PATH, "dark_vector_icon.png"))
        )

        self.config_icon = ctkImage(
            dark_image=Image.open(path.join(ASSET_PATH, "light_config_icon.png")),
            light_image=Image.open(path.join(ASSET_PATH, "dark_config_icon.png"))
        )

        self.quit_icon = ctkImage(
            dark_image=Image.open(path.join(ASSET_PATH, "light_quit_icon.png")),
            light_image=Image.open(path.join(ASSET_PATH, "dark_quit_icon.png"))
        )

        self.nav_frame_label = ctkLabel(
            self, text="  GaussBot",
            image=self.logo, compound="left",
            font=ctkFont(size=16, weight="bold"),
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

        self.nav_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.ecuaciones_button.grid(row=1, column=0, padx=10, pady=3, sticky="ew")
        self.matrices_button.grid(row=2, column=0, padx=10, pady=3, sticky="ew")
        self.vectores_button.grid(row=3, column=0, padx=10, pady=3, sticky="ew")
        self.config_button.grid(row=5, column=0, padx=10, pady=3, sticky="ew")
        self.quit_button.grid(row=6, column=0, padx=10, pady=3, sticky="ew")

        self.frames = {
            "ecuaciones": self.app.ecuaciones,
            "matrices": self.app.matrices,
            "vectores": self.app.vectores,
            "config": self.app.config_frame
        }

        self.buttons = {
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

    def matrices_button_event(self) -> None:
        self.seleccionar_frame("matrices")

    def vectores_button_event(self) -> None:
        self.seleccionar_frame("vectores")

    def ecuaciones_button_event(self) -> None:
        self.seleccionar_frame("ecuaciones")

    def config_button_event(self) -> None:
        self.seleccionar_frame("config")

    def quit_event(self) -> None:
        self.app.ops_manager.save_matrices()
        self.app.ops_manager.save_vectores()
        self.app.save_config()
        self.app.quit()
