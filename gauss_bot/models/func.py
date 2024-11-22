"""
Implementación de la clase Func.
"""

from decimal import Decimal
from os import (
    makedirs,
    path,
)

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

from ..icons import SAVED_FUNCS_PATH
from ..util_funcs import transparent_invert

TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


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
        * ValueError: si la expresión tiene dominio complejo
        """

        self.nombre = nombre
        self.variable = variable
        self.latexified = latexified
        self.latex_img: Optional[ctkImage] = None

        if "sen" in expr:
            expr = expr.replace("sen", "sin")
        if "^" in expr:
            expr = expr.replace("^", "**")

        self.func_expr: Expr = parse_expr(
            expr,
            transformations=TRANSFORMS,
        )

        if self.func_expr.has(oo, -oo, zoo, nan):
            raise ValueError("La función tiene un dominio complejo!")

    def __str__(self) -> str:
        return str(self.func_expr)

    def get_dominio(self) -> Interval:
        """
        Wrapper para continuous_domain de sympy().
        Retorna un objeto Interval que representa el
        dominio real de self.func_expr.
        """

        return continuous_domain(self.func_expr, self.variable, Reals)

    def es_continua(self, intervalo: tuple[Decimal, Decimal]) -> bool:
        """
        Valida si self.func_expr es continua en el
        intervalo indicado, con respecto a self.variable.
        """

        a, b = intervalo
        return Interval(
            a,
            b,
            left_open=True,
            right_open=True,
        ).is_subset(self.get_dominio())

    def get_png(self) -> ctkImage:
        """
        Retorna la imagen PNG de la función si ya había sido generada.
        Si no, llama a latex_to_png para generarla, y la retorna.
        """

        if not self.latexified or self.latex_img is None:
            self.latex_img  = (
                self.latex_to_png(
                    self.nombre,
                    str(self.func_expr),
                    con_nombre=True,
                )
            )

            self.latexified = True
        return self.latex_img  # type: ignore

    @staticmethod
    def latex_to_png(
        nombre: str,
        func_expr: Optional[str] = None,
        misc_str: Optional[str] = None,
        con_nombre: bool = False,
        font_size: int = 75
    ) -> ctkImage:

        """
        Convierte self.func_expr en formato LaTeX
        y lo convierte en una imagen PNG.
        * output_file: nombre del archivo de salida
        * font_size: tamaño de la fuente en la imagen PNG
        """

        makedirs(SAVED_FUNCS_PATH, exist_ok=True)
        output_file = path.join(SAVED_FUNCS_PATH, f"{nombre}.png")

        if func_expr is not None:
            parse_str = parse_expr(func_expr, transformations=TRANSFORMS)
            latex_str: str = latex(parse_str, ln_notation=True)
        elif misc_str is not None:
            latex_str = misc_str
        else:
            raise ValueError("No se recibió un string a convertir en PNG!")

        if con_nombre:
            latex_str = f"{nombre} = {latex_str}"

        rc("text", usetex=True)
        rc("font", family="serif")

        fig_length = 8 + (len(latex_str) // 8)
        fig_height = (
            2
            if r"\\" not in latex_str
            else
            int(2 + latex_str.count(r"\\") * 2)
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

        img = open_img(output_file)
        inverted_img = transparent_invert(img)
        return ctkImage(
            dark_image=inverted_img,
            light_image=img,
            size=(img_length, img_height),
        )
