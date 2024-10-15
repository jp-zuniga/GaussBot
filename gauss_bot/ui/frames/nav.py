from os import path
from PIL import Image

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkButton as ctkButton,
    CTkLabel as ctkLabel,
    CTkFont as ctkFont,
    CTkImage as ctkImage,
)

IMAGE_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "assets")

class NavFrame(ctkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        self.ctk_logo = ctkImage(Image.open(path.join(IMAGE_PATH, "ctk_logo.png")))
        self.matriz_icon = ctkImage(dark_image=Image.open(path.join(IMAGE_PATH, "light_matriz_icon.png")),
                                    light_image=Image.open(path.join(IMAGE_PATH, "dark_matriz_icon.png")))
        self.vector_icon = ctkImage(dark_image=Image.open(path.join(IMAGE_PATH, "light_vector_icon.png")),
                                    light_image=Image.open(path.join(IMAGE_PATH, "dark_vector_icon.png")))
        self.config_icon = ctkImage(dark_image=Image.open(path.join(IMAGE_PATH, "light_config_icon.png")),
                                    light_image=Image.open(path.join(IMAGE_PATH, "dark_config_icon.png")))
        self.quit_icon = ctkImage(dark_image=Image.open(path.join(IMAGE_PATH, "light_quit_icon.png")),
                                  light_image=Image.open(path.join(IMAGE_PATH, "dark_quit_icon.png")))

        self.navigation_frame_label = ctkLabel(self, text="  GaussBot", image=self.ctk_logo,
                                               compound="left", font=ctkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.matrices_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Menú de Matrices",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.matriz_icon, anchor="w", command=self.app.matrices_button_event)
        self.matrices_button.grid(row=2, column=0, sticky="ew")

        self.vectores_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Menú de Vectores",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.vector_icon, anchor="w", command=self.app.vectores_button_event)
        self.vectores_button.grid(row=3, column=0, sticky="ew")

        self.settings_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Configuración",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.config_icon, anchor="w", command=self.app.config_button_event)
        self.settings_button.grid(row=5, column=0, sticky="ew")

        self.cerrar_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Cerrar",
                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                       image=self.quit_icon, anchor="w", command=self.app.quit_event)
        self.cerrar_button.grid(row=6, column=0, sticky="ew")