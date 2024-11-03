from os import path

from PIL.Image import open as open_img
from customtkinter import CTkImage as ctkImage


ASSET_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "assets"
)

THEMES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "themes"
)

CONFIG_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data",
    "config.json",
)

MATRICES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data", "matrices.json"
)

VECTORES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data", "vectores.json"
)

dropdown_icon = ctkImage(
    open_img(path.join(ASSET_PATH, "dropdown_icon.png"))
)
