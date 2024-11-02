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
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    CTkTabview as ctkTabview,
)

from gauss_bot.managers.mats_manager import MatricesManager

from gauss_bot.gui.custom_frames import (
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame
)

if TYPE_CHECKING:
    from gauss_bot.gui.frames.matrices import MatricesFrame


class SumaRestaTab(CustomScrollFrame):
    """
    Frame para sumar y restar matrices.
    """

    def __init__(self, master_frame: "MatricesFrame", master_tab,
                 app, mats_manager: MatricesManager) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.input_guardians: list[ctkFrame] = []
        self.mensaje_frame: Optional[ctkFrame] = None

        self.select_1: ctkOptionMenu
        self.select_2: ctkOptionMenu
        self.resultado_suma: ctkFrame
        self.resultado_resta: ctkFrame

        self.mat1 = ""
        self.mat2 = ""

        self.tabview = ctkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="n")

        self.tab_sumar = self.tabview.add("Sumar")
        self.tab_restar = self.tabview.add("Restar")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        for tab in self.tabview.winfo_children():
            for widget in tab.winfo_children():  # type: ignore
                widget.destroy()  # type: ignore

        num_matrices = len(self.master_frame.nombres_matrices)
        self.resultado_suma = ctkFrame(self.tab_sumar)
        self.resultado_resta = ctkFrame(self.tab_restar)

        if num_matrices >= 1:
            self.setup_suma_resta(self.tab_sumar, "Sumar")
            self.setup_suma_resta(self.tab_restar, "Restar")
        if num_matrices == 0:
            for tab in self.tabview.winfo_children():
                tab.columnconfigure(0, weight=1)  # type: ignore
                no_matrices = ErrorFrame(tab, "No hay matrices guardadas!")
                no_matrices.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def setup_suma_resta(self, tab: ctkFrame, operacion: str) -> None:
        """
        Configura pestañas para sumar o restar matrices.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        tab.columnconfigure(0, weight=1)
        num_matrices = len(self.master_frame.nombres_matrices)

        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        if num_matrices == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(tab, value=self.master_frame.nombres_matrices[1])

        instruct_sr = ctkLabel(tab, text=f"Seleccione las matrices para {operacion.lower()}:")
        self.select_1 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_select1,
        )

        self.select_2 = ctkOptionMenu(
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

        instruct_sr.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.select_2.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        ejecutar_button.grid(row=3, column=0, padx=5, pady=5, sticky="n")

        if operacion == "Sumar":
            self.resultado_suma.grid(row=4, column=0, padx=5, pady=5, sticky="n")
        elif operacion == "Restar":
            self.resultado_resta.grid(row=4, column=0, padx=5, pady=5, sticky="n")

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

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.mats_manager.sumar_matrices(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_suma, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_suma, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def ejecutar_resta(self, nombre_mat1, nombre_mat2) -> None:
        """
        Resta las matrices seleccionadas.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.mats_manager.restar_matrices(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_resta, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_resta, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def update(self) -> None:
        for widget_s in self.tab_sumar.winfo_children():
            widget_s.destroy()  # type: ignore
        for widget_r in self.tab_restar.winfo_children():
            widget_r.destroy()  # type: ignore

        self.setup_tabs()
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

    def __init__(self, master_frame: "MatricesFrame", master_tab,
                 app, mats_manager: MatricesManager) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_guardians: list[ctkFrame] = []

        self.select_escalar_mat: ctkOptionMenu
        self.escalar_entry: ctkEntry
        self.select_mat1: ctkOptionMenu
        self.select_mat2: ctkOptionMenu
        self.select_mvec: ctkOptionMenu
        self.select_vmat: ctkOptionMenu

        self.escalar_mat = ""
        self.mat1 = ""
        self.mat2 = ""
        self.vmat = ""
        self.mvec = ""

        self.tabview = ctkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="n")

        self.tab_escalar = self.tabview.add("Escalar por Matriz")
        self.tab_matriz = self.tabview.add("Multiplicación Matricial")
        self.tab_matriz_vector = self.tabview.add("Producto Matriz-Vector")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        """
        Wrapper para llamar todos los métodos de configuración de tabs.
        """

        for tab in self.tabview.winfo_children():
            tab.columnconfigure(0, weight=1)  # type: ignore

        num_matrices = len(self.master_frame.nombres_matrices)
        num_vectores = len(self.master_frame.nombres_vectores)

        no_matrices_escalar = ErrorFrame(self.tab_escalar, "No hay matrices guardadas!")
        no_matrices_mult = ErrorFrame(self.tab_matriz, "No hay matrices guardadas!")
        no_matrices_vec = ErrorFrame(self.tab_matriz_vector, "No hay matrices guardadas!")
        no_vectores = ErrorFrame(self.tab_matriz_vector, "No hay vectores guardados!")
        no_mats_vecs = ErrorFrame(self.tab_matriz_vector, "No hay matrices o vectores guardados!")

        self.resultado_escalar = ctkFrame(self.tab_escalar)
        self.resultado_mats = ctkFrame(self.tab_matriz)
        self.resultado_mat_vec = ctkFrame(self.tab_matriz_vector)

        if num_matrices >= 1:
            for frame in self.input_guardians:
                if frame.master == self.tab_escalar or frame.master == self.tab_matriz:
                    frame.destroy()
                    self.input_guardians.remove(frame)
            self.setup_escalar_tab(self.tab_escalar)
            self.setup_mult_matrices_tab(self.tab_matriz)

        if num_matrices >= 1 and num_vectores >= 1:
            for frame in self.input_guardians:
                if frame.master == self.tab_matriz_vector:
                    frame.destroy()
                    self.input_guardians.remove(frame)
            self.setup_matriz_vector_tab(self.tab_matriz_vector)

        if num_matrices == 0 and num_vectores == 0:
            self.input_guardians = [
                no_matrices_escalar,
                no_matrices_mult,
                no_mats_vecs
            ]

            for frame in self.input_guardians:
                frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return
        if num_matrices == 0:
            self.input_guardians = [
                no_matrices_escalar,
                no_matrices_mult,
                no_matrices_vec
            ]

            for frame in self.input_guardians:
                frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return
        if num_vectores == 0:
            no_vectores.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.input_guardians = [no_vectores]
        self.update_scrollbar_visibility()

    def setup_escalar_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para multiplicación escalar.
        """

        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        instruct_e = ctkLabel(tab, text="Seleccione la matriz e ingrese el escalar:")
        self.select_escalar_mat = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_escalar_mat,
        )

        self.escalar_entry = ctkEntry(tab, width=60, )
        self.escalar_mat = self.select_escalar_mat.get()

        button_multiplicar = ctkButton(
            tab,
            text="Multiplicar",
            command=lambda: self.mult_por_escalar(self.escalar_mat),
        )

        instruct_e.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_escalar_mat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.escalar_entry.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        button_multiplicar.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.resultado_escalar.grid(row=4, column=0, padx=5, pady=5, sticky="n")

    def setup_mult_matrices_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para multiplicación matricial.
        """

        num_matrices = len(self.master_frame.nombres_matrices)

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        placeholder1 = placeholder2 = None
        if num_matrices > 1:
            placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
            placeholder2 = Variable(tab, value=self.master_frame.nombres_matrices[1])
        elif num_matrices == 1:
            placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
            placeholder2 = placeholder1

        instruct_ms = ctkLabel(tab, text="Seleccione las matrices para multiplicar:")
        self.select_mat1 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_mat1,
        )

        self.select_mat2 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder2,
            command=self.update_mat2,
        )

        self.mat1 = self.select_mat1.get()
        self.mat2 = self.select_mat2.get()

        button_multiplicar = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.mult_matrices(self.mat1, self.mat2),
        )

        instruct_ms.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_mat1.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.select_mat2.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        button_multiplicar.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.resultado_mats.grid(row=4, column=0, padx=5, pady=5, sticky="n")

    def setup_matriz_vector_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para producto matriz-vector.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        placeholder1 = Variable(tab, value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(tab, value=self.master_frame.nombres_vectores[0])

        instruct_mv = ctkLabel(tab, text="Seleccione la matriz y el vector para multiplicar:")
        self.select_vmat = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_vmat,
        )

        self.select_mvec = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            variable=placeholder2,
            command=self.update_mvec,
        )

        self.vmat = self.select_vmat.get()
        self.mvec = self.select_mvec.get()

        button_multiplicar = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.matriz_vector(self.vmat, self.mvec),
        )

        instruct_mv.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_vmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.select_mvec.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        button_multiplicar.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.resultado_mat_vec.grid(row=4, column=0, padx=5, pady=5, sticky="n")

    def mult_por_escalar(self, mat: str) -> None:
        """
        Realiza la multiplicación escalar de la matriz seleccionada por el escalar indicado.
        """

        mat = self.select_escalar_mat.get()  # type: ignore

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

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

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

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

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.mats_manager.mult_matricial(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_mats, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

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

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.app.ops_manager.matriz_por_vector(nombre_mat, nombre_vec)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_mat_vec, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_mat_vec, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update(self) -> None:
        for widget_e in self.tab_escalar.winfo_children():
            widget_e.destroy()  # type: ignore
        for widget_m in self.tab_matriz.winfo_children():
            widget_m.destroy()  # type: ignore
        for widget_v in self.tab_matriz_vector.winfo_children():
            widget_v.destroy()  # type: ignore

        self.setup_tabs()
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

    def __init__(self, master_frame: "MatricesFrame", master_tab,
                 app, mats_manager: MatricesManager) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        if len(self.master_frame.nombres_matrices) > 0:
            placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
        else:
            placeholder = None

        self.mensaje_frame: Optional[ctkFrame] = None
        self.instruct_t = ctkLabel(self, text="Seleccione la matriz para transponer:")

        self.select_tmat = ctkOptionMenu(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder,
            command=self.update_tmat,
        )

        self.tmat = self.select_tmat.get()

        self.button = ctkButton(
            self,
            height=30,
            text="Transponer",
            command=lambda: self.encontrar_transpuesta(self.tmat),
        )

        self.resultado = ctkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        if len(self.master_frame.nombres_matrices) == 0:
            self.mensaje_frame = ErrorFrame(
                self, "No hay matrices guardadas!"
            )
            self.rowconfigure(6, weight=1)
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.instruct_t.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_tmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def encontrar_transpuesta(self, nombre_tmat: str) -> None:
        """
        Transpone la matriz seleccionada.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        nombre_transpuesta, transpuesta = self.mats_manager.transponer_matriz(nombre_tmat)
        if not any(transpuesta == mat for mat in self.mats_manager.mats_ingresadas.values()):
            self.mats_manager.mats_ingresadas[nombre_transpuesta] = transpuesta
            self.master_frame.update_all()
            self.app.vectores.update_all()

        self.mensaje_frame = ResultadoFrame(
            self.resultado, header=f"{nombre_transpuesta}:", resultado=str(transpuesta)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update(self) -> None:
        if len(self.master_frame.nombres_matrices) > 0:
            if self.mensaje_frame is not None:
                self.mensaje_frame.destroy()
                self.mensaje_frame = None
                self.rowconfigure(6, weight=0)

            placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
            self.select_tmat.configure(
                values=self.master_frame.nombres_matrices, variable=placeholder
            )

            self.update_tmat(self.select_tmat.get())
            self.instruct_t.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.select_tmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
            self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()
        self.update_idletasks()

    def update_tmat(self, valor: str) -> None:
        self.tmat = valor


class DeterminanteTab(CustomScrollFrame):
    """
    Frame para calcular el determinante de una matriz.
    """

    def __init__(self, master_frame: "MatricesFrame", master_tab,
                 app, mats_manager: MatricesManager) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        if len(self.master_frame.nombres_matrices) > 0:
            placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
        else:
            placeholder = None

        self.mensaje_frame: Optional[ctkFrame] = None
        self.instruct_d = ctkLabel(self, text="Seleccione la matriz para calcular el determinante:")

        self.select_dmat = ctkOptionMenu(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder,
            command=self.update_dmat,
        )

        self.dmat = self.select_dmat.get()

        self.button = ctkButton(
            self,
            height=30,
            text="Calcular",
            command=lambda: self.calcular_determinante(self.dmat),
        )

        self.resultado = ctkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        if len(self.master_frame.nombres_matrices) == 0:
            self.mensaje_frame = ErrorFrame(
                self, "No hay matrices guardadas!"
            )
            self.rowconfigure(6, weight=1)
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.instruct_d.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_dmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def calcular_determinante(self, nombre_dmat: str) -> None:
        """
        Calcula el determinante de la matriz seleccionada.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

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

    def update(self) -> None:
        if len(self.master_frame.nombres_matrices) > 0:
            if self.mensaje_frame is not None:
                self.mensaje_frame.destroy()
                self.mensaje_frame = None
                self.rowconfigure(6, weight=0)

            placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
            self.select_dmat.configure(
                values=self.master_frame.nombres_matrices, variable=placeholder
            )

            self.update_dmat(self.select_dmat.get())
            self.instruct_d.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.select_dmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
            self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()
        self.update_idletasks()

    def update_dmat(self, valor: str) -> None:
        self.dmat = valor


class InversaTab(CustomScrollFrame):
    """
    Frame para encontrar la inversa de una matriz.
    """

    def __init__(self, master_frame: "MatricesFrame", master_tab,
                 app, mats_manager: MatricesManager) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None

        self.instruct_i = ctkLabel(self, text="Seleccione la matriz para encontrar su inversa:")
        self.select_imat = ctkOptionMenu(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            command=self.update_imat,
        )

        self.imat = self.select_imat.get()

        self.button = ctkButton(
            self,
            height=30,
            text="Encontrar",
            command=lambda: self.encontrar_inversa(self.imat),
        )

        self.resultado = ctkFrame(self)
        self.resultado.columnconfigure(0, weight=1)

        if len(self.master_frame.nombres_matrices) == 0:
            self.mensaje_frame = ErrorFrame(
                self, "No hay matrices guardadas!"
            )
            self.rowconfigure(6, weight=1)
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.instruct_i.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_imat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def encontrar_inversa(self, nombre_imat: str) -> None:
        """
        Encuentra la inversa de la matriz seleccionada,
        encontrando la adjunta y dividiendo por el determinante.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            nombre_inversa, inversa, _, _ = self.mats_manager.invertir_matriz(nombre_imat)
        except (ArithmeticError, ZeroDivisionError) as e:
            self.mensaje_frame = ErrorFrame(self.resultado, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            self.update_scrollbar_visibility()
            return

        if not any(inversa == mat for mat in self.mats_manager.mats_ingresadas.values()):
            self.mats_manager.mats_ingresadas[nombre_inversa] = inversa
            self.master_frame.update_all()
            self.app.vectores.update_all()

        self.mensaje_frame = ResultadoFrame(
            self.resultado,
            header=f"{nombre_inversa}:",
            resultado=str(inversa)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()

    def update(self) -> None:
        if len(self.master_frame.nombres_matrices) > 0:
            if self.mensaje_frame is not None:
                self.mensaje_frame.destroy()
                self.mensaje_frame = None
                self.rowconfigure(6, weight=0)

            placeholder = Variable(self, value=self.master_frame.nombres_matrices[0])
            self.select_imat.configure(
                values=self.master_frame.nombres_matrices, variable=placeholder
            )

            self.update_imat(self.select_imat.get())
            self.instruct_i.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.select_imat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
            self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()
        self.update_idletasks()

    def update_imat(self, valor: str) -> None:
        self.imat = valor
