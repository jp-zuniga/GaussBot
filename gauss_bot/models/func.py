"""
Implementación de la clase Func.
"""

from fractions import Fraction
from os import (
    makedirs,
    path,
)

from re import match
from typing import Optional

from customtkinter import CTkImage as ctkImage
from matplotlib.pyplot import (
    axis, close,
    rc, savefig,
    subplots, text,
)

from PIL.Image import open as open_img
from sympy import (
    Reals, oo, zoo, nan,
    Expr, Interval, Symbol,
    latex, parse_expr,
)

from sympy.calculus.util import continuous_domain
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
)

from gauss_bot import (
    SAVED_FUNC_PATH,
    transparent_invert,
)


class Func:
    """
    Representa una función matemática, con métodos de
    utilidad para validar su nombre y su continuidad.
    """

    def __init__(
        self,
        nombre: str,
        expr: str,
        variable: Symbol = Symbol("x"),
        latexified=False,
    ) -> None:

        """
        * ValueError: si nombre no es tiene la forma 'f(x)'
        """

        if not self.validar_nombre(nombre):
            if "x" not in nombre:
                error = "La función debe estar en términos de x!"
            else:
                error = "Nombre inválido! Debe tener la forma 'f(x)' !"
            raise ValueError(error)
        if str(variable) not in expr:
            raise ValueError("La función no contiene la variable indicada!")

        self.latexified = latexified
        self.latex_img: Optional[ctkImage] = None

        self.nombre = nombre
        self.variable = variable

        if "sen" in expr:
            expr = expr.replace("sen", "sin")
        if "^" in expr:
            expr = expr.replace("^", "**")

        self.func_expr: Expr = parse_expr(
            expr,
            transformations=(
                standard_transformations +
                (implicit_multiplication_application,)
            ),
        )

        if self.func_expr.has(oo, -oo, zoo, nan):
            raise ValueError("La función tiene un dominio complejo!")

    def __str__(self) -> str:
        return str(self.func_expr)

    def es_continua(self, intervalo: tuple[Fraction, Fraction]) -> bool:
        """
        Valida si self.func_expr es continua en el
        intervalo indicado, con respecto a self.variable.
        """

        a, b = intervalo
        domain: Interval = continuous_domain(self.func_expr, self.variable, Reals)
        return Interval(
            a,
            b,
            left_open=True,
            right_open=True,
        ).is_subset(domain)

    def latex_to_png(self, font_size: int = 75) -> ctkImage:
        """
        Convierte self.func_expr en formato LaTeX
        y lo convierte en una imagen PNG.
        * output_file: nombre del archivo de salida
        * font_size: tamaño de la fuente en la imagen PNG
        """

        makedirs(SAVED_FUNC_PATH, exist_ok=True)
        output_file = path.join(SAVED_FUNC_PATH, f"{self.nombre}.png")

        latex_str: str = latex(self.func_expr, ln_notation=True)
        latex_str = f"{self.nombre} = {latex_str}"

        rc("text", usetex=True)
        rc("font", family="serif")

        fig_length = 12 + (len(latex_str) // 8)
        fig_height = (
            2
            if r"\\" not in latex_str
            else
            int(2 + latex_str.count(r"\\") // 2)
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
            pad_inches=0.05,
            dpi=200,
        )

        close(fig)
        self.latexified = True

        img = open_img(output_file)
        inverted_img = transparent_invert(img)
        self.latex_img = ctkImage(
            dark_image=inverted_img,
            light_image=img,
            size=(img_length, img_height),
        )

        return self.latex_img

    def get_png(self) -> ctkImage:
        """
        Retorna la imagen PNG de la función si ya había sido generada.
        Si no, llama a latex_to_png para generarla, y la retorna.
        """

        if not self.latexified or self.latex_img is None:
            return self.latex_to_png()
        return self.latex_img  # type: ignore

    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """
        Valida que el nombre de la función sea válido.
        """

        pattern = r"^[a-z]\([x]\)$"
        return bool(match(pattern, nombre))
