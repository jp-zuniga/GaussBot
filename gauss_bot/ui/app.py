from os import path
from fractions import Fraction
from customtkinter import (
    CTk as ctk,
    set_default_color_theme,
    set_appearance_mode
)

from gauss_bot.clases.matriz import Matriz
from gauss_bot.clases.vector import Vector
from gauss_bot.managers.mats_manager import MatricesManager
from gauss_bot.managers.vecs_manager import VectoresManager
from gauss_bot.managers.main_manager import OpsManager

from gauss_bot.ui.frames.nav import NavFrame
from gauss_bot.ui.frames.matrices import MatricesFrame
from gauss_bot.ui.frames.vectores import VectoresFrame
from gauss_bot.ui.frames.config import ConfigFrame

THEMES_PATH = path.join(path.dirname(path.realpath(__file__)), "themes")

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
        set_default_color_theme(path.join(THEMES_PATH, "marsh.json"))
        set_appearance_mode("dark")

        self.title("GaussBot")
        self.geometry("1200x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ops_manager = ops
        self.nav_frame = NavFrame(self, self)
        self.config_frame = ConfigFrame(self, self)
        self.matrices = MatricesFrame(self, self, self.ops_manager.mats_manager)
        self.vectores = VectoresFrame(self, self, self.ops_manager.vecs_manager)
        self.seleccionar_frame("config")

    def seleccionar_frame(self, name):
        self.nav_frame.matrices_button.configure(fg_color=("gray75", "gray25") if name == "matrices" else "transparent")
        self.nav_frame.vectores_button.configure(fg_color=("gray75", "gray25") if name == "vectores" else "transparent")

        if name == "matrices":
            self.matrices.grid(row=0, column=1, sticky="nsew")
        else:
            self.matrices.grid_forget()
        if name == "vectores":
            self.vectores.grid(row=0, column=1, sticky="nsew")
        else:
            self.vectores.grid_forget()
        if name == "config":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()

    def home_button_event(self):
        self.seleccionar_frame("home")

    def matrices_button_event(self):
        self.seleccionar_frame("matrices")

    def vectores_button_event(self):
        self.seleccionar_frame("vectores")

    def config_button_event(self):
        self.seleccionar_frame("config")

    def quit_event(self):
        self.quit()