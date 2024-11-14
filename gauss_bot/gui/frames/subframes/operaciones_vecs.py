"""
Implementación de todos los frames
de operaciones con vectores.
"""

from fractions import Fraction
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
    get_dict_key
)

from gauss_bot.managers import VectoresManager
from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
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

        self.mensaje_frame: Optional[ctkFrame] = None
        self.operaciones: dict[str, str] = {
            "Sumar": "+",
            "Restar": "−",
        }

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
        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(self, value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(self, value=self.master_frame.nombres_vectores[1])

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
            command=self.update_select1,
        )

        self.select_2 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_select2,
        )

        self.ejecutar_button = ctkButton(
            self,
            height=30,
            text=default,
            command=lambda: self.ejecutar_operacion(
                self.operacion, self.vec1, self.vec2
            ),
        )

        self.resultado_frame = ctkFrame(self)

        self.vec1 = self.select_1.get()
        self.vec2 = self.select_2.get()

        self.instruct_sr.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.select_operacion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_2.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.ejecutar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")
        self.resultado_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def ejecutar_operacion(self, operacion, nombre_vec1, nombre_vec2) -> None:
        """
        Suma o resta las matrices seleccionadas.
        """

        operacion = self.select_operacion.get()
        nombre_vec1 = self.select_1.get()
        nombre_vec2 = self.select_2.get()

        delete_msg_frame(self.mensaje_frame)
        try:
            if operacion == "+":
                header, resultado = self.vecs_manager.suma_resta_vecs(
                    True, nombre_vec1, nombre_vec2
                )
            elif operacion == "−":
                header, resultado = self.vecs_manager.suma_resta_vecs(
                    False, nombre_vec1, nombre_vec2
                )
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_frame, str(e))
            self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = ResultadoFrame(
            self.resultado_frame,
            header=f"{header}:",  # pylint: disable=possibly-used-before-assignment
            resultado=str(resultado)  # pylint: disable=possibly-used-before-assignment
        )
        self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def update_frame(self) -> None:
        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

        placeholder1 = Variable(self, value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(self, value=self.master_frame.nombres_vectores[1])

        self.select_1.configure(variable=placeholder1, values=self.master_frame.nombres_vectores)
        self.select_2.configure(variable=placeholder2, values=self.master_frame.nombres_vectores)

    def update_operacion(self, valor: str) -> None:
        self.operacion = valor
        op_text: str = get_dict_key(self.operaciones, valor)  # type: ignore
        self.instruct_sr.configure(text=f"Seleccione las matrices a {op_text.lower()}:")
        self.ejecutar_button.configure(text=op_text)

    def update_select1(self, valor: str) -> None:
        self.vec1 = valor

    def update_select2(self, valor: str) -> None:
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

        self.mensaje_frame: Optional[ctkFrame] = None
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

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.tab_escalar = self.tabview.add("Escalar por Vector")
        self.tab_vector = self.tabview.add("Producto Punto")
        self.tab_matriz_vector = self.tabview.add("Producto Matriz-Vector")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        """
        Wrapper para llamar todos los métodos de configuración de tabs.
        """

        delete_msg_frame(self.mensaje_frame)
        for widget in self.tab_matriz_vector.winfo_children():
            widget.destroy()  # type: ignore

        for tab in self.tabview.winfo_children():
            tab.columnconfigure(0, weight=1)  # type: ignore
            tab.columnconfigure(2, weight=1)  # type: ignore

        num_matrices = len(self.master_frame.nombres_matrices)
        self.resultado_escalar = ctkFrame(self.tab_escalar)
        self.resultado_vectores = ctkFrame(self.tab_vector)
        self.resultado_mat_vec = ctkFrame(self.tab_matriz_vector)

        self.setup_escalar_tab(self.tab_escalar)
        self.setup_vector_tab(self.tab_vector)

        if num_matrices >= 1:
            self.setup_matriz_vector_tab(self.tab_matriz_vector)
        else:
            self.mensaje_frame = ErrorFrame(self.tab_matriz_vector, "No hay matrices guardadas!")
            agregar_button = ctkButton(
                self.tab_matriz_vector,
                height=30,
                text="Agregar matrices",
                image=INPUTS_ICON,
                command=lambda: self.app.home_frame.ir_a_matriz(mostrar=False),  # type: ignore
            )

            self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
            agregar_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_escalar_tab(self, tab: ctkFrame) -> None:
        """
        Setup de la tab para multiplicar un vector por un escalar.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(tab, value=self.master_frame.nombres_vectores[0])
        instruct_e = ctkLabel(tab, text="Seleccione el vector e ingrese el escalar:")
        operador_label = ctkLabel(tab, text="•")
        operador_label._font.configure(size=16)

        self.select_escalar_vec = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder1,
            command=self.update_escalar_vec,
        )

        self.escalar_vec = self.select_escalar_vec.get()
        self.escalar_entry = CustomEntry(tab, width=60)
        self.escalar_entry.bind("<Return>", lambda _: self.mult_por_escalar(self.escalar_vec))

        multiplicar_button = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.mult_por_escalar(self.escalar_vec),
        )

        instruct_e.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        self.escalar_entry.grid(row=1, column=0, ipadx=5, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_escalar_vec.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")
        self.resultado_escalar.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_vector_tab(self, tab: ctkFrame) -> None:
        """
        Setup de la tab para multiplicar vectores.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(tab, value=self.master_frame.nombres_vectores[0])
        if len(self.master_frame.nombres_vectores) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(tab, value=self.master_frame.nombres_vectores[1])

        instruct_v = ctkLabel(tab, text="Seleccione los vectores a multiplicar:")
        operador_label = ctkLabel(tab, text=".")
        operador_label._font.configure(size=16)

        self.select_vec1 = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder1,
            command=self.update_vec1,
        )

        self.select_vec2 = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_vec2,
        )

        self.vec1 = self.select_vec1.get()
        self.vec2 = self.select_vec2.get()

        multiplicar_button = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.prod_punto(self.vec1, self.vec2),
        )

        instruct_v.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        self.select_vec1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_vec2.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")
        self.resultado_vectores.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_matriz_vector_tab(self, tab: ctkFrame) -> None:
        """
        Setup de la tab para multiplicar matrices y vectores.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(tab, value=self.master_frame.nombres_vectores[0])

        instruct_mv = ctkLabel(tab, text="Seleccione la matriz y el vector a multiplicar:")
        operador_label = ctkLabel(tab, text="•")
        operador_label._font.configure(size=16)

        self.select_vmat = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_vmat,
        )

        self.select_mvec = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_mvec,
        )

        self.vmat = self.select_vmat.get()
        self.mvec = self.select_mvec.get()

        multiplicar_button = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.matriz_vector(self.vmat, self.mvec),
        )

        instruct_mv.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        self.select_vmat.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mvec.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")
        self.resultado_mat_vec.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def mult_por_escalar(self, vec: str) -> None:
        """
        Realiza la multiplicación de un vector por un escalar.
        """

        vec = self.select_escalar_vec.get()  # type: ignore

        try:
            if self.mensaje_frame.parent in (  # type: ignore
                self.tab_escalar,
                self.resultado_escalar,
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            pass

        try:
            escalar = Fraction(self.escalar_entry.get())  # type: ignore
            header, resultado = self.vecs_manager.escalar_por_vector(escalar, vec)
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self.resultado_escalar, "El escalar debe ser un número racional!"
            )
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return
        except ZeroDivisionError:
            self.mensaje_frame = ErrorFrame(
                self.resultado_escalar, "El denominador no puede ser 0!"
            )
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        try:
            if self.mensaje_frame.parent in (  # type: ignore
                self.tab_escalar,
                self.resultado_escalar,
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            pass

        self.mensaje_frame = ResultadoFrame(
            self.resultado_escalar, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def prod_punto(self, nombre_vec1: str, nombre_vec2: str) -> None:
        """
        Realiza el producto punto de dos vectores.
        """

        nombre_vec1 = self.select_vec1.get()  # type: ignore
        nombre_vec2 = self.select_vec2.get()  # type: ignore

        try:
            if self.mensaje_frame.parent in (  # type: ignore
                self.tab_vector,
                self.resultado_vectores,
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            pass

        try:
            header, resultado = self.vecs_manager.producto_punto(nombre_vec1, nombre_vec2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_vectores, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        try:
            if self.mensaje_frame.parent in (  # type: ignore
                self.tab_vector,
                self.resultado_vectores,
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            pass

        self.mensaje_frame = ResultadoFrame(
            self.resultado_vectores, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def matriz_vector(self, nombre_mat: str, nombre_vec: str) -> None:
        """
        Realiza el producto de una matriz por un vector.
        """

        nombre_mat = self.select_vmat.get()  # type: ignore
        nombre_vec = self.select_mvec.get()  # type: ignore

        try:
            if self.mensaje_frame.parent in (  # type: ignore
                self.tab_matriz_vector,
                self.resultado_mat_vec,
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            pass

        try:
            header, resultado = self.app.ops_manager.matriz_por_vector(  # type: ignore
                nombre_mat, nombre_vec
            )
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_mat_vec, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        try:
            if self.mensaje_frame.parent in (  # type: ignore
                self.tab_matriz_vector,
                self.resultado_mat_vec,
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            pass

        self.mensaje_frame = ResultadoFrame(
            self.resultado_mat_vec, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def update_frame(self) -> None:
        self.setup_tabs()
        self.tabview.configure(bg_color="transparent")
        self.tabview.configure(fg_color="transparent")

    def update_escalar_vec(self, valor: str) -> None:
        self.escalar_vec = valor

    def update_vec1(self, valor: str) -> None:
        self.vec1 = valor

    def update_vec2(self, valor: str) -> None:
        self.vec2 = valor

    def update_vmat(self, valor: str) -> None:
        self.vmat = valor

    def update_mvec(self, valor: str) -> None:
        self.mvec = valor
