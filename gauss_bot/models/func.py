"""
Implementación de la clase Func.
"""

from decimal import Decimal
from logging import (
    WARNING,
    getLogger,
)

from os import (
    makedirs,
    path,
)

from re import compile as comp
from typing import Optional
from customtkinter import CTkImage as ctkImage
from matplotlib import use
from matplotlib.pyplot import (
    axis, close,
    rc, savefig,
    subplots, text,
)

from PIL.Image import open as open_img
from sympy import (
    Reals, oo, zoo, nan,
    Expr, Interval, Symbol,
    diff, integrate,
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

# para que matplotlib sepa que se esta usando tkinter
use("TkAgg")

# para que matplotlib no mande mil mensajes al log
getLogger("matplotlib").setLevel(WARNING)

class Func:
    """
    Representa una función matemática, con métodos de
    utilidad para validar su nombre y su continuidad.
    """

    def __init__(
        self,
        nombre: str,
        expr: str,
        latexified=False,
    ) -> None:

        """
        * ValueError: si la expresión tiene dominio complejo
        """

        self.nombre = nombre
        self.var = Symbol(self.nombre[-2])

        self.latexified = latexified
        self.latex_img: Optional[ctkImage] = None

        if "sen" in expr:
            expr = expr.replace("sen", "sin")
        if "e^" in expr:
            expr = expr.replace("e^", "exp")
        if "^" in expr:
            expr = expr.replace("^", "**")

        expr = expr.replace("x", str(self.var))

        self.expr: Expr = parse_expr(
            expr,
            transformations=TRANSFORMS,
        )

        if self.expr.has(oo, -oo, zoo, nan):
            raise ValueError("La función tiene un dominio complejo!")

    def __str__(self) -> str:
        return str(self.expr)

    def derivar(self) -> "Func":
        """
        Retorna un nuevo objeto Func() que representa la derivada de self.
        """

        if "′" not in self.nombre:
            d_nombre = f"{self.nombre[0]}′{self.nombre[1:]}"

        else:
            num_diff = self.nombre.count("′")
            match num_diff:
                case 1:
                    d_nombre = self.nombre.replace("′", "′′")
                case 2:
                    d_nombre = self.nombre.replace("′′", "′′′")
                case _:
                    d_nombre = self.nombre.replace(
                        "′" * num_diff,
                        f"^({num_diff + 1})",
                    )

        return Func(d_nombre, str(diff(self.expr, self.var)))  # pylint: disable=E0606

    def integrar(self) -> "Func":
        """
        Retorna un nuevo objeto Func() que representa el integral indefinido de self.
        """

        try:
            match = list(comp(r"\^\(-\d+\)").finditer(self.nombre))[-1]
        except IndexError:
            match = None  # type: ignore

        if match is not None:
            num_ints = int(next(x for x in self.nombre if x.isdigit()))
            i_nombre = (
                self.nombre[:match.start()] +
                f"^(-{num_ints + 1})" +
                self.nombre[match.end():]
            )
        else:
            num_ints = 0

        notation = f"^(-{num_ints + 1})"
        i_nombre = f"{self.nombre[0]}{notation}{self.nombre[1:]}"
        return Func(i_nombre, str(integrate(self.expr, self.var)))

    def get_dominio(self) -> Interval:
        """
        Wrapper para continuous_domain de sympy().
        Retorna un objeto Interval que representa el
        dominio real de self.expr.
        """

        return continuous_domain(self.expr, self.var, Reals)

    def es_continua(self, intervalo: tuple[Decimal, Decimal]) -> bool:
        """
        Valida si self.expr es continua en el
        intervalo indicado, con respecto a self.var.
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
            self.latex_img = Func.latex_to_png(
                nombre_expr=(
                    self.nombre
                    if self.nombre.count("′") == 0
                    else None
                ),
                expr=(
                    str(self.expr)
                    if self.nombre.count("′") == 0
                    else None
                ),
                misc_str=(
                    Func.get_derivada_nombre(self) + " = " + str(self.expr)
                    if self.nombre.count("′") > 0
                    else None
                ),
                con_nombre=self.nombre.count("′") == 0,
            )

            self.latexified = True
        return self.latex_img  # type: ignore

    @staticmethod
    def latex_to_png(
        output_file: Optional[str] = None,
        nombre_expr: Optional[str] = None,
        expr: Optional[str] = None,
        misc_str: Optional[str] = None,
        con_nombre: bool = False,
        **kwargs,
    ) -> ctkImage:

        """
        Convierte texto a formato LaTeX para crear una imagen PNG.
        * output_file: nombre del archivo de salida
        * nombre_expr: nombre de la función a mostrar
        * expr: string de la expresión a convertir
        * misc_str: string de texto a convertir
        * con_nombre: si se debe incluir el nombre de la función en la imagen
        * font_size: tamaño de la fuente en la imagen PNG
        """

        makedirs(SAVED_FUNCS_PATH, exist_ok=True)
        output_file = path.join(SAVED_FUNCS_PATH, rf"{output_file or nombre_expr}.png")

        if expr is not None:
            latex_str: str = latex(
                parse_expr(expr, transformations=TRANSFORMS),
                ln_notation=kwargs.pop("ln_notation", True),
            )
        elif misc_str is not None:
            latex_str = misc_str.replace("log", "ln")
        else:
            raise ValueError("No se recibió un string a convertir en PNG!")

        if con_nombre and nombre_expr is not None:
            latex_str = f"{nombre_expr} = {latex_str}"

        rc("text", usetex=True)
        rc("font", family="serif")

        fig_length = 8 + (len(latex_str) // 12)
        fig_height = (
            2
            if r"\\" not in latex_str
            else
            2 + latex_str.count(r"\\") * 2
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
            fontsize=kwargs.pop("font_size", 75),
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

    @staticmethod
    def get_derivada_nombre(derivada: "Func") -> str:
        """
        Formate el nombre de la derivada en la
        notación dy/dx, con respecto a la variable.
        """

        num_diff = derivada.nombre.count("′")
        return (
            f"\\frac{{d{f"^{{{num_diff}}}" if num_diff > 1 else ""}{derivada.nombre[0]}}}" +
            f"{{d{str(derivada.var)}{f"^{{{num_diff}}}" if num_diff > 1 else ""}}}"
        )
