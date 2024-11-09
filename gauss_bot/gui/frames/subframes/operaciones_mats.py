"""
Implementación de todos los frames
de operaciones con matrices.
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

from gauss_bot import delete_msg_frame
from gauss_bot.managers import MatricesManager
from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import MatricesFrame


class SumaRestaTab(CustomScrollFrame):
    """
    Frame para sumar y restar matrices.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_1: CustomDropdown
        self.select_2: CustomDropdown
        self.resultado_suma: ctkFrame
        self.resultado_resta: ctkFrame

        self.mat1 = ""
        self.mat2 = ""

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        for tab in self.tabview.winfo_children():
            for widget in tab.winfo_children():  # type: ignore
                widget.destroy()  # type: ignore

        self.tab_sumar = self.tabview.add("Sumar")
        self.tab_restar = self.tabview.add("Restar")

        self.resultado_suma = ctkFrame(self.tab_sumar)
        self.resultado_resta = ctkFrame(self.tab_restar)

        self.setup_suma_resta(self.tab_sumar, "Sumar")
        self.setup_suma_resta(self.tab_restar, "Restar")

    def setup_suma_resta(self, tab: ctkFrame, operacion: str) -> None:
        """
        Configura pestañas para sumar o restar matrices.
        """

        delete_msg_frame(self.mensaje_frame)
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(2, weight=1)

        if operacion == "Sumar":
            operador = "+"
        elif operacion == "Restar":
            operador = "−"

        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        if len(self.master_frame.nombres_matrices) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(tab, value=self.master_frame.nombres_matrices[1])

        instruct_sr = ctkLabel(tab, text=f"Seleccione las matrices a {operacion.lower()}:")
        operador_label = ctkLabel(tab, text=operador)
        operador_label._font.configure(size=16)

        self.select_1 = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_select1,
        )

        self.select_2 = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder2,
            command=self.update_select2,
        )

        ejecutar_button = ctkButton(
            tab,
            height=30,
            text=operacion,
            command=lambda: self.ejecutar_operacion(operacion, self.mat1, self.mat2),
        )

        self.mat1 = self.select_1.get()
        self.mat2 = self.select_2.get()

        instruct_sr.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_2.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ejecutar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")

        if operacion == "Sumar":
            self.resultado_suma.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        elif operacion == "Restar":
            self.resultado_resta.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def ejecutar_operacion(self, operacion, nombre_mat1, nombre_mat2) -> None:
        """
        Suma o resta las matrices seleccionadas.
        """

        nombre_mat1 = self.select_1.get()
        nombre_mat2 = self.select_2.get()

        if operacion == "Sumar":
            self.ejecutar_suma(nombre_mat1, nombre_mat2)
        if operacion == "Restar":
            self.ejecutar_resta(nombre_mat1, nombre_mat2)
        self.update_scrollbar_visibility()

    def ejecutar_suma(self, nombre_mat1, nombre_mat2) -> None:
        """
        Suma las matrices seleccionadas.
        """

        delete_msg_frame(self.mensaje_frame)
        try:
            header, resultado = self.mats_manager.sumar_matrices(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_suma, str(e))
            self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = ResultadoFrame(
            self.resultado_suma, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def ejecutar_resta(self, nombre_mat1, nombre_mat2) -> None:
        """
        Resta las matrices seleccionadas.
        """

        delete_msg_frame(self.mensaje_frame)
        try:
            header, resultado = self.mats_manager.restar_matrices(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_resta, str(e))
            self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = ResultadoFrame(
            self.resultado_resta, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def update_frame(self) -> None:
        for tab in self.tabview.winfo_children():
            for widget in tab.winfo_children():
                widget.destroy()

        self.setup_tabs()
        self.tabview.configure(bg_color="transparent")
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()

    def update_select1(self, valor: str) -> None:
        self.mat1 = valor

    def update_select2(self, valor: str) -> None:
        self.mat2 = valor


class MultiplicacionTab(CustomScrollFrame):
    """
    Frame para realizar multiplicación escalar,
    multiplicación matricial y producto matriz-vector.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_escalar_mat: CustomDropdown
        self.escalar_entry: CustomEntry
        self.select_mat1: CustomDropdown
        self.select_mat2: CustomDropdown
        self.select_mvec: CustomDropdown
        self.select_vmat: CustomDropdown

        self.escalar_mat = ""
        self.mat1 = ""
        self.mat2 = ""
        self.vmat = ""
        self.mvec = ""

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.tab_escalar = self.tabview.add("Escalar por Matriz")
        self.tab_matriz = self.tabview.add("Multiplicación Matricial")
        self.tab_matriz_vector = self.tabview.add("Producto Matriz-Vector")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        """
        Wrapper para llamar todos los métodos de configuración de tabs.
        """

        delete_msg_frame(self.mensaje_frame)
        for tab in self.tabview.winfo_children():
            tab.columnconfigure(0, weight=1)  # type: ignore
            tab.columnconfigure(2, weight=1)  # type: ignore

        num_vectores = len(self.master_frame.nombres_vectores)
        self.resultado_escalar = ctkFrame(self.tab_escalar)
        self.resultado_mats = ctkFrame(self.tab_matriz)
        self.resultado_mat_vec = ctkFrame(self.tab_matriz_vector)

        self.setup_escalar_tab(self.tab_escalar)
        self.setup_mult_matrices_tab(self.tab_matriz)

        if num_vectores == 0:
            self.mensaje_frame = ErrorFrame(self.tab_matriz_vector, "No hay vectores guardados!")
            self.mensaje_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_escalar_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para multiplicación escalar.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])

        instruct_e = ctkLabel(tab, text="Seleccione la matriz e ingrese el escalar:")
        operador_label = ctkLabel(tab, text="*")
        operador_label._font.configure(size=16)

        self.select_escalar_mat = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_escalar_mat,
        )

        self.escalar_mat = self.select_escalar_mat.get()
        self.escalar_entry = CustomEntry(tab, width=60)
        self.escalar_entry.bind("<Return>", lambda _: self.mult_por_escalar(self.escalar_mat))

        multiplicar_button = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.mult_por_escalar(self.escalar_mat),
        )

        instruct_e.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        self.escalar_entry.grid(row=1, column=0, ipadx=5, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=3, pady=5, sticky="ew")
        self.select_escalar_mat.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")
        self.resultado_escalar.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_mult_matrices_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para multiplicación matricial.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        if len(self.master_frame.nombres_matrices) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(tab, value=self.master_frame.nombres_matrices[1])

        instruct_ms = ctkLabel(tab, text="Seleccione las matrices para multiplicar:")
        operador_label = ctkLabel(tab, text="*")
        operador_label._font.configure(size=16)

        self.select_mat1 = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_mat1,
        )

        self.select_mat2 = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder2,
            command=self.update_mat2,
        )

        self.mat1 = self.select_mat1.get()
        self.mat2 = self.select_mat2.get()

        multiplicar_button = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.mult_matrices(self.mat1, self.mat2),
        )

        instruct_ms.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")

        self.select_mat1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mat2.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="n")
        self.resultado_mats.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def setup_matriz_vector_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para producto matriz-vector.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(tab, value=self.master_frame.nombres_vectores[0])

        instruct_mv = ctkLabel(tab, text="Seleccione la matriz y el vector para multiplicar:")
        operador_label = ctkLabel(tab, text="*")
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

    def mult_por_escalar(self, mat: str) -> None:
        """
        Realiza la multiplicación escalar de la matriz seleccionada por el escalar indicado.
        """

        mat = self.select_escalar_mat.get()  # type: ignore

        delete_msg_frame(self.mensaje_frame)
        try:
            escalar = Fraction(self.escalar_entry.get())  # type: ignore
            header, resultado = self.mats_manager.escalar_por_matriz(escalar, mat)
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self.resultado_escalar, "El escalar debe ser un número racional!"
            )
            self.update_scrollbar_visibility()
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return
        except ZeroDivisionError:
            self.mensaje_frame = ErrorFrame(
                self.resultado_escalar, "El denominador no puede ser 0!"
            )
            self.update_scrollbar_visibility()
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = ResultadoFrame(
            self.resultado_escalar, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def mult_matrices(self, nombre_mat1: str, nombre_mat2: str) -> None:
        """
        Realiza la multiplicación matricial de las matrices seleccionadas.
        """

        nombre_mat1 = self.select_mat1.get()  # type: ignore
        nombre_mat2 = self.select_mat2.get()  # type: ignore

        delete_msg_frame(self.mensaje_frame)
        try:
            header, resultado = self.mats_manager.mult_matricial(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_mats, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = ResultadoFrame(
            self.resultado_mats, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def matriz_vector(self, nombre_mat: str, nombre_vec: str) -> None:
        """
        Realiza el producto matriz-vector de la matriz y el vector seleccionados.
        """

        nombre_mat = self.select_vmat.get()  # type: ignore
        nombre_vec = self.select_mvec.get()  # type: ignore

        delete_msg_frame(self.mensaje_frame)
        try:
            header, resultado = self.app.ops_manager.matriz_por_vector(nombre_mat, nombre_vec)  # type: ignore
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_mat_vec, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = ResultadoFrame(
            self.resultado_mat_vec, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update_frame(self) -> None:
        for tab in self.tabview.winfo_children():
            for widget in tab.winfo_children():
                widget.destroy()

        self.setup_tabs()
        self.tabview.configure(bg_color="transparent")
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()

    def update_escalar_mat(self, valor: str) -> None:
        self.escalar_mat = valor

    def update_mat1(self, valor: str) -> None:
        self.mat1 = valor

    def update_mat2(self, valor: str) -> None:
        self.mat2 = valor

    def update_vmat(self, valor: str) -> None:
        self.vmat = valor

    def update_mvec(self, valor: str) -> None:
        self.mvec = valor


class TransposicionTab(CustomScrollFrame):
    """
    Frame para transponer una matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_tmat: CustomDropdown
        self.tmat = ""
        self.resultado: ctkFrame

        self.setup_frame()

    def setup_frame(self) -> None:
        delete_msg_frame(self.mensaje_frame)
        placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
        instruct_t = ctkLabel(self, text="Seleccione una matriz para transponer:")

        self.select_tmat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder,
            command=self.update_tmat,
        )

        self.tmat = self.select_tmat.get()

        button = ctkButton(
            self,
            height=30,
            text="Transponer",
            command=lambda: self.encontrar_transpuesta(self.tmat),
        )

        self.resultado = ctkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        instruct_t.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_tmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def encontrar_transpuesta(self, nombre_tmat: str) -> None:
        """
        Transpone la matriz seleccionada.
        """

        delete_msg_frame(self.mensaje_frame)
        nombre_transpuesta, transpuesta = self.mats_manager.transponer_matriz(nombre_tmat)
        if not any(transpuesta == mat for mat in self.mats_manager.mats_ingresadas.values()):
            self.mats_manager.mats_ingresadas[nombre_transpuesta] = transpuesta
            self.app.inputs_frame.instances[0].update_all()  # type: ignore
            self.master_frame.update_all()
            self.app.vectores.update_all()  # type: ignore

        self.mensaje_frame = ResultadoFrame(
            self.resultado, header=f"{nombre_transpuesta}:", resultado=str(transpuesta)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update_frame(self) -> None:
        self.update_idletasks()
        self.setup_frame()
        self.update_idletasks()

    def update_tmat(self, valor: str) -> None:
        self.tmat = valor


class DeterminanteTab(CustomScrollFrame):
    """
    Frame para calcular el determinante de una matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_dmat: CustomDropdown
        self.dmat = ""
        self.resultado: ctkFrame

        self.setup_frame()

    def setup_frame(self) -> None:
        delete_msg_frame(self.mensaje_frame)
        placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
        instruct_d = ctkLabel(self, text="Seleccione una matriz para calcular su determinante:")

        self.select_dmat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder,
            command=self.update_dmat,
        )

        self.dmat = self.select_dmat.get()

        button = ctkButton(
            self,
            height=30,
            text="Calcular",
            command=lambda: self.calcular_determinante(self.dmat),
        )

        self.resultado = ctkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        instruct_d.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_dmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def calcular_determinante(self, nombre_dmat: str) -> None:
        """
        Calcula el determinante de la matriz seleccionada.
        """

        delete_msg_frame(self.mensaje_frame)
        dmat = self.mats_manager.mats_ingresadas[nombre_dmat]
        try:
            if dmat.filas == 1 and dmat.columnas == 1:
                det = dmat[0, 0]
            elif dmat.filas == 2 and dmat.columnas == 2:
                det = dmat.calcular_det()  # type: ignore
            else:
                det, _, _ = dmat.calcular_det()  # type: ignore
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        self.mensaje_frame = ResultadoFrame(
            self.resultado,
            header=f"| {nombre_dmat} | = {det}",
            resultado="",
            solo_header=True,
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update_frame(self) -> None:
        self.update_idletasks()
        self.setup_frame()
        self.update_idletasks()

    def update_dmat(self, valor: str) -> None:
        self.dmat = valor


class InversaTab(CustomScrollFrame):
    """
    Frame para encontrar la inversa de una matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "MatricesFrame",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_imat: CustomDropdown
        self.imat = ""
        self.resultado: ctkFrame

        self.setup_frame()

    def setup_frame(self) -> None:
        delete_msg_frame(self.mensaje_frame)
        placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
        instruct_i = ctkLabel(self, text="Seleccione una matriz para encontrar su inversa:")

        self.select_imat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder,
            command=self.update_imat,
        )

        self.imat = self.select_imat.get()

        button = ctkButton(
            self,
            height=30,
            text="Encontrar",
            command=lambda: self.encontrar_inversa(self.imat),
        )

        self.resultado = ctkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        instruct_i.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_imat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def encontrar_inversa(self, nombre_imat: str) -> None:
        """
        Encuentra la inversa de la matriz seleccionada,
        encontrando la adjunta y dividiendo por el determinante.
        """

        delete_msg_frame(self.mensaje_frame)
        try:
            nombre_inversa, inversa, _, _ = self.mats_manager.invertir_matriz(nombre_imat)
        except (ArithmeticError, ZeroDivisionError) as e:
            self.mensaje_frame = ErrorFrame(self.resultado, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        if not any(inversa == mat for mat in self.mats_manager.mats_ingresadas.values()):
            self.mats_manager.mats_ingresadas[nombre_inversa] = inversa
            self.app.inputs_frame.instances[0].update_all()  # type: ignore
            self.master_frame.update_all()
            self.app.vectores.update_all()  # type: ignore

        self.mensaje_frame = ResultadoFrame(
            self.resultado,
            header=f"{nombre_inversa}:",
            resultado=str(inversa)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update_frame(self) -> None:
        self.update_idletasks()
        self.setup_frame()
        self.update_idletasks()

    def update_imat(self, valor: str) -> None:
        self.imat = valor
