from os import path
from customtkinter import (
    CTk as ctk,
    set_default_color_theme,
    set_appearance_mode
)

from gauss_bot.ui.frames.home import HomeFrame
from gauss_bot.ui.frames.matrices import MatricesFrame
from gauss_bot.ui.frames.vectores import VectoresFrame
from gauss_bot.ui.frames.nav import NavigationFrame
from gauss_bot.ui.frames.settings import SettingsFrame

THEME_PATH = path.join(path.dirname(path.realpath(__file__)), "theme")


class App(ctk):
    def __init__(self):
        super().__init__()

        set_default_color_theme(path.join(THEME_PATH, "sky.json"))
        set_appearance_mode("light")

        self.title("GaussBot")
        self.geometry("700x450")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navigation_frame = NavigationFrame(self, self)
        self.home_frame = HomeFrame(self, self)
        self.settings_frame = SettingsFrame(self, self)
        self.matrices = MatricesFrame(self)
        self.vectores = VectoresFrame(self)

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.navigation_frame.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.navigation_frame.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "matrices" else "transparent")
        self.navigation_frame.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "vectores" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "matrices":
            self.matrices.grid(row=0, column=1, sticky="nsew")
        else:
            self.matrices.grid_forget()
        if name == "vectores":
            self.vectores.grid(row=0, column=1, sticky="nsew")
        else:
            self.vectores.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("matrices")

    def frame_3_button_event(self):
        self.select_frame_by_name("vectores")