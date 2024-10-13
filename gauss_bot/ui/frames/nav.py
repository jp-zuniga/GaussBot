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

class NavigationFrame(ctkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        self.ctk_logo = ctkImage(Image.open(path.join(IMAGE_PATH, "ctk_logo.png")), size=(26, 26))
        self.home_icon = ctkImage(light_image=Image.open(path.join(IMAGE_PATH, "home_icon.png")), size=(20, 20))
        self.matriz_icon = ctkImage(light_image=Image.open(path.join(IMAGE_PATH, "matriz_icon.png")), size=(20, 20))
        self.vector_icon = ctkImage(light_image=Image.open(path.join(IMAGE_PATH, "vector_icon.png")), size=(20, 20))

        self.navigation_frame_label = ctkLabel(self, text="  GaussBot", image=self.ctk_logo,
                                               compound="left", font=ctkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                     image=self.home_icon, anchor="w", command=self.app.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Menú de Matrices",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.matriz_icon, anchor="w", command=self.app.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctkButton(self, corner_radius=0, height=40, border_spacing=10, text="Menú de Vectores",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        image=self.vector_icon, anchor="w", command=self.app.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")