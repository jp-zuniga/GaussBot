"""
Definiciones de todos los íconos e
imagenes de la aplicación.
"""

from os import (
    walk,
    path,
)

from PIL.Image import open as open_img
from customtkinter import CTkImage as ctkImage

from . import (
    ASSET_PATH,
    DATA_PATH,
)


FUNC_ICON_PATH = path.join(ASSET_PATH, "func_icons")
SAVED_FUNCS_PATH = path.join(DATA_PATH, "saved_funcs")


################################################################################
############################   Íconos de NavFrame   ############################
################################################################################


LOGO = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_logo.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_logo.png"))
)

HOME_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_mode", "light_home_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_mode", "dark_home_icon.png"))
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


FUNCTIONS: dict[str, ctkImage] = {
    name[:-4]: ctkImage(
        size=open_img(path.join(FUNC_ICON_PATH, "dark_mode", f"light_{name}")).size,
        dark_image=open_img(path.join(FUNC_ICON_PATH, "dark_mode", f"light_{name}")),
        light_image=open_img(path.join(FUNC_ICON_PATH, "light_mode", f"dark_{name}"))
    ) for name in {
        name.split("_")[1]
        for _, _, files in walk(FUNC_ICON_PATH)
        for name in files
    }
}
