# pylint: disable=too-many-lines

"""
Implementación de todos los frames
de operaciones con vectores.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from random import choice
from tkinter import Variable
from typing import TYPE_CHECKING, Optional

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkTabview as ctkTabview,
)

from ...custom import CustomDropdown, CustomEntry, CustomScrollFrame, IconButton
from ....managers import VectoresManager
from ....models import Vector
from ....utils import (
    ENTER_ICON,
    INFO_ICON,
    INPUTS_ICON,
    delete_msg_frame,
    delete_msg_if,
    format_factor,
    generate_range,
    get_dict_key,
    place_msg_frame,
    toggle_proc,
)

if TYPE_CHECKING:
    from .. import VectoresFrame
    from ... import GaussUI

getcontext().prec = 8


class MagnitudTab(CustomScrollFrame):
    """
    Frame para calcular la magnitud de un vector ingresado por el usuario.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager,
    ) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.msg_frame: Optional[ctkFrame] = None
        self.proc_label: Optional[ctkLabel] = None
        self.proc_hidden = True

        # crear widgets
        instruct_m = ctkLabel(
            self, text="Seleccione un vector del para calcular su magnitud:"
        )

        self.select_vec = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=Variable(value=self.master_frame.nombres_vectores[0]),
            command=self.update_vec,
        )

        self.vec = self.select_vec.get()
        calcular_button = ctkButton(
            self, height=30, text="Calcular", command=self.calcular_magnitud
        )

        self.resultado_frame = ctkFrame(self, fg_color="transparent")

        # colocar widgets
        instruct_m.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vec.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        calcular_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def calcular_magnitud(self) -> None:
        """
        Calcula la magnitud del vector seleccionado.
        """

        for widget in self.resultado_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        self.resultado_frame.grid(
            row=2, column=0, columnspan=3, padx=5, pady=5, sticky="n"
        )

        delete_msg_frame(self.msg_frame)
        self.update_vec(self.select_vec.get())
        vec = self.vecs_manager.vecs_ingresados[self.vec]

        header = f"||  {self.vec}  ||"
        resultado = Decimal(float(vec.magnitud())).normalize()

        proc = "---------------------------------------------\n"
        proc += f"{self.vec}:\n{vec}\n"
        proc += "---------------------------------------------\n"
        proc += "Para calcular la magnitud de un vector,\n"
        proc += "se debe encontrar la raíz cuadrada de\n"
        proc += "la suma de los cuadrados de sus componentes.\n\n"

        proc += f"[ {
            ' + '.join(
                f'{format_factor(c, mult=False, parenth_negs=True, skip_ones=False)}^2'
                for c in vec.componentes
            )
        } ]\n"

        proc += f"=\n[ {' + '.join(str(c**2) for c in vec.componentes)} ]\n"

        sum_squares = sum(c**2 for c in vec.componentes)
        proc += f"=\n{sum_squares}\n\n"
        proc += f"||  {self.vec}  ||  =  √( {sum_squares} )\n"
        proc += "---------------------------------------------\n"
        proc += f"||  {self.vec}  ||  =  {resultado}\n"

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_frame,
            msg_frame=self.msg_frame,
            msg=f"{header}  =  {resultado}",
            tipo="resultado",
        )

        ctkButton(
            self.resultado_frame,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento para calcular la "
                + f"magnitud del vector {self.vec}",
                proc_label=self.proc_label,
                label_txt=proc,  # pylint: disable=E0606
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualiza los backgrounds y los datos del frame.
        """

        self.select_vec.configure(
            values=self.master_frame.nombres_vectores,
            variable=Variable(value=self.master_frame.nombres_vectores[0]),
        )

        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore

    def update_vec(self, valor: str) -> None:
        """
        Actualiza el valor de self.vec con el valor seleccionado en el dropdown.
        """

        self.vec = valor


class SumaRestaTab(CustomScrollFrame):
    """
    Frame para sumar y restar vectores ingresados por el usuario.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager,
    ) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.msg_frame: Optional[ctkFrame] = None

        # para el boton de ejecutar y el dropdown de operadores
        self.operaciones: dict[str, str] = {"Sumar": "+", "Restar": "−"}

        # definir atributos, se inicializan en setup_frame()
        self.instruct_sr: ctkLabel
        self.select_operacion: CustomDropdown
        self.select_1: CustomDropdown
        self.select_2: CustomDropdown
        self.ejecutar_button: ctkButton
        self.resultado_frame: ctkFrame

        self.operacion = "Sumar"
        self.vec1 = ""
        self.vec2 = ""

        self.proc_label: Optional[ctkLabel] = None
        self.proc_hidden = True

        self.setup_frame()

    def setup_frame(self, default: str = "Sumar") -> None:
        """
        Inicializa y configura las widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        # crear widgets
        self.instruct_sr = ctkLabel(
            self, text=f"Seleccione los vectores a {default.lower()}:"
        )

        self.select_operacion = CustomDropdown(
            self,
            width=40,
            font=ctkFont(size=16),
            values=list(self.operaciones.values()),
            variable=Variable(value=self.operaciones[default]),
            command=self.update_operacion,
        )

        self.select_1 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder1,
            command=self.update_vec1,
        )

        self.select_2 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_vec2,
        )

        self.vec1 = self.select_1.get()
        self.vec2 = self.select_2.get()
        self.ejecutar_button = ctkButton(
            self, height=30, text=default, command=self.ejecutar_operacion
        )

        self.resultado_frame = ctkFrame(self, fg_color="transparent")

        # colocar widgets
        self.instruct_sr.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.select_operacion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_2.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.ejecutar_button.grid(
            row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n"
        )

    def ejecutar_operacion(self) -> None:
        """
        Suma o resta las matrices seleccionadas.
        """

        for widget in self.resultado_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        self.update_operacion(self.select_operacion.get())
        self.update_vec1(self.select_1.get())
        self.update_vec2(self.select_2.get())
        self.resultado_frame.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n"
        )

        delete_msg_frame(self.msg_frame)
        try:
            if self.operacion == "+":
                proc, header, resultado = self.vecs_manager.suma_resta_vecs(
                    True, self.vec1, self.vec2
                )
            elif self.operacion == "−":
                proc, header, resultado = self.vecs_manager.suma_resta_vecs(
                    False, self.vec1, self.vec2
                )
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado_frame,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )

            return
        delete_msg_frame(self.msg_frame)

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_frame,
            msg_frame=self.msg_frame,
            msg=f"\n{header}:\n{str(resultado)}\n",  # pylint: disable=E0606
            tipo="resultado",
        )

        ctkButton(
            self.resultado_frame,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title=f"GaussBot: Procedimiento de {header}",
                proc_label=self.proc_label,
                label_txt=proc,  # pylint: disable=E0606
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualiza los backgrounds y los datos del frame.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        self.select_1.configure(
            variable=placeholder1, values=self.master_frame.nombres_vectores
        )

        self.select_2.configure(
            variable=placeholder2, values=self.master_frame.nombres_vectores
        )

    def update_operacion(self, valor: str) -> None:
        """
        Cambia el texto del botón de ejecutar operación
        y el texto de la instrucción según la opción
        seleccionada en el dropdown.
        """

        self.operacion = valor
        op_text: str = get_dict_key(self.operaciones, valor)  # type: ignore

        self.ejecutar_button.configure(text=op_text)
        self.instruct_sr.configure(text=f"Seleccione los vectores a {op_text.lower()}:")

    def update_vec1(self, valor: str) -> None:
        """
        Actualiza el valor de self.vec1 con el
        valor seleccionado en el dropdown correspondiente.
        """

        self.vec1 = valor

    def update_vec2(self, valor: str) -> None:
        """
        Actualiza el valor de self.vec2 con el
        valor seleccionado en el dropdown correspondiente.
        """

        self.vec2 = valor


class MultiplicacionTab(CustomScrollFrame):
    """
    Frame para realizar multiplicaciones de vectores por escalares,
    producto punto y producto matriz-vector.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager,
    ) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        # definir atributos, se inicializan en setup_tabs()
        self.msg_frame: Optional[ctkFrame] = None
        self.select_escalar_vec: CustomDropdown
        self.escalar_entry: CustomEntry
        self.dimensiones_entry: CustomEntry
        self.select_vec1: CustomDropdown
        self.select_vec2: CustomDropdown
        self.select_vmat: CustomDropdown
        self.select_mvec: CustomDropdown

        self.escalar_vec = ""
        self.vec1 = ""
        self.vec2 = ""
        self.vmat = ""
        self.mvec = ""

        self.proc_label: Optional[ctkLabel] = None
        self.proc_hidden = True

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        # crear tabs
        self.tab_escalar = self.tabview.add("Escalar por Vector")
        self.tab_prod_punto = self.tabview.add("Producto Punto")
        self.tab_prod_cruz = self.tabview.add("Producto Cruz")
        self.tab_mat_vec = self.tabview.add("Producto Matriz-Vector")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        """
        Wrapper para llamar todos los métodos de configuración de tabs.
        Se encarga de validar si hay matrices para que los setups
        individuales no lo tengan que hacer.
        """

        for tab in self.tabview.winfo_children():
            tab.columnconfigure(0, weight=1)  # type: ignore
            tab.columnconfigure(2, weight=1)  # type: ignore

        # crear frames de resultado
        self.resultado_escalar = ctkFrame(self.tab_escalar, fg_color="transparent")
        self.resultado_punto = ctkFrame(self.tab_prod_punto, fg_color="transparent")
        self.resultado_cruz = ctkFrame(self.tab_prod_cruz, fg_color="transparent")
        self.resultado_mat_vec = ctkFrame(self.tab_mat_vec, fg_color="transparent")

        self.setup_escalar_tab()
        self.setup_prod_punto_tab()
        self.setup_prod_cruz_tab()

        if len(self.master_frame.nombres_matrices) >= 1:
            self.setup_mat_vec_tab()
        else:
            self.msg_frame = place_msg_frame(
                parent_frame=self.tab_mat_vec,
                msg_frame=self.msg_frame,
                msg="No hay matrices guardadas!",
                tipo="error",
                columnspan=3,
            )

            ctkButton(
                self.tab_mat_vec,
                height=30,
                text="Agregar matrices",
                image=INPUTS_ICON,
                command=lambda: self.app.home_frame.ir_a_mats(mostrar=False),  # type: ignore
            ).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_escalar_tab(self) -> None:
        """
        Setup de la tab para multiplicar un vector por un escalar.
        """

        delete_msg_frame(self.msg_frame)

        # crear widgets
        operador_label = ctkLabel(self.tab_escalar, text="•", font=ctkFont(size=16))
        instruct_e = ctkLabel(
            self.tab_escalar, text="Seleccione el vector e ingrese el escalar:"
        )

        self.select_escalar_vec = CustomDropdown(
            self.tab_escalar,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=Variable(value=self.master_frame.nombres_vectores[0]),
            command=self.update_escalar_vec,
        )

        self.escalar_vec = self.select_escalar_vec.get()
        self.escalar_entry = CustomEntry(
            self.tab_escalar,
            width=60,
            placeholder_text=str(choice(generate_range(-10, 10))),
        )

        self.escalar_entry.bind("<Return>", lambda _: self.mult_por_escalar())

        multiplicar_button = ctkButton(
            self.tab_escalar,
            height=30,
            text="Multiplicar",
            command=self.mult_por_escalar,
        )

        # colocar widgets
        instruct_e.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.escalar_entry.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_escalar_vec.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        multiplicar_button.grid(
            row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n"
        )

    def setup_prod_punto_tab(self) -> None:
        """
        Setup de la tab para calcular el producto punto de dos vectores.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        # crear widgets
        operador_label = ctkLabel(self.tab_prod_punto, text=".", font=ctkFont(size=26))

        instruct_v = ctkLabel(
            self.tab_prod_punto, text="Seleccione los vectores a multiplicar:"
        )

        self.select_vec1 = CustomDropdown(
            self.tab_prod_punto,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder1,
            command=self.update_vec1,
        )

        self.select_vec2 = CustomDropdown(
            self.tab_prod_punto,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_vec2,
        )

        self.vec1 = self.select_vec1.get()
        self.vec2 = self.select_vec2.get()
        multiplicar_button = ctkButton(
            self.tab_prod_punto, height=30, text="Multiplicar", command=self.prod_punto
        )

        # colocar widgets
        instruct_v.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vec1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_vec2.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        multiplicar_button.grid(
            row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n"
        )

    def setup_prod_cruz_tab(self) -> None:
        """
        Setup de la tab para multiplicar vectores.
        """

        delete_msg_frame(self.msg_frame)

        ctkLabel(self.tab_prod_cruz, text="Ingrese las dimensiones:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.dimensiones_entry = CustomEntry(
            self.tab_prod_cruz, placeholder_text="3", width=40
        )

        self.dimensiones_entry.bind(
            "<Return>", lambda _: setup_selections(self.dimensiones_entry.get())
        )

        self.dimensiones_entry.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        IconButton(
            self.tab_prod_cruz,
            app=self.app,
            image=ENTER_ICON,
            tooltip_text="Ingresar dimensiones",
            command=lambda: setup_selections(self.dimensiones_entry.get()),
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        def setup_selections(input_dims: str) -> None:
            delete_msg_frame(self.msg_frame)
            for widget in self.tab_prod_cruz.winfo_children():  # type: ignore
                if (
                    widget is not self.resultado_cruz
                    and dict(widget.grid_info()).get("row", -1) > 0  # type: ignore
                ):
                    widget.destroy()  # type: ignore

            try:
                dimensiones = int(input_dims)
                if dimensiones <= 1:
                    raise ValueError
                if dimensiones - 1 > len(self.master_frame.nombres_vectores):
                    raise ValueError(
                        f"No hay suficientes vectores en R{dimensiones} "
                        + "para calcular un producto cruz!"
                    )
            except ValueError as e:
                str_e = str(e)
                if "!" not in str_e:
                    msg = "Debe ingresar un número entero mayor a 1!"
                else:
                    msg = str_e

                self.msg_frame = place_msg_frame(
                    parent_frame=self.tab_prod_cruz,
                    msg_frame=self.msg_frame,
                    msg=msg,
                    tipo="error",
                    row=1,
                    columnspan=3,
                )

                return

            dropdowns: list[CustomDropdown] = []
            vecs_validos = [
                get_dict_key(self.vecs_manager.vecs_ingresados, vec)
                for vec in self.vecs_manager.vecs_ingresados.values()
                if len(vec) == dimensiones
            ]

            if not vecs_validos:
                self.msg_frame = place_msg_frame(
                    parent_frame=self.tab_prod_cruz,
                    msg_frame=self.msg_frame,
                    msg=f"No hay vectores en R{dimensiones} guardados!",
                    tipo="error",
                    row=1,
                    columnspan=3,
                )

                return

            IconButton(
                self.tab_prod_cruz,
                app=self.app,
                image=INFO_ICON,
                tooltip_text="Solamente se están mostrando "
                + f"los vectores guardados en R{dimensiones}.",
            ).grid(row=1, column=0, columnspan=3, padx=5, pady=(15, 3), sticky="n")

            ctkLabel(
                self.tab_prod_cruz, text="Seleccione los vectores a multiplicar:"
            ).grid(row=2, column=0, columnspan=3, padx=5, pady=3, sticky="n")

            range_dims = dimensiones if dimensiones == 2 else dimensiones - 1
            for i in range(range_dims):
                dropdowns.append(
                    CustomDropdown(
                        self.tab_prod_cruz,
                        width=60,
                        values=vecs_validos,
                        variable=Variable(value=vecs_validos[i]),
                    )
                )

                dropdowns[i].grid(
                    row=i + 3, column=0, columnspan=3, padx=5, pady=5, sticky="n"
                )

            ctkButton(
                self.tab_prod_cruz,
                height=30,
                text="Multiplicar",
                command=lambda: self.prod_cruz(dropdowns),
            ).grid(
                row=dimensiones + 3, column=0, columnspan=3, padx=5, pady=10, sticky="n"
            )

    def setup_mat_vec_tab(self) -> None:
        """
        Setup de la tab para multiplicar matrices y vectores.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(value=self.master_frame.nombres_vectores[0])

        # crear widgets
        operador_label = ctkLabel(self.tab_mat_vec, text="•", font=ctkFont(size=16))
        instruct_mv = ctkLabel(
            self.tab_mat_vec, text="Seleccione la matriz y el vector a multiplicar:"
        )

        self.select_vmat = CustomDropdown(
            self.tab_mat_vec,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_vmat,
        )

        self.select_mvec = CustomDropdown(
            self.tab_mat_vec,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_mvec,
        )

        self.vmat = self.select_vmat.get()
        self.mvec = self.select_mvec.get()
        multiplicar_button = ctkButton(
            self.tab_mat_vec, height=30, text="Multiplicar", command=self.mult_mat_vec
        )

        # colocar widgets
        instruct_mv.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vmat.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mvec.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        multiplicar_button.grid(
            row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n"
        )

    def mult_por_escalar(self) -> None:
        """
        Realiza la multiplicación de un vector por un escalar.
        """

        for widget in self.resultado_escalar.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        self.update_escalar_vec(self.select_escalar_vec.get())
        self.resultado_escalar.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n"
        )

        delete_msg_if(self.msg_frame, (self.tab_escalar, self.resultado_escalar))
        try:
            escalar = Fraction(self.escalar_entry.get())  # type: ignore
            proc, header, resultado = self.vecs_manager.escalar_por_vec(
                escalar, self.escalar_vec
            )
        except (ValueError, ZeroDivisionError) as e:
            if isinstance(e, ValueError):
                msg = "El escalar debe ser un número racional!"
            else:
                msg = "El denominador no puede ser 0!"

            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado_escalar,
                msg_frame=self.msg_frame,
                msg=msg,
                tipo="error",
            )

            return
        delete_msg_if(self.msg_frame, (self.tab_escalar, self.resultado_escalar))

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_escalar,
            msg_frame=self.msg_frame,
            msg=f"\n{header}:\n{str(resultado)}\n",  # pylint: disable=E0606
            tipo="resultado",
        )

        ctkButton(
            self.resultado_escalar,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento de la "
                + f"multiplicación {header}",
                proc_label=self.proc_label,
                label_txt=proc,  # pylint: disable=E0606
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def prod_punto(self) -> None:
        """
        Realiza el producto punto de dos vectores.
        """

        for widget in self.resultado_punto.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        self.update_vec1(self.select_vec1.get())
        self.update_vec2(self.select_vec2.get())
        self.resultado_punto.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n"
        )

        delete_msg_if(self.msg_frame, (self.tab_prod_punto, self.resultado_punto))
        try:
            proc, header, resultado = self.vecs_manager.producto_punto(
                self.vec1, self.vec2
            )
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado_punto,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )
            return
        delete_msg_if(self.msg_frame, (self.tab_prod_punto, self.resultado_punto))

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_punto,
            msg_frame=self.msg_frame,
            msg=f"{header}:\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
            ipadx=5,
            ipady=5,
        )

        ctkButton(
            self.resultado_punto,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento de la "
                + f"multiplicación {header}",
                proc_label=self.proc_label,
                label_txt=proc,  # pylint: disable=E0606
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def prod_cruz(self, dropdowns: list[CustomDropdown]) -> None:
        """
        Realiza el producto cruz de dos vectores.
        """

        delete_msg_frame(self.msg_frame)
        vectores = [
            self.vecs_manager.vecs_ingresados[dropdown.get()] for dropdown in dropdowns
        ]

        self.resultado_cruz.grid(
            row=len(vectores) + 5, column=0, columnspan=3, padx=5, pady=5, sticky="n"
        )

        header = " × ".join([dropdown.get() for dropdown in dropdowns])
        resultado = Vector.prod_cruz(len(vectores[0]), vectores)

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_cruz,
            msg_frame=self.msg_frame,
            msg=f"\n{header}:\n{str(resultado)}\n",
            tipo="resultado",
        )

    def mult_mat_vec(self) -> None:
        """
        Realiza el producto de una matriz por un vector.
        """

        self.update_vmat(self.select_vmat.get())
        self.update_mvec(self.select_mvec.get())
        self.resultado_mat_vec.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n"
        )

        delete_msg_if(self.msg_frame, (self.tab_mat_vec, self.resultado_mat_vec))
        try:
            proc, header, resultado = self.app.ops_manager.mat_por_vec(
                self.vmat, self.mvec
            )
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado_mat_vec,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )
            return
        delete_msg_if(self.msg_frame, (self.tab_mat_vec, self.resultado_mat_vec))

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_mat_vec,
            msg_frame=self.msg_frame,
            msg=f"\n{header}:\n{str(resultado)}\n",  # pylint: disable=E0606
            tipo="resultado",
        )

        ctkButton(
            self.resultado_mat_vec,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento de la "
                + f"multiplicación {header}",
                proc_label=self.proc_label,
                label_txt=proc,  # pylint: disable=E0606
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Destruye todas las widgets en todas las tabs,
        y vuelve a correr el setup.
        """

        for tab in self.tabview.winfo_children():
            for widget in tab.winfo_children():
                widget.destroy()

        self.setup_tabs()
        self.tabview.configure(bg_color="transparent")
        self.tabview.configure(fg_color="transparent")

    def update_escalar_vec(self, valor: str) -> None:
        """
        Actualiza el valor de self.escalar_vec con
        el valor seleccionado en el dropdown.
        """

        self.escalar_vec = valor

    def update_vec1(self, valor: str) -> None:
        """
        Actualiza el valor de self.vec1 con
        el valor seleccionado en el dropdown.
        """

        self.vec1 = valor

    def update_vec2(self, valor: str) -> None:
        """
        Actualiza el valor de self.vec2 con
        el valor seleccionado en el dropdown.
        """

        self.vec2 = valor

    def update_vmat(self, valor: str) -> None:
        """
        Actualiza el valor de self.vmat con
        el valor seleccionado en el dropdown.
        """

        self.vmat = valor

    def update_mvec(self, valor: str) -> None:
        """
        Actualiza el valor de self.mvec con
        el valor seleccionado en el dropdown.
        """

        self.mvec = valor
