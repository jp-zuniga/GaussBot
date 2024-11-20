"""
Implementación de RaicesFrame,
un frame que permite encontrar
las raíces de funciones matemáticas.
"""

# from fractions import Fraction
from random import randint
from typing import TYPE_CHECKING

from tkinter import Variable
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    # CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

# from gauss_bot import delete_msg_frame
# from gauss_bot.models import Func
from gauss_bot.managers import (
    MARGEN_ERROR,
    MAX_ITERACIONES,
    FuncManager,
)

from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    # place_msg_frame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import AnalisisFrame


class RaicesFrame(CustomScrollFrame):
    """
    Frame que permite encontrar las raíces de una función.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "AnalisisFrame",
        func_manager: FuncManager,
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.metodo_frame = ctkFrame(self, fg_color="transparent")
        self.datos_frame = ctkFrame(self, fg_color="transparent")
        self.resultado = ctkFrame(self, fg_color="transparent")
        self.metodo_frame.columnconfigure(0, weight=1)
        self.datos_frame.columnconfigure(0, weight=1)
        self.datos_frame.columnconfigure(3, weight=1)
        self.resultado.columnconfigure(0, weight=1)

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.metodos: dict[str, int] = {
            "Método de Bisección": 0,
            "Método de Falsa Posición": 1,
            "Método de Newton": 2,
            "Método de la Secante": 3,
        }

        self.metodo_actual: int = -1
        self.a_entry: CustomEntry
        self.b_entry: CustomEntry
        self.xi_entry: CustomEntry
        self.xu_entry: CustomEntry
        self.error_entry: CustomEntry
        self.iteraciones_entry: CustomEntry

        self.func_select = CustomDropdown(
            self,
            variable=Variable(
                value="Seleccione una función para encontrar sus raíces:",
            ), values=self.nombres_funcs,
            command=self.mostrar_func,
        )

        self.func_select.grid(row=0, column=0, pady=5, sticky="n")

    def mostrar_func(self, nombre_func: str) -> None:
        """
        Muestra la función seleccionada en el dropdown,
        y crea un dropdown para seleccionar el método a utilizar.
        """

        self.metodo_frame.grid(row=1, column=0, pady=5, sticky="n")
        func_seleccionada = self.func_manager.funcs_ingresadas[nombre_func]

        for widget in self.metodo_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        ctkLabel(
            self.metodo_frame,
            text="",
            image=func_seleccionada.get_png(),
        ).grid(row=0, column=0, pady=5, sticky="n")

        CustomDropdown(
            self.metodo_frame,
            variable=Variable(value="Seleccione un método para encontrar las raíces:"),
            values=list(self.metodos.keys()),
            command=self.mostrar_datos,
        ).grid(row=1, column=0, pady=5, sticky="n")

    def mostrar_datos(self, metodo: str) -> None:
        """
        Muestra los campos necesarios para ingresar los datos
        requeridos por el método seleccionado.
        """

        self.datos_frame.grid(row=2, column=0, pady=5, sticky="n")
        for widget in self.resultado.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        if self.metodo_actual == self.metodos[metodo]:
            return

        if (
            self.metodo_actual == 0 and self.metodos[metodo] == 1
            or
            self.metodo_actual == 1 and self.metodos[metodo] == 0
        ):
            self.limpiar_inputs()
            return

        for widget in self.datos_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        self.metodo_actual = self.metodos[metodo]
        match self.metodo_actual:
            case 0:
                self.setup_cerrado()
            case 1:
                self.setup_cerrado()
            case 2:
                self.setup_abierto(newton=True)
            case 3:
                self.setup_abierto(newton=False)
            case _:
                raise ValueError("Argumento inválido para 'metodo'!")

    def setup_cerrado(self) -> None:
        """
        Configura self.datos_frame para aceptar input
        de intervalo y margen de error para métodos cerrados.
        """

        ctkLabel(
            self.datos_frame,
            text="Intervalo:",
        ).grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ne")

        self.a_entry = CustomEntry(
            self.datos_frame,
            width=60,
            placeholder_text=str(randint(-10, -1))
        )

        self.a_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="ne")
        ctkLabel(
            self.datos_frame,
            text=",",
            font=("Roboto", 18),
        ).grid(row=0, column=2, padx=2, pady=(5, 2), sticky="nw")

        self.b_entry = CustomEntry(
            self.datos_frame,
            width=60,
            placeholder_text=str(randint(1, 10))
        )

        self.b_entry.grid(row=0, column=3, padx=5, pady=(5, 2), sticky="nw")
        ctkLabel(
            self.datos_frame,
            text="Margen de error:",
        ).grid(row=1, column=0, padx=5, pady=(2, 5), sticky="ne")

        self.error_entry = CustomEntry(self.datos_frame)
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")
        self.error_entry.grid(
            row=1, column=1,
            columnspan=3,
            padx=5, pady=(2, 5),
            sticky="nw",
        )

        ctkButton(
            self.datos_frame,
            height=30,
            text="Encontrar raíz",
            command=self.leer_datos
        ).grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def setup_abierto(self, newton: bool) -> None:
        """
        Configura self.datos_frame para aceptar input
        de valor inicial, margen de error y máximo de iteraciones
        para el método de Newton.
        """

        ctkLabel(
            self.datos_frame,
            text="Valor inicial:"
                 if newton
                 else
                 "Valores iniciales:",
        ).grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ne")

        xi_width = 140 if newton else 60
        self.xi_entry = CustomEntry(
            self.datos_frame,
            width=xi_width,
            placeholder_text=str(randint(-10, 10))
        )

        if not newton:
            self.xu_entry = CustomEntry(
                self.datos_frame,
                width=60,
                placeholder_text=str(randint(-10, 10))
            )

            self.xi_entry.grid(row=0, column=1, padx=5, pady=(5, 2), sticky="nw")
            ctkLabel(
                self.datos_frame,
                text=",",
                font=("Roboto", 18),
            ).grid(row=0, column=2, padx=2, pady=(5, 2), sticky="nw")

            self.xu_entry.grid(
                row=0, column=3,
                padx=5, pady=(5, 2),
                sticky="nw",
            )
        else:
            self.xi_entry.grid(
                row=0, column=1,
                columnspan=3,
                padx=5, pady=(5, 2),
                sticky="nw",
            )

        ctkLabel(
            self.datos_frame,
            text="Margen de error:",
        ).grid(row=2, column=0, padx=5, pady=2, sticky="ne")

        self.error_entry = CustomEntry(self.datos_frame)
        self.error_entry.insert(0, f"{float(MARGEN_ERROR):.6f}")
        self.error_entry.grid(
            row=2, column=1,
            columnspan=3,
            padx=5, pady=2,
            sticky="nw",
        )

        ctkLabel(
            self.datos_frame,
            text="Máximo de iteraciones:",
        ).grid(row=3, column=0, padx=5, pady=(2, 5), sticky="ne")

        self.iteraciones_entry = CustomEntry(self.datos_frame)
        self.iteraciones_entry.insert(0, MAX_ITERACIONES)
        self.iteraciones_entry.grid(
            row=3, column=1,
            columnspan=3,
            padx=5, pady=(2, 5),
            sticky="nw",
        )

        ctkButton(
            self.datos_frame,
            height=30,
            text="Encontrar raíz",
            command=self.leer_datos
        ).grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="n")

    def leer_datos(self) -> None:
        """
        Lee y valida los datos ingresados por el usuario
        en las widgets de self.datos_frame.
        """

    def limpiar_inputs(self) -> None:
        """
        Limpia el texto de todos los entries
        de datos en self.datos_frame.
        """

        for widget in self.datos_frame.winfo_children():
            if (
                isinstance(widget, CustomEntry) and
                widget.get() != "" and
                widget.get() != f"{float(MARGEN_ERROR):.6f}"
            ):
                widget.delete(0, "end")

    def update_frame(self):
        """
        Configura todos los backgrounds de los widgets
        por si hubo un cambio de modo de apariencia.
        """

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.func_select.configure(values=self.nombres_funcs)

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore
            if isinstance(widget, ctkFrame):
                for subwidget in widget.winfo_children():  # type: ignore
                    subwidget.configure(bg_color="transparent")  # type: ignore
