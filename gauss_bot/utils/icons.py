"""
Definiciones de todos los íconos e imagenes de la aplicación.
"""

from pathlib import Path
from platform import system

from PIL.Image import open as open_img
from customtkinter import CTkImage as ctkImage

from .paths import ASSET_PATH, NUMPAD_ICON_PATH

if system() == "Windows":
    # path y archivos compatibles con iconbitmap()
    APP_ICON = (
        str(ASSET_PATH / "dark_mode" / "light_logo.ico"),
        str(ASSET_PATH / "light_mode" / "dark_logo.ico"),
    )
else:
    # path y archivos compatibles con iconphoto()
    APP_ICON = (
        str(ASSET_PATH / "dark_mode" / "light_logo.png"),
        str(ASSET_PATH / "light_mode" / "dark_logo.png"),
    )


################################################################################
############################   Íconos de NavFrame   ############################
################################################################################

LOGO = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_logo.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_logo.png"),
)

INPUTS_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_input_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_input_icon.png"),
)

MATRIZ_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_matriz_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_matriz_icon.png"),
)

VECTOR_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_vector_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_vector_icon.png"),
)

ANALISIS_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_analisis_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_analisis_icon.png"),
)

ECUACIONES_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_ecuaciones_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_ecuaciones_icon.png"),
)

CONFIG_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_config_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_config_icon.png"),
)

QUIT_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_quit_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_quit_icon.png"),
)


################################################################################
########################   Íconos de CustomMessagebox   ########################
################################################################################

CHECK_ICON = ctkImage(open_img(ASSET_PATH / "check_icon.png"))
ERROR_ICON = ctkImage(open_img(ASSET_PATH / "error_icon.png"))
WARNING_ICON = ctkImage(open_img(ASSET_PATH / "warning_icon.png"))

INFO_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_info_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_info_icon.png"),
)

QUESTION_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_question_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_question_icon.png"),
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

ABOUT_US_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_about_us_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_about_us_icon.png"),
)

ACEPTAR_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_aceptar_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_aceptar_icon.png"),
)

DROPDOWN_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_dropdown_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_dropdown_icon.png"),
)

DROPLEFT_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_dropleft_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_dropleft_icon.png"),
)

DROPRIGHT_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_dropright_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_dropright_icon.png"),
)

DROPUP_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_dropup_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_dropup_icon.png"),
)

ELIMINAR_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_eliminar_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_eliminar_icon.png"),
)

ENTER_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_enter_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_enter_icon.png"),
)

LIMPIAR_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_limpiar_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_limpiar_icon.png"),
    size=(27, 20),
)

MOSTRAR_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_mostrar_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_mostrar_icon.png"),
)

SAVE_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_save_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_save_icon.png"),
)

SHUFFLE_ICON = ctkImage(
    dark_image=open_img(ASSET_PATH / "dark_mode" / "light_shuffle_icon.png"),
    light_image=open_img(ASSET_PATH / "light_mode" / "dark_shuffle_icon.png"),
)


################################################################################
##########################   Íconos de CustomNumpad   ##########################
################################################################################

NUMPAD_KEYS: dict[str, ctkImage] = {}
for file in NUMPAD_ICON_PATH.glob("*/*"):
    if file.is_file():
        name_parts: list[str] = file.stem.split("_", 1)
        if len(name_parts) > 1:
            key: str = name_parts[1]
            dark_path: Path = NUMPAD_ICON_PATH / "dark_mode" / f"light_{key}.png"
            light_path: Path = NUMPAD_ICON_PATH / "light_mode" / f"dark_{key}.png"

            if dark_path.exists() and light_path.exists():
                img = open_img(dark_path)
                NUMPAD_KEYS[key] = ctkImage(
                    size=img.size, dark_image=img, light_image=open_img(light_path)
                )
