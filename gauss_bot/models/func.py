"""
Implementación de la clase Func.
"""

from fractions import Fraction
from os import path
from re import match

from customtkinter import CTkImage as ctkImage
from matplotlib.pyplot import (
    axis, close,
    rc, savefig,
    subplots, text,
)

from PIL.Image import open as open_img
from sympy import (
    Reals, Interval,
    Set, Symbol,
    latex, parse_expr,
)

from sympy.calculus.util import continuous_domain
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
)

from gauss_bot import (
    FUNC_PATH,
    transparent_invert,
)


class Func:
    """
    Representa una función matemática, con métodos de
    utilidad para validar su nombre y su continuidad.
    """

    def __init__(self, nombre: str, expr: str, variable: Symbol) -> None:
        """
        * TypeError: si nombre no es tiene la forma 'f(x)'
        """

        if not self.validar_nombre(nombre):
            raise ValueError("Nombre inválido! Debe tener la forma 'f(x)'!")
        if str(variable) not in expr:
            raise ValueError("La función no contiene la variable indicada!")

        self.latexified = False
        self.nombre = nombre
        self.variable = variable
        self.func_expr = parse_expr(
            expr,
            transformations=(
                standard_transformations +
                (implicit_multiplication_application,)
            ),
        )

    def __str__(self) -> str:
        return str(self.func_expr)

    def es_continua(self, intervalo: tuple[Fraction, Fraction]) -> bool:
        """
        Valida si una expresión de sympy es continua
        en el intervalo indicado, con respecto al símbolo 'var'.
        """

        a, b = intervalo
        domain: Set = continuous_domain(self.func_expr, self.variable, Reals)
        return domain.contains(
            Interval(
                a,
                b,
                left_open=True,
                right_open=True,
            )
        )

    def latex_to_png(self, font_size: int = 75) -> ctkImage:
        """
        Convierte self.func_expr en formato LaTeX
        y lo convierte en una imagen PNG.
        * output_file: nombre del archivo de salida
        * font_size: tamaño de la fuente en la imagen PNG
        """

        output_file = path.join(FUNC_PATH, f"{self.nombre}.png")
        latex_str = latex(self.func_expr, ln_notation=True)

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
        self.latexified = True

        img = open_img(output_file)
        inverted_img = transparent_invert(img)
        return ctkImage(
            dark_image=inverted_img,
            light_image=img,
            size=(img_length, img_height),
        )

    def get_png(self) -> ctkImage:
        """
        Retorna la imagen PNG de la función si ya habia sido generada.
        """

        if not self.latexified:
            return self.latex_to_png()

        return ctkImage(
            dark_image=open_img(path.join(FUNC_PATH, f"{self.nombre}.png")),
            light_image=open_img(path.join(FUNC_PATH, f"{self.nombre}.png")),
        )

    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """
        Valida que el nombre de la función sea válido.
        """

        pattern = r"^[a-z]\([a-z]\)$"
        return bool(match(pattern, nombre))
