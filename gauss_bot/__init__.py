from typing import (
    Any,
    Union,
)

from os import (
    path,
    walk,
)

from PIL.Image import (
    LANCZOS,
    open as open_img,
)

from customtkinter import CTkImage as ctkImage

__all__ = [
    "ASSET_PATH",
    "THEMES_PATH",
    "CONFIG_PATH",
    "MATRICES_PATH",
    "VECTORES_PATH",
    "DROPDOWN_ARROW",
    "FUNCTIONS",
    "get_dict_key",
    "resize_image",
]


def get_dict_key(dict_lookup: dict, buscando: Any) -> Union[Any, None]:
    """
    Busca un valor en un diccionario y retorna su llave.
    """

    for key, value in dict_lookup.items():
        if value == buscando or value is buscando:
            return key
    return None


def resize_image(img: ctkImage, divisors: tuple = (4, 8)) -> ctkImage:
    div1, div2 = divisors
    dark = img._dark_image
    light = img._light_image

    width, height = img._size
    new_width = int(width // div1)
    new_height = int(height // div1)

    dark_img = dark.resize((new_width, new_height), LANCZOS)
    light_img = light.resize((new_width, new_height), LANCZOS)
    return ctkImage(
        dark_image=dark_img,
        light_image=light_img,
        size=(int(new_width // div2), int(new_height // div2)),
    )


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
    open_img(path.join(ASSET_PATH, "light_dropdown_icon.png"))
)

FUNCTIONS: dict[str, ctkImage] = {
    name[:-4]: ctkImage(
        size=open_img(path.join(ASSET_PATH, f"functions/dark_{name}")).size,
        dark_image=open_img(path.join(ASSET_PATH, f"functions/light_{name}")),
        light_image=open_img(path.join(ASSET_PATH, f"functions/dark_{name}")),
    ) for name in set([
        name.split("_")[1]
        for _, _, files in walk(path.join(ASSET_PATH, "functions"))
        for name in files
    ])
}
