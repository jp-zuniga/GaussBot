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

        self.temas_json = {
            "Autumn": path.join(THEMES_PATH, "autumn.json"),
            "Breeze": path.join(THEMES_PATH, "breeze.json"),
            "Cherry": path.join(THEMES_PATH, "cherry.json"),
            "Carrot": path.join(THEMES_PATH, "carrot.json"),
            "Coffee": path.join(THEMES_PATH, "coffee.json"),
            "Lavender": path.join(THEMES_PATH, "lavender.json"),
            "Marsh": path.join(THEMES_PATH, "marsh.json"),
            "Metal": path.join(THEMES_PATH, "metal.json"),
            "Midnight": path.join(THEMES_PATH, "midnight.json"),
            "Orange": path.join(THEMES_PATH, "orange.json"),
            "Patina": path.join(THEMES_PATH, "patina.json"),
            "Pink": path.join(THEMES_PATH, "pink.json"),
            "Red": path.join(THEMES_PATH, "red.json"),
            "Rime": path.join(THEMES_PATH, "rime.json"),
            "Rose": path.join(THEMES_PATH, "rose.json"),
            "Sky": path.join(THEMES_PATH, "sky.json"),
            "Violet": path.join(THEMES_PATH, "violet.json"),
            "Yellow": path.join(THEMES_PATH, "yellow.json"),
        }

        self.temas = list(self.temas_json.keys())
        self.modos = ["Claro", "Oscuro", "Sistema"]

        self.temas_label = ctkLabel(self, text="Tema:")
        self.temas_label.grid(row=0, column=0, padx=20, pady=10)
        self.desplegar_temas = ctkOptionMenu(self,values=self.temas, command=self.cambiar_tema)
        self.desplegar_temas.grid(row=0, column=1, padx=20, pady=10)

        self.modos_label = ctkLabel(self, text="Modo:")
        self.modos_label.grid(row=1, column=0, padx=20, pady=10)
        self.desplegar_modos = ctkOptionMenu(self, values=self.modos, command=self.light_dark)
        self.desplegar_modos.grid(row=1, column=1, padx=20, pady=10)

    def cambiar_tema(self, tema_seleccionado):
        set_default_color_theme(self.temas_json[tema_seleccionado])
        
    def light_dark(self, modo_seleccionado):
        match modo_seleccionado:
            case "Claro":
                set_appearance_mode("light")
            case "Oscuro":
                set_appearance_mode("dark")
            case "Sistema":
                set_appearance_mode("system")