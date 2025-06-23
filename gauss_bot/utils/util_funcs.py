"""
Funciones de utilidad generales para la aplicación.
"""

from fractions import Fraction
from logging import DEBUG, FileHandler, Formatter, Logger, getLogger
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
    Formatear un factor para mostrarlo en el procedimiento de una operación.

    Args:
        factor:        Fracción a formatear.
        mult:          Si se multiplicará con otro número.
        parenth_negs:  Si se debería poner números negativos en parentésis.
        parenth_fracs: Si se debería poner fracciones en parentésis.
        skip_ones:     Si se debería ignorar factores de 1.

    Returns:
        str: El factor formateado según los parámetros.
    ---
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
    Formatear un par de números para mostrarlos
    en el procedimiento de una operación.

    Args:
        nums:     El par de números a formatear.
        operador: El operador matemático a colocar entre los números.

    Returns:
        str: La operación entre los números formateada.
    ---
    """

    num1, num2 = nums
    if operador == "−" and num2 < 0:
        operador: str = "+"
        num2 *= -1
    elif operador == "+" and num2 < 0:
        operador: str = "−"
        num2 *= -1

    combine_nums = (
        f"{format_factor(num1, mult=False, parenth_negs=False)}"
        + f" {operador} "
        + f"{format_factor(num2, mult=False, parenth_negs=True)}"
    )

    return f"[ {combine_nums} ]"


def log_setup(logger: Logger = LOGGER) -> None:
    """
    Configurar el logger de la aplicación y
    crear el archivo 'log.txt' si no existe.

    Args:
        logger: Objeto Logger a configurar.
    ---
    """

    if not LOG_PATH.exists():
        DATA_PATH.mkdir(exist_ok=True)
        LOG_PATH.touch()

    # si hay mas de 500 lineas en el log, limpiarlo
    with open(LOG_PATH, mode="r", encoding="utf-8") as log_file:
        if len(log_file.readlines()) > 500:
            LOG_PATH.write_text("")

    handler = FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter("\n%(asctime)s - %(levelname)s:\n%(message)s"))

    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    logger.info("Logger configurado...")


def get_dict_key(dict_lookup: dict, buscando: Any) -> Optional[Any]:
    """
    Buscar un valor en un diccionario y retornar su llave.

    Args:
        dict_lookup: Diccionario a recorrer secuencialmente.
        buscando:    Valor a buscar en el diccionario.

    Returns:
        Any:  La llave del valor especificado, si se encuentra.
        None: Si la llave no se encuentra.
    ---
    """

    if buscando not in dict_lookup.values():
        return None

    for key, value in dict_lookup.items():
        # comparar igualdad e identidad
        if value == buscando or value is buscando:
            return key

    # fallback, la función debería retornar antes de llegar aquí
    return None


def generate_range(start: int, end: int) -> list[int]:
    """
    Generar una lista de enteros en un rango dado, excluyendo 0 y 1.

    Args:
        start: Inicio del rango.
        end:   Final del rango.

    Returns:
        list[int]: Números aleatorios generados.
    ---
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
    Crear una imagen de un separador vertical u horizontal.

    Args:
        orientation: Dirección del separador: True para vertical, False para horizontal.
        size:        Tamaño de la CTkImage en pixeles (x, y).

    Returns:
        CTkImage: Imagen del separador creada.
    ---
    """

    seps: dict[bool, tuple[Image, Image]] = {
        True: (
            open_img(ASSET_PATH / "light_mode" / "dark_vseparator.png"),
            open_img(ASSET_PATH / "dark_mode" / "light_vseparator.png"),
        ),
        False: (
            open_img(ASSET_PATH / "light_mode" / "dark_hseparator.png"),
            open_img(ASSET_PATH / "dark_mode" / "light_hseparator.png"),
        ),
    }

    return ctkImage(
        size=size, dark_image=seps[orientation][1], light_image=seps[orientation][0]
    )


def resize_image(
    img: ctkImage, divisors: tuple[int | float, int | float] = (4, 8)
) -> ctkImage:
    """
    Reducir el tamaño de una CTkImage según los divisores dados.

    Args:
        img:      Imagen a redimensionar.
        divisors: Divisores para controlar el tamaño de la nueva imagen.

    Returns:
        CTkImage: Imagen redimensionar.
    ---
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
    Invertir los colores de una imagen sin perder su transparencia.

    Args:
        img: Imagen RGBA a invertir.

    Returns:
        Image: Imagen transparente invertida.
    ---
    """

    r, g, b, a = img.split()
    rgb_inverted = invert(merge("RGB", (r, g, b)))

    return merge("RGBA", (*rgb_inverted.split(), a))
