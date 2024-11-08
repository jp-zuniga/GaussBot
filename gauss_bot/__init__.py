from typing import (
    Any,
    Optional,
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

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
)

__all__ = [
    "ASSET_PATH",
    "THEMES_PATH",
    "DATA_PATH",
    "CONFIG_PATH",
    "MATRICES_PATH",
    "VECTORES_PATH",
    "LOGO",
    "HOME_ICON",
    "INPUTS_ICON",
    "ECUACIONES_ICON",
    "MATRIZ_ICON",
    "VECTOR_ICON",
    "CONFIG_ICON",
    "QUIT_ICON",
    "DROPDOWN_ARROW",
    "FUNCTIONS",
    "get_dict_key",
    "resize_image",
]


def delete_msg_frame(msg_frame: Optional[ctkFrame]) -> None:
    if msg_frame is not None:
        msg_frame.destroy()
        msg_frame = None


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

DATA_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data"
)

CONFIG_PATH = path.join(
    DATA_PATH, "config.json",
)

MATRICES_PATH = path.join(
    DATA_PATH, "matrices.json"
)

VECTORES_PATH = path.join(
    DATA_PATH, "vectores.json"
)

LOGO = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_logo.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_logo.png"))
)

HOME_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_home_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_home_icon.png"))
)

INPUTS_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_input_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_input_icon.png"))
)

ECUACIONES_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_ecuaciones_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_ecuaciones_icon.png"))
)

MATRIZ_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_matriz_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_matriz_icon.png"))
)

VECTOR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_vector_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_vector_icon.png"))
)

CONFIG_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_config_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_config_icon.png"))
)

QUIT_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_quit_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_quit_icon.png"))
)

DROPDOWN_ARROW = ctkImage(
    open_img(path.join(ASSET_PATH, "light_dropdown_icon.png"))
)

FUNCTIONS: dict[str, ctkImage] = {
    name[:-4]: ctkImage(
        size=open_img(path.join(ASSET_PATH, f"functions/light_{name}")).size,
        dark_image=open_img(path.join(ASSET_PATH, f"functions/light_{name}")),
        light_image=open_img(path.join(ASSET_PATH, f"functions/dark_{name}"))
    ) for name in set([
        name.split("_")[1]
        for _, _, files in walk(path.join(ASSET_PATH, "functions"))
        for name in files
    ])
}
