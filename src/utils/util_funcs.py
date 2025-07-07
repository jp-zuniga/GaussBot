"""
Funciones de utilidad generales para la aplicación.
"""

from fractions import Fraction
from importlib.resources import as_file, files
from logging import DEBUG, FileHandler, Formatter, Logger, getLogger
from typing import Literal

from PIL.Image import Image, Resampling, merge, open as open_img
from PIL.ImageOps import invert
from customtkinter import CTkImage as ctkImage

from .paths import DARK_NUMPAD_ICONS, DATA_PATH, LIGHT_NUMPAD_ICONS, LOG_PATH, PKG

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
    nums: tuple[Fraction, Fraction],
    operador: Literal["•", "+", "−"] = "•",  # type: ignore[reportRedeclaration]
) -> str:
    """
    Formatear un par de números para mostrarlos
    en el procedimiento de una operación.

    Args:
        nums:     El par de números a formatear.
        operador: El operador matemático a colocar entre los números.

    Returns:
        str: La operación entre los números formateada.

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
        f" {operador} "
        f"{format_factor(num2, mult=False, parenth_negs=True)}"
    )

    return f"[ {combine_nums} ]"


def load_mode_icon(path: str, size: tuple[int, int] = (20, 20)) -> ctkImage:
    """
    Cargar íconos de modo claro/oscuro.

    Args:
        path: Dirección del ícono dentro del directorio de assets.
        size: Tamaño a pasar a CTkImage.

    Returns:
        CTkImage: Objeto de imagen conteniendo los íconos.

    """

    with (
        as_file(files(PKG) / f"assets/icons/dark/{path}") as d_path,
        as_file(files(PKG) / f"assets/icons/light/{path}") as l_path,
    ):
        return ctkImage(
            size=size,
            dark_image=open_img(l_path),
            light_image=open_img(d_path),
        )


def load_numpad_icons() -> dict[str, ctkImage]:
    """
    Cargar los íconos utilizados en CustomNumpad y almacernalos en un diccionario.
    """

    icons: dict[str, ctkImage] = {}

    for item in DARK_NUMPAD_ICONS.iterdir():
        if item.name.endswith(".png"):
            with (
                as_file(DARK_NUMPAD_ICONS / item.name) as d_path,
                as_file(LIGHT_NUMPAD_ICONS / item.name) as l_path,
            ):
                img = open_img(l_path)
                icons[item.name[:-4]] = ctkImage(
                    size=img.size,
                    dark_image=img,
                    light_image=open_img(d_path),
                )

    return icons


def load_single_icon(path: str) -> ctkImage:
    """
    Cargar íconos independientes de modo.

    Args:
        path: Dirección del ícono dentro del directorio de assets.

    Returns:
        CTkImage: Objeto de imagen conteniendo el ícono.

    """

    with as_file(files(PKG) / f"assets/icons/{path}") as icon_path:
        return ctkImage(open_img(icon_path))


def log_setup(logger: Logger = LOGGER) -> None:
    """
    Configurar el logger de la aplicación y crear el archivo 'log.txt' si no existe.

    Args:
        logger: Objeto Logger a configurar.

    """

    if not LOG_PATH.exists():
        DATA_PATH.mkdir(exist_ok=True)
        LOG_PATH.touch()

    # si hay mas de 500 lineas en el log, limpiarlo
    with LOG_PATH.open() as log_file:
        if len(log_file.readlines()) > 500:
            LOG_PATH.write_text("")

    handler = FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter("\n%(asctime)s - %(levelname)s:\n%(message)s"))

    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    logger.info("Logger configurado...")


def generate_range(start: int, end: int) -> list[int]:
    """
    Generar una lista de enteros en un rango dado, excluyendo 0 y 1.

    Args:
        start: Inicio del rango.
        end:   Final del rango.

    Returns:
        list[int]: Números aleatorios generados.

    """

    return [x for x in range(start + 1, end) if x not in (0, 1)]


def generate_sep(orientation: bool, size: tuple[int, int]) -> ctkImage:
    """
    Crear una imagen de un separador vertical u horizontal.

    Args:
        orientation: Dirección del separador: True para vertical, False para horizontal.
        size:        Tamaño de la CTkImage en pixeles (x, y).

    Returns:
        CTkImage: Imagen del separador creada.

    """

    return load_mode_icon("v_separator.png" if orientation else "h_separator.png", size)


def resize_image(img: ctkImage, per: float = 0.75) -> ctkImage:
    """
    Reducir el tamaño de una CTkImage según el porcentaje especificado.

    Args:
        img: Imagen a redimensionar.
        per: Porcentaje a aplicar a la imagen.

    Returns:
        CTkImage: Imagen redimensionada.

    """

    width, height = img.cget("size")
    dark: Image = img.cget("dark_image")
    light: Image = img.cget("light_image")

    new_width = int(width * per)
    new_height = int(height * per)

    dark_img: Image = dark.resize((new_width, new_height), Resampling.LANCZOS)
    light_img: Image = light.resize((new_width, new_height), Resampling.LANCZOS)
    return ctkImage(dark_image=dark_img, light_image=light_img, size=dark_img.size)


def transparent_invert(img: Image) -> Image:
    """
    Invertir los colores de una imagen sin perder su transparencia.

    Args:
        img: Imagen RGBA a invertir.

    Returns:
        Image: Imagen transparente invertida.

    """

    r, g, b, a = img.split()
    rgb_inverted = invert(merge("RGB", (r, g, b)))

    return merge("RGBA", (*rgb_inverted.split(), a))
