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

from re import (
    compile as comp,
    sub,
)

from typing import Optional
from customtkinter import CTkImage as ctkImage

from matplotlib import use
from matplotlib.backends.backend_agg import FigureCanvasAgg
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

        var_pattern = r"\(([a-z])\)"
        self.var = Symbol(
            comp(var_pattern).findall(nombre)[0]
        )

        self.latexified = latexified
        self.latex_img: Optional[ctkImage] = None

        def replace_var(expr: str) -> str:
            var_str = str(self.var)
            patt = r"\bx\b"

            replaced_expr = expr
            for _ in list(comp(patt).finditer(expr)):
                replaced_expr = sub(
                    patt,
                    var_str,
                    expr,
                )
            return replaced_expr

        if "sen" in expr:
            expr = expr.replace("sen", "sin")
        if "^" in expr:
            expr = expr.replace("^", "**")

        expr = replace_var(
            str(parse_expr(expr, transformations=TRANSFORMS))
        )

        if "e**" in expr:
            expr = expr.replace("e**", "exp")

        self.expr: Expr = parse_expr(
            expr,
            transformations=TRANSFORMS,
        )

        if self.expr.has(oo, -oo, zoo, nan):
            raise ValueError("La función tiene un dominio complejo!")

    def __str__(self) -> str:
        return f"{self.nombre} = {self.expr}"

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

    def derivar(self) -> "Func":
        """
        Retorna un nuevo objeto Func() que representa la derivada de self.
        """

        if "′" not in self.nombre:
            d_nombre = f"{self.nombre[0]}′{self.nombre[1:]}"

        else:
            num_diff = self.nombre.count("′")
            d_nombre = self.nombre.replace(
                "".join("′" for _ in range(num_diff)),
                "".join("′" for _ in range(num_diff + 1)),
            )

        return Func(d_nombre, str(diff(self.expr, self.var)))  # pylint: disable=E0606

    def integrar(self) -> "Func":
        """
        Retorna un nuevo objeto Func() que
        representa el integral indefinido de self.
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
            i_nombre = rf"{self.nombre[0]}^{"(-1)"}{self.nombre[1:]}"

        return Func(i_nombre, str(integrate(self.expr, self.var)))

    def get_dominio(self) -> Interval:
        """
        Wrapper para continuous_domain de sympy().
        Retorna un objeto Interval que representa el
        dominio real de self.expr.
        """

        return continuous_domain(self.expr, self.var, Reals)

    def get_di_nombre(self, diffr: bool = False, integ: bool = False) -> str:
        """
        Llama las funciones get_derivada_nombre() o get_integral_nombre().
        """

        num_diff = self.nombre.count("′")
        num_integ = int(
            next(
                (x for x in self.nombre if x.isdigit()),
                0,
            )
        )

        if num_diff != 0 or diffr:
            return self.get_derivada_nombre(num_diff)
        if num_integ != 0 or integ:
            return self.get_integral_nombre(num_integ)
        raise NameError("No se pudo determinar el tipo de función!")

    def get_derivada_nombre(self, num_diff: int) -> str:
        """
        Formate el nombre de la derivada en la
        notación dy/dx, con respecto a la variable.
        """

        return (
            f"\\frac{{d{f"^{{{num_diff}}}" if num_diff > 1 else ""}{self.nombre[0]}}}" +
            f"{{d{str(self.var)}{f"^{{{num_diff}}}" if num_diff > 1 else ""}}}"
        )

    def get_integral_nombre(self, num_integ: int) -> str:
        """
        Formate el nombre de la integral con la
        notación ∫ f(x) dx, con respecto a la variable.
        """

        return (
            rf"{r"".join(r"\int" for _ in range(num_integ))}" +
            rf"{self.nombre[0] + rf"({self.var})"}d{str(self.var)}"
        )

    def get_png(self) -> ctkImage:
        """
        Retorna la imagen PNG de la función si ya había sido generada.
        Si no, llama a latex_to_png() para generarla, y la retorna.
        """

        if not self.latexified or self.latex_img is None:
            self.latex_img = Func.latex_to_png(
                nombre_expr=(
                    self.nombre
                    if (
                        self.nombre.count("′") == 0
                        and
                        self.nombre.count("∫") == 0
                    )
                    else self.get_di_nombre()
                ),
                expr=str(self.expr),
                con_nombre=True,
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

        - kwargs:
            - ln_notation: si se debe usar ln en lugar de log
            - font_size: tamaño de la fuente en la imagen
        """

        makedirs(SAVED_FUNCS_PATH, exist_ok=True)
        output_file = path.join(
            SAVED_FUNCS_PATH,
            rf"{output_file or nombre_expr}.png",
        )

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

        temp_fig, temp_ax = subplots()
        temp_text = temp_ax.text(
            0.5,
            0.5,
            f"${latex_str}$",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=kwargs.get("font_size", 75),
            transform=temp_ax.transAxes
        )

        temp_canvas = FigureCanvasAgg(temp_fig)
        temp_canvas.draw()

        bbox = temp_text.get_window_extent(renderer=temp_canvas.get_renderer())
        width, height = (
            (bbox.width / temp_fig.dpi) + 2,
            (bbox.height / temp_fig.dpi) + 1,
        )

        close(temp_fig)

        fig, _ = subplots(figsize=(width, height))
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
            dpi=200,
            pad_inches=0.1,
        )

        close(fig)

        img = open_img(output_file)
        inverted_img = transparent_invert(img)
        return ctkImage(
            dark_image=inverted_img,
            light_image=img,
            size=(int(width * 20), int(height * 20)),
        )
