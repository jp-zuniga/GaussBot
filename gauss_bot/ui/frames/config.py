from os import path
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    set_default_color_theme,
    set_appearance_mode,
)

THEMES_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "themes")


class ConfigFrame(ctkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app

        self.modos = ["Oscuro", "Claro", "Sistema"]
        self.temas = [
            "Marsh", "Autumn", "Breeze", "Coffee", "Lavender",
            "Metal", "Midnight", "Rime", "Sky", "Violet"
        ]

        self.temas_label = ctkLabel(self, text="Tema:")
        self.temas_label.grid(row=0, column=0, padx=20, pady=10)
        self.desplegar_temas = ctkOptionMenu(self,values=self.temas, command=self.cambiar_tema)
        self.desplegar_temas.grid(row=0, column=1, padx=20, pady=10)

        self.modos_label = ctkLabel(self, text="Modo:")
        self.modos_label.grid(row=1, column=0, padx=20, pady=10)
        self.desplegar_modos = ctkOptionMenu(self, values=self.modos, command=self.light_dark)
        self.desplegar_modos.grid(row=1, column=1, padx=20, pady=10)

    def cambiar_tema(self, tema_seleccionado):
        match tema_seleccionado:
            case "Marsh":
                set_default_color_theme(path.join(THEMES_PATH, "marsh.json"))
            case "Autumn":
                set_default_color_theme(path.join(THEMES_PATH, "autumn.json"))
            case "Breeze":
                set_default_color_theme(path.join(THEMES_PATH, "breeze.json"))
            case "Coffee":
                set_default_color_theme(path.join(THEMES_PATH, "coffee.json"))
            case "Lavender":
                set_default_color_theme(path.join(THEMES_PATH, "lavender.json"))
            case "Metal":
                set_default_color_theme(path.join(THEMES_PATH, "metal.json"))
            case "Midnight":
                set_default_color_theme(path.join(THEMES_PATH, "midnight.json"))
            case "Rime":
                set_default_color_theme(path.join(THEMES_PATH, "rime.json"))
            case "Sky":
                set_default_color_theme(path.join(THEMES_PATH, "sky.json"))
            case "Violet":
                set_default_color_theme(path.join(THEMES_PATH, "violet.json"))
        
    def light_dark(self, modo_seleccionado):
        match modo_seleccionado:
            case "Claro":
                set_appearance_mode("light")
            case "Oscuro":
                set_appearance_mode("dark")
            case "Sistema":
                set_appearance_mode("system")