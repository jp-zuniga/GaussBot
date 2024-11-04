from os import (
    path,
    walk
)

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
    "data", "config.json",
)

MATRICES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data", "matrices.json"
)

VECTORES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data", "vectores.json"
)

DROPDOWN_ARROW = ctkImage(
    open_img(path.join(ASSET_PATH, "dropdown_icon.png"))
)

FUNCTIONS: dict[str, ctkImage] = {
    name.strip(".png"): ctkImage(
        size=open_img(path.join(ASSET_PATH, f"functions/dark_{name}")).size,
        dark_image=open_img(path.join(ASSET_PATH, f"functions/light_{name}")),
        light_image=open_img(path.join(ASSET_PATH, f"functions/dark_{name}")),
    ) for name in set([
        name.split("_")[1]
        for _, _, files in walk(path.join(ASSET_PATH, "functions"))
        for name in files
        if name.count("f(x)") == 0
    ])
}
