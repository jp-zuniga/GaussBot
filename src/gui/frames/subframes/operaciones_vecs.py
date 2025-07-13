"""
Implementación de todos los frames de operaciones de vectores.
"""

from decimal import Decimal
from fractions import Fraction
from random import choice
from tkinter import Variable
from typing import TYPE_CHECKING, Literal

from bidict import bidict
from customtkinter import CTkButton, CTkFont, CTkFrame, CTkLabel, CTkTabview

from src.gui.custom import CustomDropdown, CustomEntry, IconButton
from src.gui.custom.adapted import CustomScrollFrame
from src.managers import VectoresManager
from src.models import Vector
from src.utils import (
    ENTER_ICON,
    INFO_ICON,
    INPUTS_ICON,
    delete_msg_frame,
    delete_msg_if,
    format_factor,
    generate_range,
    place_msg_frame,
    toggle_proc,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.frames import VectoresFrame


class MagnitudTab(CustomScrollFrame):
    """
    Frame para calcular la magnitud de un vector ingresado por el usuario.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de magnitud de vectores.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.msg_frame: CTkFrame | None = None
        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        # crear widgets
        instruct_m = CTkLabel(
            self,
            text="Seleccione un vector del para calcular su magnitud:",
        )

        self.select_vec = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=Variable(value=self.master_frame.nombres_vectores[0]),
            command=self.update_vec,
        )

        self.vec = self.select_vec.get()
        calcular_button = CTkButton(
            self,
            height=30,
            text="Calcular",
            command=self.calcular_magnitud,
        )

        self.resultado_frame = CTkFrame(self, fg_color="transparent")

        # colocar widgets
        instruct_m.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vec.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        calcular_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def calcular_magnitud(self) -> None:
        """
        Calcular magnitud del vector seleccionado.
        """

        for widget in self.resultado_frame.winfo_children():
            widget.destroy()

        self.resultado_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
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

        CTkButton(
            self.resultado_frame,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento para calcular la "
                f"magnitud del vector {self.vec}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualizar widgets y datos del frame.
        """

        self.select_vec.configure(
            values=self.master_frame.nombres_vectores,
            variable=Variable(value=self.master_frame.nombres_vectores[0]),
        )

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

    def update_vec(self, valor: str) -> None:
        """
        Actualizar vector seleccionado.

        Args:
            valor: Nuevo vector seleccionado.

        """

        self.vec = valor


class SumaRestaTab(CustomScrollFrame):
    """
    Frame para sumar y restar vectores ingresados por el usuario.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de suma y resta de vectores.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.msg_frame: CTkFrame | None = None

        # para el boton de ejecutar y el dropdown de operadores
        self.operaciones: bidict[str, Literal["+", "−"]] = bidict(
            {"Sumar": "+", "Restar": "−"},
        )

        # definir atributos, se inicializan en setup_frame()
        self.instruct_sr: CTkLabel
        self.select_operacion: CustomDropdown
        self.select_1: CustomDropdown
        self.select_2: CustomDropdown
        self.ejecutar_button: CTkButton
        self.resultado_frame: CTkFrame

        self.operacion: Literal["+", "−"] = "+"
        self.vec1: str = ""
        self.vec2: str = ""

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.setup_frame()

    def setup_frame(self, default: str = "Sumar") -> None:
        """
        Inicializar y configurar widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        # crear widgets
        self.instruct_sr = CTkLabel(
            self,
            text=f"Seleccione los vectores a {default.lower()}:",
        )

        self.select_operacion = CustomDropdown(
            self,
            width=40,
            font=CTkFont(size=16),
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
        self.ejecutar_button = CTkButton(
            self,
            height=30,
            text=default,
            command=self.ejecutar_operacion,
        )

        self.resultado_frame = CTkFrame(self, fg_color="transparent")

        # colocar widgets
        self.instruct_sr.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.select_operacion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_2.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.ejecutar_button.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=10,
            sticky="n",
        )

    def ejecutar_operacion(self) -> None:
        """
        Sumar o restar los vectores seleccionados.
        """

        for widget in self.resultado_frame.winfo_children():
            widget.destroy()

        self.update_operacion(self.select_operacion.get())  # type: ignore[reportArgumentType]
        self.update_vec1(self.select_1.get())
        self.update_vec2(self.select_2.get())
        self.resultado_frame.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

        delete_msg_frame(self.msg_frame)
        try:
            proc, header, resultado = self.vecs_manager.suma_resta_vecs(
                self.operacion,
                self.vec1,
                self.vec2,
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
            msg=f"\n{header}:\n{resultado!s}\n",
            tipo="resultado",
        )

        CTkButton(
            self.resultado_frame,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title=f"GaussBot: Procedimiento de {header}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualizar widgets y datos del frame.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        self.select_1.configure(
            variable=placeholder1,
            values=self.master_frame.nombres_vectores,
        )

        self.select_2.configure(
            variable=placeholder2,
            values=self.master_frame.nombres_vectores,
        )

    def update_operacion(self, valor: Literal["+", "−"]) -> None:
        """
        Actualizar botón de ejecutar operación y texto de la instrucción.

        Args:
            valor: Operación a realizar.

        """

        op_text = self.operaciones.inverse[valor]
        self.ejecutar_button.configure(text=op_text)
        self.instruct_sr.configure(text=f"Seleccione los vectores a {op_text.lower()}:")
        self.operacion = valor

    def update_vec1(self, valor: str) -> None:
        """
        Actualizar vector seleccionado.

        Args:
            valor: Nuevo primer vector seleccionado.

        """

        self.vec1 = valor

    def update_vec2(self, valor: str) -> None:
        """
        Actualizar vector seleccionado.

        Args:
            valor: Nuevo segundo vector seleccionado.

        """

        self.vec2 = valor


class MultiplicacionTab(CustomScrollFrame):
    """
    Frame para realizar multiplicación escalar,
    producto punto, producto cruz
    y producto matriz-vector.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de multiplicación.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        # definir atributos, se inicializan en setup_tabs()
        self.msg_frame: CTkFrame | None = None
        self.select_escalar_vec: CustomDropdown
        self.escalar_entry: CustomEntry
        self.dimension_entry: CustomEntry
        self.select_vec1: CustomDropdown
        self.select_vec2: CustomDropdown
        self.select_vmat: CustomDropdown
        self.select_mvec: CustomDropdown

        self.escalar_vec: str = ""
        self.vec1: str = ""
        self.vec2: str = ""
        self.vmat: str = ""
        self.mvec: str = ""

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.tabview = CTkTabview(self, fg_color="transparent")
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
        """

        for tab in self.tabview.winfo_children():
            tab.columnconfigure(0, weight=1)
            tab.columnconfigure(2, weight=1)

        # crear frames de resultado
        self.resultado_escalar = CTkFrame(self.tab_escalar, fg_color="transparent")
        self.resultado_punto = CTkFrame(self.tab_prod_punto, fg_color="transparent")
        self.resultado_cruz = CTkFrame(self.tab_prod_cruz, fg_color="transparent")
        self.resultado_mat_vec = CTkFrame(self.tab_mat_vec, fg_color="transparent")

        self.setup_escalar_tab()
        self.setup_prod_punto_tab()
        self.setup_prod_cruz_tab()

        if len(self.master_frame.nombres_matrices) >= 1:
            self.setup_mat_vec_tab()
        else:
            self.msg_frame = place_msg_frame(
                parent_frame=self.tab_mat_vec,
                msg_frame=self.msg_frame,
                msg="¡No hay matrices guardadas!",
                tipo="error",
                columnspan=3,
            )

            CTkButton(
                self.tab_mat_vec,
                height=30,
                text="Agregar matrices",
                image=INPUTS_ICON,
                command=lambda: self.app.home_frame.ir_a_frame("matrices"),
            ).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_escalar_tab(self) -> None:
        """
        Configurar pestaña de multiplicación escalar.
        """

        delete_msg_frame(self.msg_frame)

        # crear widgets
        operador_label = CTkLabel(self.tab_escalar, text="•", font=CTkFont(size=16))
        instruct_e = CTkLabel(
            self.tab_escalar,
            text="Seleccione el vector e ingrese el escalar:",
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
            width=80,
            placeholder_text=str(choice(generate_range(-10, 10))),
        )

        self.escalar_entry.bind("<Return>", lambda _: self.mult_por_escalar())
        multiplicar_button = CTkButton(
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
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=10,
            sticky="n",
        )

    def setup_prod_punto_tab(self) -> None:
        """
        Configurar pestaña de producto punto.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        # crear widgets
        operador_label = CTkLabel(self.tab_prod_punto, text=".", font=CTkFont(size=26))
        instruct_v = CTkLabel(
            self.tab_prod_punto,
            text="Seleccione los vectores a multiplicar:",
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
        multiplicar_button = CTkButton(
            self.tab_prod_punto,
            height=30,
            text="Multiplicar",
            command=self.prod_punto,
        )

        # colocar widgets
        instruct_v.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vec1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_vec2.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        multiplicar_button.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=10,
            sticky="n",
        )

    def setup_prod_cruz_tab(self) -> None:
        """
        Configurar pestaña de producto cruz.
        """

        delete_msg_frame(self.msg_frame)
        CTkLabel(self.tab_prod_cruz, text="Ingrese las dimensiones:").grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.dimension_entry = CustomEntry(
            self.tab_prod_cruz,
            placeholder_text="3",
            width=60,
        )

        self.dimension_entry.bind(
            "<Return>",
            lambda _: setup_selections(self.dimension_entry.get()),
        )

        self.dimension_entry.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        IconButton(
            self.tab_prod_cruz,
            image=ENTER_ICON,
            tooltip_text="Ingresar dimension",
            command=lambda: setup_selections(self.dimension_entry.get()),
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        def setup_selections(input_dim: str) -> None:
            """
            Inicializa widgets para seleccionar vectores a multiplicar.

            Args:
                input_dim: Dimensión seleccionada para multiplicación.

            """

            delete_msg_frame(self.msg_frame)
            for widget in self.tab_prod_cruz.winfo_children():
                if (
                    widget is not self.resultado_cruz
                    and dict(widget.grid_info()).get("row", -1) > 0
                ):
                    widget.destroy()

            dims_invalidas: str = "Debe ingresar un número entero mayor a 1."
            falta_vectores: str = f"No hay suficientes vectores en R{
                input_dim
            } para calcular un producto cruz."

            try:
                dimension = int(input_dim)
                if dimension <= 1:
                    raise ValueError  # noqa: TRY301
            except ValueError:
                self.msg_frame = place_msg_frame(
                    parent_frame=self.tab_prod_cruz,
                    msg_frame=self.msg_frame,
                    msg=dims_invalidas,
                    tipo="error",
                    row=1,
                    columnspan=3,
                )

                return

            if dimension - 1 > len(self.master_frame.nombres_vectores):
                self.msg_frame = place_msg_frame(
                    parent_frame=self.tab_prod_cruz,
                    msg_frame=self.msg_frame,
                    msg=falta_vectores,
                    tipo="error",
                    row=1,
                    columnspan=3,
                )

                return

            dropdowns: list[CustomDropdown] = []
            vecs_validos = [
                nombre
                for nombre, vec in self.vecs_manager.vecs_ingresados.items()
                if len(vec) == dimension
            ]

            if not vecs_validos:
                self.msg_frame = place_msg_frame(
                    parent_frame=self.tab_prod_cruz,
                    msg_frame=self.msg_frame,
                    msg=f"¡No se han guardado vectores en R{dimension}!",
                    tipo="error",
                    row=1,
                    columnspan=3,
                )

                return

            IconButton(
                self.tab_prod_cruz,
                image=INFO_ICON,
                tooltip_text="Solamente se están mostrando "
                f"vectores guardados en R{dimension}.",
            ).grid(row=1, column=0, columnspan=3, padx=5, pady=(15, 3), sticky="n")

            CTkLabel(
                self.tab_prod_cruz,
                text="Seleccione los vectores a multiplicar:",
            ).grid(row=2, column=0, columnspan=3, padx=5, pady=3, sticky="n")

            range_dims = dimension if dimension == 2 else dimension - 1
            for i in range(range_dims):
                dropdowns.append(
                    CustomDropdown(
                        self.tab_prod_cruz,
                        width=60,
                        values=vecs_validos,
                        variable=Variable(value=vecs_validos[i]),
                    ),
                )

                dropdowns[i].grid(
                    row=i + 3,
                    column=0,
                    columnspan=3,
                    padx=5,
                    pady=5,
                    sticky="n",
                )

            CTkButton(
                self.tab_prod_cruz,
                height=30,
                text="Multiplicar",
                command=lambda: self.prod_cruz(dropdowns),
            ).grid(
                row=dimension + 3,
                column=0,
                columnspan=3,
                padx=5,
                pady=10,
                sticky="n",
            )

    def setup_mat_vec_tab(self) -> None:
        """
        Configurar pestaña de producto matriz-vector.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(value=self.master_frame.nombres_vectores[0])

        # crear widgets
        operador_label = CTkLabel(self.tab_mat_vec, text="•", font=CTkFont(size=16))
        instruct_mv = CTkLabel(
            self.tab_mat_vec,
            text="Seleccione la matriz y el vector a multiplicar:",
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
        multiplicar_button = CTkButton(
            self.tab_mat_vec,
            height=30,
            text="Multiplicar",
            command=self.mult_mat_vec,
        )

        # colocar widgets
        instruct_mv.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vmat.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mvec.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        multiplicar_button.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=10,
            sticky="n",
        )

    def mult_por_escalar(self) -> None:
        """
        Multiplicar vector seleccionado por escalar ingresado.
        """

        for widget in self.resultado_escalar.winfo_children():
            widget.destroy()

        self.update_escalar_vec(self.select_escalar_vec.get())
        self.resultado_escalar.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_escalar, self.resultado_escalar))
        try:
            escalar = Fraction(self.escalar_entry.get())
            proc, header, resultado = self.vecs_manager.escalar_por_vec(
                escalar,
                self.escalar_vec,
            )
        except (ValueError, ZeroDivisionError) as e:
            if isinstance(e, ValueError):
                msg = "El escalar debe ser un número racional."
            else:
                msg = "El denominador de una fracción no puede ser 0."

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
            msg=f"\n{header}:\n{resultado!s}\n",
            tipo="resultado",
        )

        CTkButton(
            self.resultado_escalar,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title=f"GaussBot: Procedimiento de la multiplicación {header}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def prod_punto(self) -> None:
        """
        Calcular producto punto de vectores seleccionados.
        """

        for widget in self.resultado_punto.winfo_children():
            widget.destroy()

        self.update_vec1(self.select_vec1.get())
        self.update_vec2(self.select_vec2.get())
        self.resultado_punto.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_prod_punto, self.resultado_punto))
        try:
            proc, header, resultado = self.vecs_manager.producto_punto(
                self.vec1,
                self.vec2,
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
            msg=f"{header}:\n{resultado!s}",
            tipo="resultado",
            ipadx=5,
            ipady=5,
        )

        CTkButton(
            self.resultado_punto,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title=f"GaussBot: Procedimiento de la multiplicación {header}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def prod_cruz(self, dropdowns: list[CustomDropdown]) -> None:
        """
        Calcular producto cruz de vectores seleccionados.
        """

        delete_msg_frame(self.msg_frame)
        vectores = [
            self.vecs_manager.vecs_ingresados[dropdown.get()] for dropdown in dropdowns
        ]

        self.resultado_cruz.grid(
            row=len(vectores) + 5,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

        header = " × ".join([dropdown.get() for dropdown in dropdowns])
        resultado = Vector.prod_cruz(len(vectores[0]), vectores)

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_cruz,
            msg_frame=self.msg_frame,
            msg=f"\n{header}:\n{resultado!s}\n",
            tipo="resultado",
        )

    def mult_mat_vec(self) -> None:
        """
        Multiplicar matriz y vector seleccionados.
        """

        self.update_vmat(self.select_vmat.get())
        self.update_mvec(self.select_mvec.get())
        self.resultado_mat_vec.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_mat_vec, self.resultado_mat_vec))
        try:
            proc, header, resultado = self.app.ops_manager.mat_por_vec(
                self.vmat,
                self.mvec,
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
            msg=f"\n{header}:\n{resultado!s}\n",
            tipo="resultado",
        )

        CTkButton(
            self.resultado_mat_vec,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title=f"GaussBot: Procedimiento de la multiplicación {header}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Correr setup nuevamente para actualizar frame.
        """

        for tab in self.tabview.winfo_children():
            for widget in tab.winfo_children():
                widget.destroy()

        self.setup_tabs()
        self.tabview.configure(bg_color="transparent")
        self.tabview.configure(fg_color="transparent")

    def update_escalar_vec(self, valor: str) -> None:
        """
        Actualizar vector seleccionado para multiplicación escalar.

        Args:
            valor: Nueva vector seleccionado.

        """

        self.escalar_vec = valor

    def update_vec1(self, valor: str) -> None:
        """
        Actualizar primer vector seleccionado para producto punto.

        Args:
            valor: Nueva vector seleccionado.

        """

        self.vec1 = valor

    def update_vec2(self, valor: str) -> None:
        """
        Actualizar segundo vector seleccionado para producto punto.

        Args:
            valor: Nueva vector seleccionado.

        """

        self.vec2 = valor

    def update_vmat(self, valor: str) -> None:
        """
        Actualizar vector seleccionado para producto matriz-vector.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.vmat = valor

    def update_mvec(self, valor: str) -> None:
        """
        Actualizar vector seleccionado para producto matriz-vector.

        Args:
            valor: Nuevo vector seleccionado.

        """

        self.mvec = valor
