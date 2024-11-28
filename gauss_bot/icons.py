"""
Definiciones de todos los íconos e
imagenes de la aplicación.
"""

from os import (
    walk,
    path,
)

from customtkinter import CTkImage as ctkImage
from PIL.Image import open as open_img

from . import (
    ASSET_PATH,
    DATA_PATH,
)


__all__ = [
    "ACEPTAR_ICON",
    "ANALISIS_ICON",
    "APP_ICON",
    "CHECK_ICON",
    "CONFIG_ICON",
    "DROPDOWN_ICON",
    "DROPLEFT_ICON",
    "DROPRIGHT_ICON",
    "DROPUP_ICON",
    "ECUACIONES_ICON",
    "ELIMINAR_ICON",
    "ENTER_ICON",
    "ERROR_ICON",
    "NUMPAD_KEYS",
    "INFO_ICON",
    "INPUTS_ICON",
    "LIMPIAR_ICON",
    "LOGO",
    "MATRIZ_ICON",
    "MOSTRAR_ICON",
    "MSGBOX_ICONS",
    "NUMPAD_ICON_PATH",
    "QUESTION_ICON",
    "QUIT_ICON",
    "SHUFFLE_ICON",
    "VECTOR_ICON",
    "WARNING_ICON",
]


NUMPAD_ICON_PATH = path.join(ASSET_PATH, "numpad_icons")
SAVED_FUNCS_PATH = path.join(DATA_PATH, "saved_funcs")

APP_ICON = (
    path.join(ASSET_PATH, "light_logo.ico"),
    path.join(ASSET_PATH, "dark_logo.ico"),
)


################################################################################
############################   Íconos de NavFrame   ############################
################################################################################


LOGO = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_logo.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_logo.png"))
)

INPUTS_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_input_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_input_icon.png"))
)

MATRIZ_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_matriz_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_matriz_icon.png"))
)

VECTOR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_vector_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_vector_icon.png"))
)

ANALISIS_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_analisis_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_analisis_icon.png"))
)

ECUACIONES_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_ecuaciones_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_ecuaciones_icon.png"))
)

CONFIG_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_config_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_config_icon.png"))
)

QUIT_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_quit_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_quit_icon.png"))
)


################################################################################
########################   Íconos de CustomMessagebox   ########################
################################################################################


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
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_info_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_info_icon.png")),
)

QUESTION_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_question_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_question_icon.png")),
)

MSGBOX_ICONS = {
    "check": CHECK_ICON,
    "error": ERROR_ICON,
    "info": INFO_ICON,
    "question": QUESTION_ICON,
    "warning": WARNING_ICON,
}


################################################################################
############################   Íconos de botones   #############################
################################################################################


ACEPTAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_aceptar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_aceptar_icon.png")),
    size=(18, 18),
)

DROPDOWN_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_dropdown_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_dropdown_icon.png")),
    size=(18, 18),
)

DROPLEFT_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_dropleft_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_dropleft_icon.png")),
    size=(18, 18),
)

DROPRIGHT_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_dropright_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_dropright_icon.png")),
    size=(18, 18),
)

DROPUP_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_dropup_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_dropup_icon.png")),
    size=(18, 18),
)

ELIMINAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_eliminar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_eliminar_icon.png")),
    size=(18, 18),
)

ENTER_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_enter_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_enter_icon.png")),
    size=(18, 18),
)

LIMPIAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_limpiar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_limpiar_icon.png")),
    size=(25, 18),
)

MOSTRAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_mostrar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_mostrar_icon.png")),
    size=(18, 18),
)

SHUFFLE_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_shuffle_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_shuffle_icon.png")),
    size=(18, 18),
)


################################################################################
##########################   Imagenes de funciones   ###########################
################################################################################


NUMPAD_KEYS: dict[str, ctkImage] = {
    name[:-4]: ctkImage(
        size=open_img(path.join(NUMPAD_ICON_PATH, "dark_mode", f"light_{name}")).size,
        dark_image=open_img(path.join(NUMPAD_ICON_PATH, "dark_mode", f"light_{name}")),
        light_image=open_img(path.join(NUMPAD_ICON_PATH, "light_mode", f"dark_{name}"))
    ) for name in {
        name.split("_")[1]
        for _, _, files in walk(NUMPAD_ICON_PATH)
        for name in files
    }
}
