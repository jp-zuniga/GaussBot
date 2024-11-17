# pylint: disable=too-many-lines
# mas corto no lo puedo hacer sin perder legibilidad

"""
Implementación de todos los frames
de operaciones con matrices.
"""

from fractions import Fraction
from random import randint
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
    get_dict_key,
)

from gauss_bot.managers import MatricesManager
from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    place_msg_frame,
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
        self.columnconfigure(2, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.operaciones: dict[str, str] = {
            "Sumar": "+",
            "Restar": "−",
        }

        # definir atributos; se inicializan en setup_frame
        self.instruct_sr: ctkLabel
        self.select_operacion: CustomDropdown
        self.select_1: CustomDropdown
        self.select_2: CustomDropdown
        self.ejecutar_button: ctkButton
        self.resultado_frame: ctkFrame

        self.operacion = "Sumar"
        self.mat1 = ""
        self.mat2 = ""

        self.setup_frame()

    def setup_frame(self, default: str = "Sumar") -> None:
        """
        Inicializa el frame y sus atributos.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(
            self, value=self.master_frame.nombres_matrices[0]
        )

        if len(self.master_frame.nombres_matrices) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(
                self,
                value=self.master_frame.nombres_matrices[1]
            )

        # crear widgets
        self.instruct_sr = ctkLabel(
            self,
            text=f"Seleccione las matrices a {default.lower()}:"
        )

        self.select_operacion = CustomDropdown(
            self,
            width=40,
            font=("Roboto", 18),
            values=list(self.operaciones.values()),
            variable=Variable(value=self.operaciones[default]),
            command=self.update_operacion,
        )

        self.select_1 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder1,
            command=self.update_select1,
        )

        self.select_2 = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=placeholder2,
            command=self.update_select2,
        )

        self.mat1 = self.select_1.get()
        self.mat2 = self.select_2.get()
        self.ejecutar_button = ctkButton(
            self,
            height=30,
            text=default,
            command=lambda: self.ejecutar_operacion(self.operacion),
        )

        self.resultado_frame = ctkFrame(self, fg_color="transparent")

        # colocar widgets
        self.instruct_sr.grid(
            row=0, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
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

        self.resultado_frame.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

    def ejecutar_operacion(self, operacion) -> None:
        """
        Suma o resta las matrices seleccionadas.
        """

        operacion = self.select_operacion.get()
        nombre_mat1 = self.select_1.get()
        nombre_mat2 = self.select_2.get()

        delete_msg_frame(self.mensaje_frame)
        try:
            if operacion == "+":
                header, resultado = self.mats_manager.suma_resta_mats(
                    True,
                    nombre_mat1,
                    nombre_mat2,
                )
            elif operacion == "−":
                header, resultado = self.mats_manager.suma_resta_mats(
                    False,
                    nombre_mat1,
                    nombre_mat2,
                )
        except ArithmeticError as e:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self.resultado_frame,
                msg_frame=self.mensaje_frame,
                msg=str(e),
                tipo="error",
                columnspan=3,
            )
            return
        delete_msg_frame(self.mensaje_frame)

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado_frame,
            msg_frame=self.mensaje_frame,
            msg=f"{header}:\n\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
            columnspan=3,
        )

    def update_frame(self) -> None:
        """
        Actualiza todos los backgrounds y valores de los dropdowns.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

        placeholder1 = Variable(self, value=self.master_frame.nombres_matrices[0])
        if len(self.master_frame.nombres_matrices) == 1:
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(
                self, value=self.master_frame.nombres_matrices[1],
            )

        self.select_1.configure(
            variable=placeholder1,
            values=self.master_frame.nombres_matrices,
        )

        self.select_2.configure(
            variable=placeholder2,
            values=self.master_frame.nombres_matrices,
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

    def update_select1(self, valor: str) -> None:
        """
        Actualiza el valor de self.mat1 con el
        valor seleccionado en el dropdown correspondiente.
        """

        self.mat1 = valor

    def update_select2(self, valor: str) -> None:
        """
        Actualiza el valor de self.mat2 con el
        valor seleccionado en el dropdown correspondiente.
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

        # definir atributos; se inicializan en setup_tabs
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

        self.tabview = ctkTabview(self, fg_color="transparent")
        self.tabview.pack(expand=True, fill="both")

        # crear tabs
        self.tab_escalar = self.tabview.add("Escalar por Matriz")
        self.tab_matriz = self.tabview.add("Multiplicación Matricial")
        self.tab_matriz_vector = self.tabview.add("Matriz por Vector")
        self.setup_tabs()

    def setup_tabs(self) -> None:
        """
        Wrapper para llamar todos los métodos de configuración de tabs.
        Se encarga de validar si hay vectores ingresados para que
        los setups individuales no lo tengan que hacer.
        """

        for tab in self.tabview.winfo_children():
            tab.columnconfigure(0, weight=1)  # type: ignore
            tab.columnconfigure(2, weight=1)  # type: ignore

        # crear frames de resultado
        self.resultado_escalar = ctkFrame(self.tab_escalar, fg_color="transparent")
        self.resultado_mats = ctkFrame(self.tab_matriz, fg_color="transparent")
        self.resultado_mat_vec = ctkFrame(
            self.tab_matriz_vector, fg_color="transparent"
        )

        self.setup_escalar_tab(self.tab_escalar)
        self.setup_mult_matrices_tab(self.tab_matriz)

        if len(self.master_frame.nombres_vectores) >= 1:
            self.setup_matriz_vector_tab(self.tab_matriz_vector)
        else:
            # si no hay vectores, informar al usuario,
            self.mensaje_frame = place_msg_frame(
                parent_frame=self.tab_matriz_vector,
                msg_frame=self.mensaje_frame,
                msg="No hay vectores guardados!",
                tipo="error",
                columnspan=3,
            )

            # y dirigirlos al menu de datos para agregar vectores
            ctkButton(
                self.tab_matriz_vector,
                height=30,
                text="Agregar vectores",
                image=INPUTS_ICON,
                command=lambda: self.app.home_frame.ir_a_vector(mostrar=False),  # type: ignore
            ).grid(
                row=1, column=0,
                columnspan=3,
                padx=5, pady=5,
                sticky="n",
            )

    def setup_escalar_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para multiplicación escalar.
        """

        # crear widgets
        operador_label = ctkLabel(tab, text="•", font=("Roboto", 18))
        instruct_e = ctkLabel(
            tab,
            text="Seleccione la matriz e ingrese el escalar:",
        )

        self.select_escalar_mat = CustomDropdown(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_escalar_mat,
        )

        self.escalar_mat = self.select_escalar_mat.get()
        self.escalar_entry = CustomEntry(
            tab, width=60,
            placeholder_text=randint(-10, 10)
        )

        self.escalar_entry.bind(
            "<Return>",
            lambda _: self.mult_por_escalar(self.escalar_mat)
        )

        multiplicar_button = ctkButton(
            tab,
            height=30,
            text="Multiplicar",
            command=lambda: self.mult_por_escalar(self.escalar_mat),
        )

        # colocar widgets
        instruct_e.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.escalar_entry.grid(row=1, column=0, ipadx=5, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=3, pady=5, sticky="ew")
        self.select_escalar_mat.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(
            row=2, column=0,
            columnspan=3,
            padx=5, pady=10,
            sticky="n",
        )

        self.resultado_escalar.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

    def setup_mult_matrices_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para multiplicación matricial.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        if len(self.master_frame.nombres_matrices) == 1:
            # si solo hay una matriz, ocupar el mismo placeholder
            placeholder2 = placeholder1
        else:
            placeholder2 = Variable(value=self.master_frame.nombres_matrices[1])

        # crear widgets
        operador_label = ctkLabel(tab, text="•", font=("Roboto", 18))
        instruct_ms = ctkLabel(
            tab,
            text="Seleccione las matrices a multiplicar:",
        )

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

        # colocar widgets
        instruct_ms.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
        self.select_mat1.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        operador_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.select_mat2.grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )

        multiplicar_button.grid(
            row=2, column=0,
            columnspan=3,
            padx=5, pady=10,
            sticky="n",
        )

        self.resultado_mats.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

    def setup_matriz_vector_tab(self, tab: ctkFrame) -> None:
        """
        Configura la pestaña para producto matriz-vector.
        """

        delete_msg_frame(self.mensaje_frame)
        placeholder1 = Variable(value=self.master_frame.nombres_matrices[0])
        placeholder2 = Variable(value=self.master_frame.nombres_vectores[0])

        # crear widgets
        operador_label = ctkLabel(tab, text="•", font=("Roboto", 18))
        instruct_mv = ctkLabel(
            tab,
            text="Seleccione la matriz y el vector a multiplicar:",
        )

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

        self.resultado_mat_vec.grid(
            row=3, column=0,
            columnspan=3,
            padx=5, pady=5,
            sticky="n",
        )

    def mult_por_escalar(self, mat: str) -> None:
        """
        Realiza la multiplicación escalar de la
        matriz seleccionada por el escalar indicado.
        """

        mat = self.select_escalar_mat.get()  # type: ignore

        self.delete_msg_if(self.tab_escalar, self.resultado_escalar)
        try:
            escalar = Fraction(self.escalar_entry.get())  # type: ignore
            header, resultado = self.mats_manager.escalar_por_mat(escalar, mat)
        except (ValueError, ZeroDivisionError) as e:
            if isinstance(e, ValueError):
                msg = "El escalar debe ser un número racional!"
            else:
                msg = "El denominador no puede ser 0!"
            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg=msg,
                tipo="error",
                row=3,
            )
            return
        self.delete_msg_if(self.tab_escalar, self.resultado_escalar)

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado_escalar,
            msg_frame=self.mensaje_frame,
            msg=f"{header}:\n\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
            columnspan=3,
        )

    def mult_matrices(self, nombre_mat1: str, nombre_mat2: str) -> None:
        """
        Realiza la multiplicación matricial de las matrices seleccionadas.
        """

        nombre_mat1 = self.select_mat1.get()  # type: ignore
        nombre_mat2 = self.select_mat2.get()  # type: ignore

        self.delete_msg_if(self.tab_matriz, self.resultado_mats)
        try:
            header, resultado = self.mats_manager.mult_mats(nombre_mat1, nombre_mat2)
        except ArithmeticError as e:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg=str(e),
                tipo="error",
                row=3,
            )
            return
        self.delete_msg_if(self.tab_matriz, self.resultado_mats)

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado_mats,
            msg_frame=self.mensaje_frame,
            msg=f"{header}:\n\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
            columnspan=3,
        )

    def matriz_vector(self, nombre_mat: str, nombre_vec: str) -> None:
        """
        Realiza el producto matriz-vector de la matriz y el vector seleccionados.
        """

        nombre_mat = self.select_vmat.get()  # type: ignore
        nombre_vec = self.select_mvec.get()  # type: ignore

        self.delete_msg_if(self.tab_matriz_vector, self.resultado_mat_vec)
        try:
            header, resultado = self.app.ops_manager.mat_por_vec(  # type: ignore
                nombre_mat, nombre_vec
            )
        except ArithmeticError as e:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg=str(e),
                tipo="error",
                row=3,
            )
            return
        self.delete_msg_if(self.tab_matriz_vector, self.resultado_mat_vec)

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado_mat_vec,
            msg_frame=self.mensaje_frame,
            msg=f"{header}:\n\n{str(resultado)}",  # pylint: disable=E0606
            tipo="resultado",
            columnspan=3,
        )

    def delete_msg_if(self, tab: ctkFrame, frame: ctkFrame) -> None:
        """
        Llama delete_msg_frame() si self.mensaje_frame
        esta colocado en uno de los frames indicados.
        """

        try:
            if (
                self.mensaje_frame.master  # type: ignore
                in (tab, frame)
            ):
                delete_msg_frame(self.mensaje_frame)
        except AttributeError:
            # si self.mensaje_frame == None,
            # el .master va a tirar error
            pass

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

    def update_escalar_mat(self, valor: str) -> None:
        """
        Actualiza el valor de self.escalar_mat con
        el valor seleccionado en el dropdown.
        """

        self.escalar_mat = valor

    def update_mat1(self, valor: str) -> None:
        """
        Actualiza el valor de self.mat1 con
        el valor seleccionado en el dropdown.
        """

        self.mat1 = valor

    def update_mat2(self, valor: str) -> None:
        """
        Actualiza el valor de self.mat2 con
        el valor seleccionado en el dropdown.
        """

        self.mat2 = valor

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

        # definir atributos, inicializados en setup_frame()
        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_tmat: CustomDropdown
        self.tmat = ""
        self.resultado: ctkFrame

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializa todas las widgets y las configura.
        """

        delete_msg_frame(self.mensaje_frame)
        instruct_t = ctkLabel(self, text="Seleccione la matriz a transponer:")

        self.select_tmat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_tmat,
        )

        self.tmat = self.select_tmat.get()
        button = ctkButton(
            self,
            height=30,
            text="Transponer",
            command=self.encontrar_transpuesta,
        )

        self.resultado = ctkFrame(self, fg_color="transparent")
        self.resultado.columnconfigure(0, weight=1)

        instruct_t.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_tmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def encontrar_transpuesta(self) -> None:
        """
        Transpone la matriz seleccionada.
        """

        delete_msg_frame(self.mensaje_frame)
        self.update_tmat(self.select_tmat.get())
        nombre_transpuesta, transpuesta = (
            self.mats_manager.transponer_mat(self.tmat)
        )

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.mensaje_frame,
            msg=f"{nombre_transpuesta}:\n\n{str(transpuesta)}",
            tipo="resultado",
            columnspan=3,
        )

        # si la transposicion no esta guardada,
        # agregarla y mandar a actualizar los datos
        if not any(
            transpuesta == mat
            for mat in self.mats_manager.mats_ingresadas.values()
        ):
            self.mats_manager.mats_ingresadas[nombre_transpuesta] = transpuesta
            self.master_frame.update_all()
            self.app.vectores.update_all()  # type: ignore
            self.app.inputs_frame.instances[1].update_all()  # type: ignore


    def update_frame(self) -> None:
        """
        Actualiza los valores del dropdown.
        """

        self.select_tmat.configure(
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            values=self.master_frame.nombres_matrices,
        )

    def update_tmat(self, valor: str) -> None:
        """
        Actualiza self.tmat con el valor
        seleccionado en el dropdown.
        """

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

        # definir atributos, inicalizados en setup_frame()
        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_dmat: CustomDropdown
        self.dmat = ""
        self.resultado: ctkFrame

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializa y configura los widgets del frame.
        """

        delete_msg_frame(self.mensaje_frame)
        instruct_d = ctkLabel(
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

    def calcular_determinante(self, nombre_dmat: str) -> None:
        """
        Calcula el determinante de la matriz seleccionada.
        """

        delete_msg_frame(self.mensaje_frame)
        dmat = self.mats_manager.mats_ingresadas[nombre_dmat]
        try:
            if dmat.filas <= 2 and dmat.columnas <= 2:
                det = dmat.calcular_det()  # type: ignore
            else:
                det, _, _ = dmat.calcular_det()  # type: ignore
        except ArithmeticError as e:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self.resultado,
                msg_frame=self.mensaje_frame,
                msg=str(e),
                tipo="error",
            )
            return

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.mensaje_frame,
            msg=f"| {nombre_dmat} | = {det}",
            tipo="resultado",
        )

    def update_frame(self) -> None:
        """
        Actualiza los valores del dropdown.
        """

        self.select_dmat.configure(
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            values=self.master_frame.nombres_matrices,
        )

    def update_dmat(self, valor: str) -> None:
        """
        Actualiza self.dmat con el valor
        seleccionado en el dropdown.
        """

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

        # definir atributos, se inicializan en setup_frame()
        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_imat: CustomDropdown
        self.imat = ""
        self.resultado: ctkFrame

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializa todas las widgets y las configura.
        """

        delete_msg_frame(self.mensaje_frame)
        instruct_i = ctkLabel(self, text="Seleccione la matriz a invertir:")

        self.select_imat = CustomDropdown(
            self,
            width=60,
            values=self.master_frame.nombres_matrices,
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            command=self.update_imat,
        )

        self.imat = self.select_imat.get()
        button = ctkButton(
            self,
            height=30,
            text="Encontrar inversa",
            command=self.encontrar_inversa,
        )

        self.resultado = ctkFrame(self, fg_color="transparent")
        self.resultado.columnconfigure(0, weight=1)

        instruct_i.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_imat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.resultado.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def encontrar_inversa(self) -> None:
        """
        Invierte la matriz seleccionada.
        """

        delete_msg_frame(self.mensaje_frame)
        self.update_imat(self.select_imat.get())
        nombre_inversa, inversa, _, _ = (
            self.mats_manager.invertir_mat(self.imat)
        )

        self.mensaje_frame = place_msg_frame(
            parent_frame=self.resultado,
            msg_frame=self.mensaje_frame,
            msg=f"{nombre_inversa}:\n\n{str(inversa)}",
            tipo="resultado",
            columnspan=3,
        )

        # si la inversa no esta guardada,
        # agregarla y mandar a actualizar los datos
        if not any(
            inversa == mat
            for mat in self.mats_manager.mats_ingresadas.values()
        ):
            self.mats_manager.mats_ingresadas[nombre_inversa] = inversa
            self.master_frame.update_all()
            self.app.vectores.update_all()  # type: ignore
            self.app.inputs_frame.instances[1].update_all()  # type: ignore


    def update_frame(self) -> None:
        """
        Actualiza los valores del dropdown.
        """

        self.select_imat.configure(
            variable=Variable(value=self.master_frame.nombres_matrices[0]),
            values=self.master_frame.nombres_matrices,
        )

    def update_imat(self, valor: str) -> None:
        """
        Actualiza self.imat con el valor
        seleccionado en el dropdown.
        """

        self.imat = valor
