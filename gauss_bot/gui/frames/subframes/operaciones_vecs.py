"""
Implementación de todos los frames
de operaciones con vectores.
"""

from fractions import Fraction
from random import choice
from typing import (
    TYPE_CHECKING,
    Optional,
)

from tkinter import Variable
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkTabview as ctkTabview,
)

from gauss_bot import (
    INPUTS_ICON,
    delete_msg_frame,
    delete_msg_if,
    generate_range,
    get_dict_key
)

from gauss_bot.managers import VectoresManager
from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    place_msg_frame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import VectoresFrame


class VSumaRestaTab(CustomScrollFrame):
    """
    Frame para sumar y restar vectores ingresados por el usuario.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.msg_frame: Optional[ctkFrame] = None

        # para el boton de ejecutar y el dropdown de operadores
        self.operaciones: dict[str, str] = {
            "Sumar": "+",
            "Restar": "−",
        }

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
            self,
            text=f"Seleccione los vectores a {default.lower()}:"
        )

        self.select_operacion = CustomDropdown(
            self,
            width=40,
            font=("Roboto", 16),
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
            self,
            height=30,
            text=default,
            command=self.ejecutar_operacion,
        )

        self.resultado_frame = ctkFrame(self, fg_color="transparent")

        # colocar widgets
        self.instruct_sr.grid(
            row=0, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n"
        )

        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.select_operacion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_2.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.ejecutar_button.grid(
            row=2, column=0,
            columnspan=3,
            padx=5, pady=10,
            sticky="n",
        )

    def ejecutar_operacion(self) -> None:
        """
        Suma o resta las matrices seleccionadas.
        """

        self.update_operacion(self.select_operacion.get())
        self.update_vec1(self.select_1.get())
        self.update_vec2(self.select_2.get())
        self.resultado_frame.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

        delete_msg_frame(self.msg_frame)
        try:
            if self.operacion == "+":
                header, resultado = (
                    self.vecs_manager.suma_resta_vecs(
                        True, self.vec1, self.vec2
                    )
                )
            elif self.operacion == "−":
                header, resultado = (
                    self.vecs_manager.suma_resta_vecs(
                        False, self.vec1, self.vec2
                    )
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
            msg=f"{header}:\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
        )

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
            variable=placeholder1,
            values=self.master_frame.nombres_vectores,
        )

        self.select_2.configure(
            variable=placeholder2,
            values=self.master_frame.nombres_vectores,
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
        self.instruct_sr.configure(
            text=f"Seleccione las matrices a {op_text.lower()}:"
        )

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


class VMultiplicacionTab(CustomScrollFrame):
    """
    Frame para realizar multiplicaciones de vectores por escalares,
    producto punto y producto matriz-vector.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "VectoresFrame",
        vecs_manager: VectoresManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        # definir atributos, se inicializan en setup_tabs()
        self.msg_frame: Optional[ctkFrame] = None
        self.select_escalar_vec: CustomDropdown
        self.escalar_entry: CustomEntry
        self.select_vec1: CustomDropdown
        self.select_vec2: CustomDropdown
        self.select_vmat: CustomDropdown
        self.select_mvec: CustomDropdown

        self.escalar_vec = ""
        self.vec1 = ""
        self.vec2 = ""
        self.vmat = ""
        self.mvec = ""

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        # crear tabs
        self.tab_escalar = self.tabview.add("Escalar por Vector")
        self.tab_prod_punto = self.tabview.add("Producto Punto")
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
        self.resultado_vecs = ctkFrame(self.tab_prod_punto, fg_color="transparent")
        self.resultado_mat_vec = ctkFrame(
            self.tab_mat_vec, fg_color="transparent"
        )

        self.setup_escalar_tab()
        self.setup_prod_punto_tab()

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
                command=lambda: self.app.home_frame.ir_a_matriz(mostrar=False),  # type: ignore
            ).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_escalar_tab(self) -> None:
        """
        Setup de la tab para multiplicar un vector por un escalar.
        """

        delete_msg_frame(self.msg_frame)

        # crear widgets
        operador_label = ctkLabel(self.tab_escalar, text="•", font=("Roboto", 16))
        instruct_e = ctkLabel(
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
            width=60,
            placeholder_text=str(choice(generate_range(-10, 10))),
        )

        self.escalar_entry.bind(
            "<Return>",
            lambda _: self.mult_por_escalar(),
        )

        multiplicar_button = ctkButton(
            self.tab_escalar,
            height=30,
            text="Multiplicar",
            command=self.mult_por_escalar,
        )

        # colocar widgets
        instruct_e.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.escalar_entry.grid(row=1, column=0, ipadx=5, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_escalar_vec.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(
            row=2, column=0,
            columnspan=3,
            padx=5, pady=10,
            sticky="n",
        )

    def setup_prod_punto_tab(self) -> None:
        """
        Setup de la tab para multiplicar vectores.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_vectores[1])

        # crear widgets
        operador_label = ctkLabel(
            self.tab_prod_punto,
            text=".",
            font=("Roboto", 16),
        )

        instruct_v = ctkLabel(
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
        multiplicar_button = ctkButton(
            self.tab_prod_punto,
            height=30,
            text="Multiplicar",
            command=self.prod_punto,
        )

        # colocar widgets
        instruct_v.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vec1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_vec2.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(
            row=2, column=0,
            columnspan=3,
            padx=5, pady=10,
            sticky="n",
        )

    def setup_mat_vec_tab(self) -> None:
        """
        Setup de la tab para multiplicar matrices y vectores.
        """

        delete_msg_frame(self.msg_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(value=self.master_frame.nombres_vectores[0])

        # crear widgets
        operador_label = ctkLabel(self.tab_mat_vec, text="•", font=("Roboto", 16))
        instruct_mv = ctkLabel(
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
        multiplicar_button = ctkButton(
            self.tab_mat_vec,
            height=30,
            text="Multiplicar",
            command=self.mult_mat_vec,
        )

        # colocar widgets
        instruct_mv.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_vmat.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mvec.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(
            row=2, column=0,
            columnspan=3,
            padx=5, pady=10,
            sticky="n",
        )

    def mult_por_escalar(self) -> None:
        """
        Realiza la multiplicación de un vector por un escalar.
        """

        self.update_escalar_vec(self.select_escalar_vec.get())
        self.resultado_escalar.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_escalar, self.resultado_escalar))
        try:
            escalar = Fraction(self.escalar_entry.get())  # type: ignore
            header, resultado = (
                self.vecs_manager.escalar_por_vector(
                    escalar,
                    self.escalar_vec,
                )
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
            msg=f"{header}:\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
        )

    def prod_punto(self) -> None:
        """
        Realiza el producto punto de dos vectores.
        """

        self.update_vec1(self.select_vec1.get())
        self.update_vec2(self.select_vec2.get())
        self.resultado_vecs.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_prod_punto, self.resultado_vecs))
        try:
            header, resultado = (
                self.vecs_manager.producto_punto(
                    self.vec1,
                    self.vec2
                )
            )
        except ArithmeticError as e:
            self.msg_frame = place_msg_frame(
                parent_frame=self.resultado_vecs,
                msg_frame=self.msg_frame,
                msg=str(e),
                tipo="error",
            )
            return
        delete_msg_if(self.msg_frame, (self.tab_prod_punto, self.resultado_vecs))

        self.msg_frame = place_msg_frame(
            parent_frame=self.resultado_vecs,
            msg_frame=self.msg_frame,
            msg=f"{header}:\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
        )

    def mult_mat_vec(self) -> None:
        """
        Realiza el producto de una matriz por un vector.
        """

        self.update_vmat(self.select_vmat.get())
        self.update_mvec(self.select_mvec.get())
        self.resultado_mat_vec.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

        delete_msg_if(self.msg_frame, (self.tab_mat_vec, self.resultado_mat_vec))
        try:
            header, resultado = (
                self.app.ops_manager.mat_por_vec(
                    self.vmat,
                    self.mvec,
                )
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
            msg=f"{header}:\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
        )

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
