"""
Implementación de todos los frames de operaciones de matrices.
"""

from fractions import Fraction
from random import choice
from tkinter import Variable
from typing import TYPE_CHECKING, Literal

from bidict import bidict
from customtkinter import CTkButton, CTkFont, CTkFrame, CTkLabel, CTkTabview

from src.gui.custom import CustomDropdown, CustomEntry
from src.gui.custom.adapted import CustomScrollFrame
from src.managers import MatricesManager
from src.utils import (
    INPUTS_ICON,
    delete_msg_frame,
    delete_msg_if,
    generate_range,
    place_msg_frame,
    toggle_proc,
)

if TYPE_CHECKING:
    from src.gui.frames.matrices import MatricesFrame
    from src.gui.gui import GaussUI


class SumaRestaTab(CustomScrollFrame):
    """
    Frame para sumar y restar matrices.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de suma y resta de matrices.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.msg_frame: CTkFrame | None = None
        self.operaciones: bidict[str, str] = bidict({"Sumar": "+", "Restar": "−"})

        # definir atributos; se inicializan en setup_frame
        self.instruct_sr: CTkLabel
        self.select_operacion: CustomDropdown
        self.select_1: CustomDropdown
        self.select_2: CustomDropdown
        self.ejecutar_button: CTkButton
        self.resultado_frame: CTkFrame

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.operacion: Literal["+", "−"] = "+"
        self.mat1: str = ""
        self.mat2: str = ""

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar frame y atributos.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(self, value=self.master_frame.nombres_matrices[0])

        if len(self.master_frame.nombres_matrices) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(self, value=self.master_frame.nombres_matrices[1])

        # crear widgets
        self.instruct_sr = CTkLabel(
            self,
            text="Seleccione las matrices a sumar:",
        )

        self.select_operacion = CustomDropdown(
            self,
            width=40,
            font=CTkFont(size=16),
            values=list(self.operaciones.values()),
            variable=Variable(value=self.operaciones["Sumar"]),
            command=self.update_operacion,
        )

        self.select_1 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_mat1,
        )

        self.select_2 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder2,
            command=self.update_mat2,
        )

        self.mat1 = self.select_1.get()
        self.mat2 = self.select_2.get()
        self.ejecutar_button = CTkButton(
            self,
            height=30,
            text="Sumar",
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
        Sumar o restar las matrices seleccionadas.
        """

        for widget in self.resultado_frame.winfo_children():
            widget.destroy()

        self.update_operacion(self.select_operacion.get())  # type: ignore[reportArgumentType]
        self.update_mat1(self.select_1.get())
        self.update_mat2(self.select_2.get())
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
            proc, header, resultado = self.mats_manager.suma_resta_mats(
                self.operacion,
                self.mat1,
                self.mat2,
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
            msg=f"\n{header}:\n{resultado}\n",
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
        Actualizar colores de widgets y valores de dropdowns.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        if len(self.master_frame.nombres_matrices) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(self, value=self.master_frame.nombres_matrices[1])

        self.select_1.configure(
            variable=placeholder1,
            values=self.master_frame.nombres_matrices,
        )

        self.select_2.configure(
            variable=placeholder2,
            values=self.master_frame.nombres_matrices,
        )

    def update_operacion(self, valor: Literal["+", "−"]) -> None:
        """
        Actualizar botón de ejecutar operación y texto de la instrucción.

        Args:
            valor: Operación a realizar.

        """

        op_text: str = self.operaciones.inverse[valor]
        self.ejecutar_button.configure(text=op_text)
        self.instruct_sr.configure(text=f"Seleccione las matrices a {op_text.lower()}:")
        self.operacion = valor

    def update_mat1(self, valor: str) -> None:
        """
        Actualizar primera matriz seleccionada.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.mat1 = valor

    def update_mat2(self, valor: str) -> None:
        """
        Actualizar segunda matriz seleccionada.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.mat2 = valor


class MultiplicacionTab(CustomScrollFrame):
    """
    Frame para realizar multiplicación escalar,
    multiplicación matricial y producto matriz-vector.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de multiplicación de matrices.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.msg_frame: CTkFrame | None = None

        # definir atributos; se inicializan en setup_tabs
        self.select_escalar_mat: CustomDropdown
        self.escalar_entry: CustomEntry
        self.select_mat1: CustomDropdown
        self.select_mat2: CustomDropdown
        self.select_mvec: CustomDropdown
        self.select_vmat: CustomDropdown

        self.escalar_mat: str = ""
        self.mat1: str = ""
        self.mat2: str = ""
        self.vmat: str = ""
        self.mvec: str = ""

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.tabview = CTkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        # crear tabs
        self.tab_escalar = self.tabview.add("Escalar por Matriz")
        self.tab_mats = self.tabview.add("Multiplicación Matricial")
        self.tab_mat_vec = self.tabview.add("Matriz por Vector")
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
        self.resultado_mats = CTkFrame(self.tab_mats, fg_color="transparent")
        self.resultado_mat_vec = CTkFrame(self.tab_mat_vec, fg_color="transparent")

        self.setup_escalar_tab()
        self.setup_mult_mats_tab()

        if len(self.master_frame.nombres_vectores) >= 1:
            self.setup_mat_vec_tab()
        else:
            # si no hay vectores, informar al usuario
            self.msg_frame = place_msg_frame(
                parent_frame=self.tab_mat_vec,
                msg_frame=self.msg_frame,
                msg="¡No hay vectores guardados!",
                tipo="error",
                columnspan=3,
            )

            # y dirigirlos al menu de datos para agregar vectores
            CTkButton(
                self.tab_mat_vec,
                height=30,
                text="Agregar vectores",
                image=INPUTS_ICON,
                command=lambda: self.app.home_frame.ir_a_frame("vectores"),
            ).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_escalar_tab(self) -> None:
        """
        Configurar pestaña de multiplicación escalar.
        """

        # crear widgets
        operador_label = CTkLabel(self.tab_escalar, text="•", font=CTkFont(size=16))
        instruct_e = CTkLabel(
            self.tab_escalar,
            text="Seleccione la matriz e ingrese el escalar:",
        )

        self.select_escalar_mat = CustomDropdown(
            self.tab_escalar,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_escalar_mat,
        )

        self.escalar_mat = self.select_escalar_mat.get()
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
        self.select_escalar_mat.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        multiplicar_button.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=10,
            sticky="n",
        )

    def setup_mult_mats_tab(self) -> None:
        """
        Configurar pestaña de multiplicación matricial.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        if len(self.master_frame.nombres_matrices) == 1:
            # si solo hay una matriz, ocupar el mismo placeholder
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_matrices[1])

        # crear widgets
        operador_label = CTkLabel(self.tab_mats, text="•", font=CTkFont(size=16))
        instruct_ms = CTkLabel(
            self.tab_mats,
            text="Seleccione las matrices a multiplicar:",
        )

        self.select_mat1 = CustomDropdown(
            self.tab_mats,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_mat1,
        )

        self.select_mat2 = CustomDropdown(
            self.tab_mats,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder2,
            command=self.update_mat2,
        )

        self.mat1 = self.select_mat1.get()
        self.mat2 = self.select_mat2.get()
        multiplicar_button = CTkButton(
            self.tab_mats,
            height=30,
            text="Multiplicar",
            command=self.mult_matrices,
        )

        # colocar widgets
        instruct_ms.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_mat1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mat2.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        multiplicar_button.grid(
            row=2,
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
        Multiplicar matriz seleccionada por escalar ingresado.
        """

        for widget in self.resultado_escalar.winfo_children():
            widget.destroy()

        self.update_escalar_mat(self.select_escalar_mat.get())
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
            proc, header, resultado = self.mats_manager.escalar_por_mat(
                escalar,
                self.escalar_mat,
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

    def mult_matrices(self) -> None:
        """
        Multiplicar matrices seleccionadas.
        """

        for widget in self.resultado_mats.winfo_children():
            widget.destroy()

        self.update_mat1(self.select_mat1.get())
        self.update_mat2(self.select_mat2.get())
        self.resultado_mats.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_mats, self.resultado_mats))
        try:
            proc, header, resultado = self.mats_manager.mult_mats(self.mat1, self.mat2)
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado_mats,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )
            return
        delete_msg_if(self.msg_frame, (self.tab_mats, self.resultado_mats))

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_mats,
            msg_frame=self.msg_frame,
            msg=f"\n{header}:\n{resultado!s}\n",
            tipo="resultado",
        )

        CTkButton(
            self.resultado_mats,
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

    def mult_mat_vec(self) -> None:
        """
        Multiplicar matriz y vector seleccionados.
        """

        for widget in self.resultado_mat_vec.winfo_children():
            widget.destroy()

        self.update_mvec(self.select_vmat.get())
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

    def update_escalar_mat(self, valor: str) -> None:
        """
        Actualizar matriz seleccionada para multiplicación escalar.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.escalar_mat = valor

    def update_mat1(self, valor: str) -> None:
        """
        Actualizar primera matriz seleccionada para multiplicación matricial.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.mat1 = valor

    def update_mat2(self, valor: str) -> None:
        """
        Actualizar segunda matriz seleccionada para multiplicación matricial.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.mat2 = valor

    def update_vmat(self, valor: str) -> None:
        """
        Actualizar matriz seleccionada para producto matriz-vector.

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


class DeterminanteTab(CustomScrollFrame):
    """
    Frame para calcular el determinante de una matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de determinantes.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        # definir atributos, inicalizados en setup_frame()
        self.msg_frame: CTkFrame | None = None
        self.select_dmat: CustomDropdown
        self.dmat: str = ""
        self.resultado: CTkFrame

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar y configurar widgets.
        """

        delete_msg_frame(self.msg_frame)
        instruct_d = CTkLabel(
            self,
            text="Seleccione una matriz para calcular su determinante:",
        )

        self.select_dmat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_dmat,
        )

        self.dmat = self.select_dmat.get()
        button = CTkButton(
            self,
            height=30,
            text="Calcular",
            command=self.calcular_determinante,
        )

        self.resultado = CTkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        instruct_d.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_dmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def calcular_determinante(self) -> None:
        """
        Calcular determinante de la matriz seleccionada.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.resultado.winfo_children():
            widget.destroy()

        self.update_dmat(self.select_dmat.get())

        try:
            proc, header, resultado = self.mats_manager.calcular_determinante(self.dmat)
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )

            return

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            msg=f"{header}  =  {resultado}",
            tipo="resultado",
        )

        CTkButton(
            self.resultado,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento para calcular "
                f"el determinante de la matriz {self.dmat}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualizar valores del dropdown.
        """

        self.select_dmat.configure(
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            values=self.master_frame.nombres_matrices,
        )

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

    def update_dmat(self, valor: str) -> None:
        """
        Actualizar matriz seleccionada.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.dmat = valor


class TransposicionTab(CustomScrollFrame):
    """
    Frame para transponer una matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de transposición.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        # definir atributos, inicializados en setup_frame()
        self.msg_frame: CTkFrame | None = None
        self.select_tmat: CustomDropdown
        self.tmat: str = ""
        self.resultado: CTkFrame

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar y configurar widgets.
        """

        delete_msg_frame(self.msg_frame)
        instruct_t = CTkLabel(self, text="Seleccione la matriz a transponer:")

        self.select_tmat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_tmat,
        )

        self.tmat = self.select_tmat.get()
        button = CTkButton(
            self,
            height=30,
            text="Transponer",
            command=self.encontrar_transpuesta,
        )

        self.resultado = CTkFrame(self, fg_color="transparent")
        self.resultado.columnconfigure(0, weight=1)

        instruct_t.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_tmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def encontrar_transpuesta(self) -> None:
        """
        Transponer matriz seleccionada.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.resultado.winfo_children():
            widget.destroy()

        self.update_tmat(self.select_tmat.get())
        proc, nombre_transpuesta, transpuesta = self.mats_manager.transponer_mat(
            self.tmat,
        )

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            msg=f"\n{nombre_transpuesta}:\n{transpuesta!s}\n",
            tipo="resultado",
            columnspan=3,
        )

        CTkButton(
            self.resultado,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento de la "
                f"transposición de la matriz {self.tmat}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualizar valores del dropdown.
        """

        self.select_tmat.configure(
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            values=self.master_frame.nombres_matrices,
        )

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

    def update_tmat(self, valor: str) -> None:
        """
        Actualizar matriz seleccionada.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.tmat = valor


class InversaTab(CustomScrollFrame):
    """
    Frame para encontrar la inversa de una matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de inversas.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        # definir atributos, se inicializan en setup_frame()
        self.msg_frame: CTkFrame | None = None
        self.select_imat: CustomDropdown
        self.imat: str = ""
        self.resultado: CTkFrame

        self.proc_label: CTkLabel | None = None
        self.proc_hidden = True

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar y configurar widgets.
        """

        delete_msg_frame(self.msg_frame)
        instruct_i = CTkLabel(self, text="Seleccione la matriz a invertir:")

        self.select_imat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_imat,
        )

        self.imat = self.select_imat.get()
        button = CTkButton(
            self,
            height=30,
            text="Invertir",
            command=self.encontrar_inversa,
        )

        self.resultado = CTkFrame(self, fg_color="transparent")
        self.resultado.columnconfigure(0, weight=1)

        instruct_i.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_imat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def encontrar_inversa(self) -> None:
        """
        Invertir matriz seleccionada.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.resultado.winfo_children():
            widget.destroy()

        self.update_imat(self.select_imat.get())

        try:
            proc, nombre_inversa, inversa = self.mats_manager.invertir_mat(self.imat)
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )

            return

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.msg_frame,
            msg=f"\n{nombre_inversa}:\n{inversa}\n",
            tipo="resultado",
            columnspan=3,
        )

        CTkButton(
            self.resultado,
            text="Mostrar procedimiento",
            command=lambda: toggle_proc(
                app=self.app,
                parent_frame=self,
                window_title="GaussBot: Procedimiento para encontrar "
                f"la inversa de la matriz {self.imat}",
                proc_label=self.proc_label,
                label_txt=proc,
                proc_hidden=self.proc_hidden,
            ),
        ).grid(row=1, column=0, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Actualizar valores del dropdown.
        """

        self.select_imat.configure(
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            values=self.master_frame.nombres_matrices,
        )

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

    def update_imat(self, valor: str) -> None:
        """
        Actualizar matriz seleccionada.

        Args:
            valor: Nueva matriz seleccionada.

        """

        self.imat = valor
