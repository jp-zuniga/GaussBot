from fractions import Fraction
from json import dump, load
from os import path

from customtkinter import CTk as ctk
from customtkinter import (
    set_widget_scaling,
    set_default_color_theme,
    set_appearance_mode,
)

from gauss_bot.clases.matriz import Matriz
from gauss_bot.clases.vector import Vector
from gauss_bot.managers.main_manager import OpsManager
from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager

from gauss_bot.ui.frames.config import ConfigFrame, THEMES_PATH, CONFIG_PATH
from gauss_bot.ui.frames.matrices import MatricesFrame
from gauss_bot.ui.frames.nav import NavFrame, ASSET_PATH
from gauss_bot.ui.frames.vectores import VectoresFrame

matrices_dict = {
    "A": Matriz(aumentada=False, filas=2, columnas=2, valores=[[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]]),
    "B": Matriz(aumentada=False, filas=2, columnas=2, valores=[[Fraction(5), Fraction(6)], [Fraction(7), Fraction(8)]]),
    "C": Matriz(aumentada=False, filas=2, columnas=2, valores=[[Fraction(9), Fraction(10)], [Fraction(11), Fraction(12)]])
}

vectores_dict = {
    "a": Vector([Fraction(1), Fraction(2), Fraction(3)]),
    "b": Vector([Fraction(4), Fraction(5), Fraction(6)]),
    "c": Vector([Fraction(7), Fraction(8), Fraction(9)])
}

ops = OpsManager()
test_mats = MatricesManager(matrices_dict, ops)
test_vecs = VectoresManager(vectores_dict, ops)
ops.mats_manager = test_mats
ops.vecs_manager = test_vecs


class App(ctk):
    def __init__(self):
        super().__init__()
        self.load_config()

        self.title("GaussBot")
        self.set_icon(self.modo_actual)
        self.geometry("1200x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ops_manager = ops
        self.mats_manager = ops.mats_manager
        self.vecs_manager = ops.vecs_manager
        self.nav_frame = NavFrame(self, self)
        self.config_frame = ConfigFrame(self, self)
        self.matrices = MatricesFrame(self, self, self.mats_manager)
        self.vectores = VectoresFrame(self, self, self.vecs_manager)

        self.frames = {
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
        with open(CONFIG_PATH, "r") as config_file:
            self.config = load(config_file)
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

    def seleccionar_frame(self, nombre):
        for nombre_frame, button in self.buttons.items():
            button.configure(fg_color=("gray75", "gray25") if nombre == nombre_frame else "transparent")

        for nombre_frame, frame in self.frames.items():
            if nombre == nombre_frame:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def home_button_event(self):
        self.seleccionar_frame("home")

    def matrices_button_event(self):
        self.seleccionar_frame("matrices")

    def vectores_button_event(self):
        self.seleccionar_frame("vectores")

    def config_button_event(self):
        self.seleccionar_frame("config")

    def quit_event(self):
        self.save_config()
        self.quit()