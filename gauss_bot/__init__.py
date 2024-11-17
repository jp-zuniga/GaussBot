"""
GaussBot es una aplicación para realizar cálculos
de álgebra lineal, como resolver sistemas de ecuaciones,
operaciones con matrices y vectores, y análisis númerico.
"""

from logging import (
    DEBUG,
    Formatter,
    FileHandler,
    getLogger,
)

from os import (
    makedirs,
    walk,
    path,
)

from random import choice
from typing import (
    Any,
    Optional,
    Union,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
)

from matplotlib.pyplot import (
    axis, close,
    rc, savefig,
    subplots, text,
)

from PIL.ImageOps import invert
from PIL.Image import (  # pylint: disable=no-name-in-module
    LANCZOS,  # definido en PIL.Image.pyi (stub file)
    Image,
    merge,
    open as open_img,
)


__all__ = [
    "delete_msg_frame",
    "delete_msg_if",
    "generate_funcs",
    "generate_range",
    "generate_sep",
    "get_dict_key",
    "latex_to_png",
    "log_setup",
    "resize_image",
    "transparent_invert",
    "ACEPTAR_ICON",
    "ANALISIS_ICON",
    "ASSET_PATH",
    "CHECK_ICON",
    "CONFIG_ICON",
    "CONFIG_PATH",
    "DATA_PATH",
    "DROPDOWN_ICON",
    "DROPUP_ICON",
    "ECUACIONES_ICON",
    "ELIMINAR_ICON",
    "ENTER_ICON",
    "ERROR_ICON",
    "FUNC_PATH",
    "FUNCTIONS",
    "FX_ICON",
    "HOME_ICON",
    "INFO_ICON",
    "INPUTS_ICON",
    "LIMPIAR_ICON",
    "LOGO",
    "LOGGER",
    "LOG_PATH",
    "MATRICES_PATH",
    "MATRIZ_ICON",
    "MOSTRAR_ICON",
    "MSGBOX_ICONS",
    "QUESTION_ICON",
    "QUIT_ICON",
    "SHUFFLE_ICON",
    "SISTEMAS_PATH",
    "THEMES_PATH",
    "VECTOR_ICON",
    "VECTORES_PATH",
    "WARNING_ICON",
]


# objeto logger global para la aplicacion
# configurado en la funcion log_setup()
LOGGER = getLogger()


################################################################################
###################   Funciones generales de la aplicación   ###################
################################################################################


def delete_msg_frame(msg_frame: Optional[ctkFrame]) -> None:
    """
    Elimina un frame de mensaje si existe.
    * msg_frame: frame a eliminar
    """

    if msg_frame is not None:
        msg_frame.destroy()
        msg_frame = None


def delete_msg_if(
    msg_frame: Optional[ctkFrame],
    masters: tuple[ctkFrame, ctkFrame]
) -> None:

    """
    Llama delete_msg_frame() si msg_frame
    esta colocado en uno de los frames indicados.
    * msg_frame: frame a eliminar
    * masters: frames donde buscar msg_frame
    """

    try:
        if msg_frame.master in masters:  # type: ignore
            delete_msg_frame(msg_frame)
    except AttributeError:
        # si msg_frame == None,
        # .master va a tirar error
        pass


def log_setup(logger=LOGGER) -> None:
    """
    Configura el logger de la aplicación y
    crea el archivo 'log.txt' si no existe.
    """

    if not path.exists(LOG_PATH):
        makedirs(DATA_PATH, exist_ok=True)
        with open(LOG_PATH, mode="w", encoding="utf-8") as _:
            pass

    # si hay mas de 1000 lineas en el log, limpiarlo
    with open(LOG_PATH, mode="r", encoding="utf-8") as log_file:
        if len(log_file.readlines()) > 1000:
            with open(LOG_PATH, mode="w", encoding="utf-8") as _:
                pass

    handler = FileHandler(
        LOG_PATH,
        mode="a",
        encoding="utf-8"
    )

    handler.setLevel(DEBUG)
    handler.setFormatter(
        Formatter(
            "%(asctime)s - %(levelname)s:\n%(message)s\n"
        )
    )

    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    logger.info("Logger configurado...")


def get_dict_key(dict_lookup: dict, buscando: Any) -> Union[Any, None]:
    """
    Busca un valor en un diccionario y retorna su llave.
    * dict_lookup: diccionario a recorrer secuencialmente
    * buscando: valor a buscar en el diccionario
    """

    for key, value in dict_lookup.items():
        # usando == or is para comparar igualdad e identidad,
        # en caso de que 'buscando' sea un objeto mutable pasado por referencia
        if value == buscando or value is buscando:
            return key
    return None


def generate_funcs(func_key: str) -> str:
    """
    Genera funciones aleatorias para mostrar ejemplos
    de como ingresar términos correctamente en RaicesFrame.
    * func_key: función aleatoria a generar y retornar
    """

    neg_range = generate_range(-10, 10)
    pos_range = generate_range(1, 10)

    placeholders: dict[str, str] = {
        "k": f"{choice(neg_range)}",
        "x^n": f"x^{choice(neg_range)}",
        "b^x": f"{choice(neg_range)}^x",
        "e^x": f"e^{choice(neg_range)}x",
        "ln(x)": f"ln({choice(pos_range)}x)",
        "log-b(x)": f"log_{choice(pos_range)}({choice(pos_range)}x)",
        "sen(x)": f"sen({choice(neg_range)}x)-{choice(pos_range)}",
        "cos(x)": f"cos({choice(neg_range)}x+{choice(pos_range)})",
        "tan(x)": f"tan({choice(neg_range)}x-{choice(pos_range)})",
    }

    return placeholders[func_key]


def generate_range(start: int, end: int) -> list[int]:
    """
    Genera una lista de enteros en un rango dado, excluyendo 0 y 1.
    Utilizado para generar coeficientes válidos en generate_funcs().
    """

    valid = list(range(start + 1, end))
    try:
        valid.remove(0)
        valid.remove(1)
    except ValueError:
        pass
    return valid


def generate_sep(orientation: bool, size: tuple[int, int]) -> ctkImage:
    """
    Retorna una CTkImage de un separador vertical u horizontal
    del tamaño 'size' y orientación 'orientation.' Estos separadores
    no pueden ser constantes porque su tamaño es variable.
    * orientation, bool: True para vertical, False para horizontal.
    * size, tuple[int, int]: tamaño de la CTkImage en pixeles (x, y)

    Usado para separar:
    * la columna de constantes de un sistema de ecuaciones en AgregarSistemas
    * los inputs de funciones en RaicesFrame.
    """

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


def latex_to_png(latex_str: str, output_file: str, font_size: int = 75) -> ctkImage:
    """
    Toma un string en formato LaTeX y lo convierte en una imagen PNG.
    * latex_str: string a convertir en PNG
    * output_file: nombre del archivo de salida
    * font_size: tamaño de la fuente en la imagen PNG
    """

    rc("text", usetex=True)
    rc("font", family="serif")

    fig_length = 10 + (len(latex_str) // 12)
    fig_height = (
        2
        if r"\\" not in latex_str
        else
        2 + int(latex_str.count(r"\\") * 2)
    )

    img_length = fig_length * 20
    img_height = fig_height * 20

    fig, _ = subplots(figsize=(fig_length, fig_height))
    axis("off")
    text(
        0.5,
        0.5,
        f"${latex_str}$",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=font_size,
    )

    savefig(
        output_file,
        format="png",
        transparent=True,
        pad_inches=0.1,
        dpi=200,
    )

    close(fig)

    img = open_img(output_file)
    inverted_img = transparent_invert(img)
    return ctkImage(
        dark_image=inverted_img,
        light_image=img,
        size=(img_length, img_height),
    )


def resize_image(img: ctkImage, divisors: tuple = (4, 8)) -> ctkImage:
    """
    Recibe una CTkImage y retorna una nueva CTkImage
    con un tamaño reducido en base a los divisores dados.
    * img: imagen a redimensionar
    * divisors: divisores para controlar el tamaño de la nueva imagen
    """

    div1, div2 = divisors
    dark: Image = img.cget("dark_image")
    light: Image = img.cget("light_image")

    size: tuple[int, int] = img.cget("size")
    width, height = size

    new_width = int(width // div1)
    new_height = int(height // div1)

    dark_img = dark.resize((new_width, new_height), LANCZOS)
    light_img = light.resize((new_width, new_height), LANCZOS)
    return ctkImage(
        dark_image=dark_img,
        light_image=light_img,
        size=(int(new_width // div2), int(new_height // div2)),
    )


def transparent_invert(img: Image) -> Image:
    """
    Invierte los colores de una imagen sin perder su transparencia.
    La funcion invert() de PIL no acepta imagenes con un canal alpha,
    entonces esta función toma un objeto Image RGBA, separa los canales,
    invierte solamente los canales RBG, y retorna una nueva imagen con
    los canales invertidos unidos con el canal alpha original.
    * img: imagen RGBA a invertir

    Utilizada cuando se genera un PNG de un string LaTeX, para que
    la imagen generada sea compatible con el modo claro y oscuro.
    """

    r, g, b, a = img.split()
    rgb_inverted = invert(merge("RGB", (r, g, b)))
    return merge("RGBA", (*rgb_inverted.split(), a))


################################################################################
###################   Paths y directorios de la aplicación   ###################
################################################################################


ASSET_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "assets"
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

THEMES_PATH = path.join(
    ASSET_PATH, "themes"
)

LOG_PATH = path.join(DATA_PATH, "log.txt")


################################################################################
############################   Íconos de NavFrame   ############################
################################################################################


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

MATRIZ_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_matriz_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_matriz_icon.png"))
)

VECTOR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_vector_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_vector_icon.png"))
)

ANALISIS_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_analisis_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_analisis_icon.png"))
)

ECUACIONES_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_ecuaciones_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_ecuaciones_icon.png"))
)

CONFIG_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_config_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_config_icon.png"))
)

QUIT_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_quit_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_quit_icon.png"))
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
    dark_image=open_img(path.join(ASSET_PATH, "dark_info_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_info_icon.png")),
)

QUESTION_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "dark_question_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "light_question_icon.png")),
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
    dark_image=open_img(path.join(ASSET_PATH, "light_aceptar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_aceptar_icon.png")),
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

ELIMINAR_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_eliminar_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_eliminar_icon.png")),
    size=(18, 18),
)

ENTER_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_enter_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_enter_icon.png")),
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

SHUFFLE_ICON = ctkImage(
    dark_image=open_img(path.join(ASSET_PATH, "light_shuffle_icon.png")),
    light_image=open_img(path.join(ASSET_PATH, "dark_shuffle_icon.png")),
    size=(18, 18),
)


################################################################################
##########################   Imagenes de funciones   ###########################
################################################################################


FUNCTIONS: dict[str, ctkImage] = {
    name[:-4]: ctkImage(
        size=open_img(path.join(FUNC_PATH, f"light_{name}")).size,
        dark_image=open_img(path.join(FUNC_PATH, f"light_{name}")),
        light_image=open_img(path.join(FUNC_PATH, f"dark_{name}"))
    ) for name in {
        name.split("_")[1]
        for _, _, files in walk(FUNC_PATH)
        for name in files
    }
}

FX_ICON = resize_image(FUNCTIONS["f(x)"], (3, 7))
