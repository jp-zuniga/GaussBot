from os import path

from tkinter import StringVar
from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    set_widget_scaling,
    set_default_color_theme,
    set_appearance_mode,
)

THEMES_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "themes")
CONFIG_PATH = path.join(path.dirname(path.dirname(path.realpath(__file__))), "config.json")


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

        self.modos_dict = {
            "Claro": "light",
            "Oscuro": "dark",
            "Sistema": "system",
        }

        self.escalas_float = {
            "80%": 0.8,
            "90%": 0.9,
            "100%": 1.0,
            "110%": 1.1,
            "120%": 1.2,
        }

        self.get_tema = self.get_dict_key(self.temas_json, self.app.tema_actual)
        self.get_modo = self.get_dict_key(self.modos_dict, self.app.modo_actual)
        self.get_escala = self.get_dict_key(self.escalas_float, self.app.escala_actual)

        self.first_tema = StringVar(value=self.get_tema.split("\\")[-1])
        self.first_modo = StringVar(value=self.get_modo)
        self.first_escala = StringVar(value=self.get_escala)

        self.temas = list(self.temas_json.keys())
        self.escalas = list(self.escalas_float.keys())
        self.modos = list(self.modos_dict.keys())

        self.temas_label = ctkLabel(self, text="Tema:")
        self.temas_label.grid(row=0, column=0, padx=20, pady=10)
        self.desplegar_temas = ctkOptionMenu(self, variable=self.first_tema, values=self.temas, command=self.cambiar_tema)
        self.desplegar_temas.grid(row=0, column=1, padx=20, pady=10)

        self.modos_label = ctkLabel(self, text="Modo:")
        self.modos_label.grid(row=1, column=0, padx=20, pady=10)
        self.desplegar_modos = ctkOptionMenu(self, variable=self.first_modo, values=self.modos, command=self.light_dark)
        self.desplegar_modos.grid(row=1, column=1, padx=20, pady=10)

        self.escala_label = ctkLabel(self, text="Escala:")
        self.escala_label.grid(row=2, column=0, padx=20, pady=10)
        self.desplegar_escalas = ctkOptionMenu(self, variable=self.first_escala, values=self.escalas, command=self.cambiar_escala)
        self.desplegar_escalas.grid(row=2, column=1, padx=20, pady=10)

    def cambiar_escala(self, escala_seleccionada):
        self.app.escala_actual = self.escalas_float[escala_seleccionada]
        set_widget_scaling(self.app.escala_actual)
        self.app.save_config()

    def cambiar_tema(self, tema_seleccionado):
        self.app.tema_actual = self.temas_json[tema_seleccionado]
        set_default_color_theme(self.app.tema_actual)
        self.app.save_config()

    def light_dark(self, modo_seleccionado):
        self.app.modo_actual = self.modos_dict[modo_seleccionado]
        set_appearance_mode(self.app.modo_actual)
        self.app.save_config()

    def get_dict_key(self, dict, tema):
        for key, value in dict.items():
            if value == tema:
                return key
        return None