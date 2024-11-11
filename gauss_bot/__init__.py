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
    Image,
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
    "SISTEMAS_PATH",
    "MATRICES_PATH",
    "VECTORES_PATH",
    "FUNC_PATH",
    "LOGO",
    "HOME_ICON",
    "INPUTS_ICON",
    "ECUACIONES_ICON",
    "MATRIZ_ICON",
    "VECTOR_ICON",
    "CONFIG_ICON",
    "QUIT_ICON",
    "CHECK_ICON",
    "ERROR_ICON",
    "WARNING_ICON",
    "INFO_ICON",
    "QUESTION_ICON",
    "MSGBOX_ICONS",
    "ENTER_ICON",
    "SHUFFLE_ICON",
    "ACEPTAR_ICON",
    "LIMPIAR_ICON",
    "MOSTRAR_ICON",
    "ELIMINAR_ICON",
    "DROPDOWN_ICON",
    "DROPUP_ICON",
    "FUNCTIONS",
    "F_ICON",
    "delete_msg_frame",
    "get_dict_key",
    "resize_image",
    "generate_sep",
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


def generate_sep(orientation: bool, size: tuple[int, int]) -> ctkImage:
    seps: dict[bool, tuple[Image, Image]] = {
        True: (
            open_img(path.join(ASSET_PATH, "dark_vseparator.png")),
            open_img(path.join(ASSET_PATH, "light_vseparator.png")),
        ),
        False: (
            open_img(path.join(ASSET_PATH, "dark_hseparator.png")),
            open_img(path.join(ASSET_PATH, "light_hseparator.png")),
        ),
    }

    return ctkImage(
        size=size,
        dark_image=seps[orientation][1],
        light_image=seps[orientation][0],
    )


ASSET_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "assets"
)

THEMES_PATH = path.join(
    ASSET_PATH, "themes"
)

DATA_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data"
)

CONFIG_PATH = path.join(
    DATA_PATH, "config.json",
)

SISTEMAS_PATH = path.join(
    DATA_PATH, "sistemas.json"
)

MATRICES_PATH = path.join(
    DATA_PATH, "matrices.json"
)

VECTORES_PATH = path.join(
    DATA_PATH, "vectores.json"
)

FUNC_PATH = path.join(
    ASSET_PATH, "functions"
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


CHECK_ICON = ctkImage(
    open_img(path.join(ASSET_PATH, "check_icon.png")),
)

ERROR_ICON = ctkImage(
    open_img(path.join(ASSET_PATH, "error_icon.png")),
)

WARNING_ICON = ctkImage(
    open_img(path.join(ASSET_PATH, "warning_icon.png")),
)

INFO_ICON = ctkImage(
    open_img(path.join(ASSET_PATH, "info_icon.png")),
)

QUESTION_ICON = ctkImage(
    open_img(path.join(ASSET_PATH, "question_icon.png")),
)

MSGBOX_ICONS = {
    "check": CHECK_ICON,
    "cancel": ERROR_ICON,
    "info": INFO_ICON,
    "question": QUESTION_ICON,
    "warning": WARNING_ICON,
}



ENTER_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_enter_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_enter_icon.png")),
    size=(18, 18),
)

SHUFFLE_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_shuffle_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_shuffle_icon.png")),
    size=(18, 18),
)

ACEPTAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_aceptar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_aceptar_icon.png")),
    size=(18, 18),
)

LIMPIAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_limpiar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_limpiar_icon.png")),
    size=(25, 18),
)

MOSTRAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_mostrar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_mostrar_icon.png")),
    size=(18, 18),
)

ELIMINAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_eliminar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_eliminar_icon.png")),
    size=(18, 18),
)

DROPDOWN_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_dropdown_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_dropdown_icon.png")),
    size=(18, 18),
)

DROPUP_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_dropup_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_dropup_icon.png")),
    size=(18, 18),
)


FUNCTIONS: dict[str, ctkImage] = {
    name[:-4]: ctkImage(
        size=open_img(path.join(FUNC_PATH, f"light_{name}")).size,
        dark_image=open_img(path.join(FUNC_PATH, f"light_{name}")),
        light_image=open_img(path.join(FUNC_PATH, f"dark_{name}"))
    ) for name in set([
        name.split("_")[1]
        for _, _, files in walk(FUNC_PATH)
        for name in files
    ])
}

FX_ICON = resize_image(FUNCTIONS["f(x)"], (3, 7))
