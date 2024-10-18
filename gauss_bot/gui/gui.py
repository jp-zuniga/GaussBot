from json import dump, load
from os import path

from customtkinter import CTk as ctk
from customtkinter import (
    set_widget_scaling,
    set_default_color_theme,
    set_appearance_mode,
)

from gauss_bot.managers.ops_manager import OpsManager

from gauss_bot.gui.frames.nav import NavFrame, ASSET_PATH
from gauss_bot.gui.frames.matrices import MatricesFrame
from gauss_bot.gui.frames.vectores import VectoresFrame
from gauss_bot.gui.frames.ecuaciones import EcuacionesFrame
from gauss_bot.gui.frames.config import ConfigFrame, THEMES_PATH, CONFIG_PATH


class GaussUI(ctk):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.set_icon(self.modo_actual)

        self.title("GaussBot")
        #! self.state("zoomed")
        self.geometry("1200x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ops_manager = OpsManager()
        self.mats_manager = self.ops_manager.mats_manager
        self.vecs_manager = self.ops_manager.vecs_manager

        self.nav_frame = NavFrame(self, self)
        self.ecuaciones = EcuacionesFrame(self, self, self.mats_manager)
        self.matrices = MatricesFrame(self, self, self.mats_manager)
        self.vectores = VectoresFrame(self, self, self.vecs_manager)
        self.config_frame = ConfigFrame(self, self)

        self.frames = {
            "ecuaciones": self.ecuaciones,
            "matrices": self.matrices,
            "vectores": self.vectores,
            "config": self.config_frame
        }

        self.buttons = {
            "matrices": self.nav_frame.matrices_button,
            "vectores": self.nav_frame.vectores_button
        }

    def matriz_vector(self):
        pass

    def load_config(self):
        if path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as config_file:
                self.config = load(config_file)
        else:
            self.config = {
                "tema": "metal.json",
                "escala": 1.0,
                "modo": "dark"
            }

        self.tema_actual = self.config["tema"]
        self.escala_actual = self.config["escala"]
        self.modo_actual = self.config["modo"]

        set_widget_scaling(self.escala_actual)
        set_default_color_theme(path.join(THEMES_PATH, self.tema_actual))
        set_appearance_mode(self.modo_actual)

    def save_config(self):
        self.config["tema"] = self.tema_actual
        self.config["escala"] = self.escala_actual
        self.config["modo"] = self.modo_actual
        with open(CONFIG_PATH, "w") as config_file:
            dump(self.config, config_file, indent=4)

    def set_icon(self, modo):
        if modo == "light":
            self.iconbitmap(path.join(ASSET_PATH, "dark_logo.ico"))
        elif modo == "dark":
            self.iconbitmap(path.join(ASSET_PATH, "light_logo.ico"))
        else:
            raise ValueError("Input inválido!")

    def seleccionar_frame(self, nombre):
        for nombre_frame, button in self.buttons.items():
            button.configure(fg_color=("gray75", "gray25") if nombre == nombre_frame else "transparent")

        for nombre_frame, frame in self.frames.items():
            if nombre == nombre_frame:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def matrices_button_event(self):
        self.seleccionar_frame("matrices")

    def vectores_button_event(self):
        self.seleccionar_frame("vectores")

    def ecuaciones_button_event(self):
        self.seleccionar_frame("ecuaciones")

    def config_button_event(self):
        self.seleccionar_frame("config")

    def quit_event(self):
        self.ops_manager.save_matrices()
        self.ops_manager.save_vectores()
        self.save_config()
        self.quit()