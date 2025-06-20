"""
Funciones de utilidad generales para la aplicación.
"""

from fractions import Fraction
from logging import DEBUG, FileHandler, Formatter, getLogger, Logger
from os import makedirs, path
from typing import Any, Literal, Optional

from PIL.Image import Image, Resampling, merge, open as open_img
from PIL.ImageOps import invert
from customtkinter import CTkImage as ctkImage

from .paths import ASSET_PATH, DATA_PATH, LOG_PATH

# objeto logger global para la aplicacion
# configurado en la funcion log_setup()
LOGGER = getLogger("GaussBot")


def format_factor(
    factor: Fraction,
    mult: bool = True,
    parenth_negs: bool = False,
    parenth_fracs: bool = True,
    skip_ones: bool = True,
) -> str:
    """
    Formatea un factor para mostrarlo en el procedimiento de una operación.
    * factor:        fracción a formatear
    * mult:          si se multiplicará con otro número
    * parenth_negs:  si se debería poner números negativos en parentésis
    * parenth_fracs: si se debería poner fracciones en parentésis
    * skip_ones:     si se debería ignorar factores de 1
    """

    if factor == 1:
        if skip_ones:
            return ""
        return str(factor)
    if factor == -1:
        if skip_ones:
            return "−"
        return "−1"
    if factor.is_integer():
        if parenth_negs and factor < 0:
            return f"( −{-factor} )"
        if factor < 0:
            return f"−{-factor}"
        return str(factor)

    str_factor = f"{factor if factor > 0 else f'−{-factor}'}"
    if parenth_fracs:
        str_factor = f"( {str_factor} )"
    if mult:
        str_factor += " • "

    return str_factor


def format_proc_num(
    nums: tuple[Fraction, Fraction], operador: Literal["•", "+", "−"] = "•"
) -> str:
    """
    Formatea un par de números para mostrarlos
    en el procedimiento de una operación.
    """

    num1, num2 = nums
    if operador == "−" and num2 < 0:
        operador = "+"
        num2 *= -1
    elif operador == "+" and num2 < 0:
        operador = "−"
        num2 *= -1

    combine_nums = (
        f"{format_factor(num1, mult=False, parenth_negs=False)}"
        + f" {operador} "
        + f"{format_factor(num2, mult=False, parenth_negs=True)}"
    )

    return f"[ {combine_nums} ]"


def log_setup(logger: Logger = LOGGER) -> None:
    """
    Configura el logger de la aplicación y
    crea el archivo 'log.txt' si no existe.
    """

    if not path.exists(LOG_PATH):
        makedirs(DATA_PATH, exist_ok=True)
        with open(LOG_PATH, mode="w", encoding="utf-8") as _:
            pass

    # si hay mas de 500 lineas en el log, limpiarlo
    with open(LOG_PATH, mode="r", encoding="utf-8") as log_file:
        if len(log_file.readlines()) > 500:
            with open(LOG_PATH, mode="w", encoding="utf-8") as _:
                pass

    handler = FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter("\n%(asctime)s - %(levelname)s:\n%(message)s"))

    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    logger.info("Logger configurado...")


def get_dict_key(dict_lookup: dict[Any, Any], buscando: Any) -> Optional[Any]:
    """
    Busca un valor en un diccionario y retorna su llave.
    * dict_lookup: diccionario a recorrer secuencialmente
    * buscando:    valor a buscar en el diccionario
    """

    for key, value in dict_lookup.items():
        # comparar igualdad e identidad
        if value == buscando or value is buscando:
            return key
    return None


def generate_range(start: int, end: int) -> list[int]:
    """
    Genera una lista de enteros en un rango dado, excluyendo 0 y 1.
    Utilizado para generar coeficientes válidos en generate_funcs().
    * start: inicio del rango
    * end:   final del rango
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
    * orientation: True para vertical, False para horizontal.
    * size:        tamaño de la CTkImage en pixeles (x, y)

    Usado para separar la columna de constantes de
    un sistema de ecuaciones y los inputs de funciones.
    """

    seps: dict[bool, tuple[Image, Image]] = {
        True: (
            open_img(path.join(ASSET_PATH, "light_mode", "dark_vseparator.png")),
            open_img(path.join(ASSET_PATH, "dark_mode", "light_vseparator.png")),
        ),
        False: (
            open_img(path.join(ASSET_PATH, "light_mode", "dark_hseparator.png")),
            open_img(path.join(ASSET_PATH, "dark_mode", "light_hseparator.png")),
        ),
    }

    return ctkImage(
        size=size, dark_image=seps[orientation][1], light_image=seps[orientation][0]
    )


def resize_image(
    img: ctkImage, divisors: tuple[int | float, int | float] = (4, 8)
) -> ctkImage:
    """
    Recibe una CTkImage y retorna una nueva CTkImage
    con un tamaño reducido en base a los divisores dados.
    * img:      imagen a redimensionar
    * divisors: divisores para controlar el tamaño de la nueva imagen
    """

    div1, div2 = divisors
    dark: Image = img.cget("dark_image")
    light: Image = img.cget("light_image")

    size: tuple[int, int] = img.cget("size")
    width, height = size

    new_width = int(width // div1)
    new_height = int(height // div1)

    dark_img: ctkImage = dark.resize((new_width, new_height), Resampling.LANCZOS)
    light_img: ctkImage = light.resize((new_width, new_height), Resampling.LANCZOS)
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
