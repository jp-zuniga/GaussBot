"""
Implementación de todos los frames relacionados con vectores.
"""

from fractions import Fraction
from random import randint
from typing import Optional, Union

from customtkinter import (
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkOptionMenu as ctkOptionMenu,
    CTkScrollableFrame as ctkScrollFrame,
    CTkTabview as ctkTabview,
)

from gauss_bot.models.vector import Vector
from gauss_bot.managers.vecs_manager import VectoresManager

from gauss_bot.gui.custom_frames import (
    ErrorFrame,
    SuccessFrame,
    ResultadoFrame
)


class VectoresFrame(ctkFrame):
    """
    Frame que contiene un ctkTabview para todas
    las funcionalidades de vectores, donde cada
    una tiene su propia tab.
    """

    def __init__(self, master, app, vecs_manager: VectoresManager) -> None:
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.app = app
        self.vecs_manager = vecs_manager
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.app.mats_manager.mats_ingresadas.keys())
        self.crear_tabview()

    def crear_tabview(self) -> None:
        """
        Crea un ctkTabview con pestañas para cada funcionalidad.
        """

        self.tabview = ctkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.instances: list[Union[ctkFrame, ctkScrollFrame]] = []
        self.tabs = [
            ("Mostrar vectores", MostrarTab),
            ("Agregar vector", AgregarTab),
            ("Sumar y restar vectores", SumaRestaTab),
            ("Multiplicación", MultiplicacionTab),
        ]

        for nombre, cls in self.tabs:
            tab = self.tabview.add(nombre)
            tab_instance = cls(self, tab, self.app, self.vecs_manager)
            tab_instance.pack(expand=True, fill="both")
            self.instances.append(tab_instance)  # type: ignore

    def update_all(self) -> None:
        """
        Actualiza los datos de todos los frames del tabview.
        """

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.nombres_matrices = list(self.app.mats_manager.mats_ingresadas.keys())
        for tab in self.instances:
            tab.update()
            for widget in tab.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
        self.update_idletasks()


class MostrarTab(ctkScrollFrame):
    """
    Frame para mostrar todos los vectores ingresados por el usuario.
    """

    def __init__(self, master_frame, master_tab, app, vecs_manager: VectoresManager) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.vecs = ctkLabel(self, text=vecs_manager.get_vectores())
        self.vecs.pack(padx=5, pady=5, expand=True, fill="both")

    def update(self) -> None:
        self.vecs.configure(text=self.vecs_manager.get_vectores())
        self.update_idletasks()


class AgregarTab(ctkScrollFrame):
    """
    Frame para agregar un vector a la lista de vectores ingresados,
    ingresando datos manualmente o generándolos aleatoriamente.
    """

    def __init__(self, master_frame, master_tab, app, vecs_manager: VectoresManager) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[ctkEntry] = []
        self.nombre_entry = ctkEntry(self, width=60, placeholder_text="u")

        dimension_label = ctkLabel(self, text="Dimensiones del vector:")
        self.dimension_entry = ctkEntry(self, width=60)
        generar_button = ctkButton(self, text="Ingresar datos", command=self.generar_casillas)
        aleatorio_button = ctkButton(
            self, text="Generar vector aleatorio", command=self.generar_aleatorio
        )
        self.vector_frame = ctkFrame(self)

        dimension_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.dimension_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        generar_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        aleatorio_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.vector_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ns")

    def generar_casillas(self) -> None:
        """
        Genera las casillas para ingresar los valores del vector.
        """

        for widget in self.vector_frame.winfo_children():
            widget.destroy()  # type: ignore

        try:
            dimension = int(self.dimension_entry.get())
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar un número entero positivo como dimensión!"
            )
            self.mensaje_frame.grid(row=3, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        for i in range(dimension):
            input_entry = ctkEntry(self.vector_frame, width=60)
            input_entry.grid(row=i, column=0, padx=5, pady=5)
            self.input_entries.append(input_entry)

        nombre_label = ctkLabel(self, text="Nombre del vector:")
        agregar_button = ctkButton(self, text="Agregar", command=self.agregar_vector)
        limpiar_button = ctkButton(self, text="Limpiar casillas", command=self.generar_casillas)

        nombre_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        agregar_button.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        limpiar_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    def generar_aleatorio(self) -> None:
        """
        Genera casillas con valores aleatorios para el vector.
        """

        for widget in self.vector_frame.winfo_children():
            widget.destroy()  # type: ignore

        try:
            dimension = int(self.dimension_entry.get())
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar un número entero positivo como dimensión!"
            )
            self.mensaje_frame.grid(row=3, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        for i in range(dimension):
            numerador = randint(1, 20)
            denominador = randint(1, 10)
            valor_random = Fraction(numerador, denominador)
            input_entry = ctkEntry(self.vector_frame, width=60)
            input_entry.insert(0, str(valor_random))
            input_entry.grid(row=i, column=0, padx=5, pady=5)
            self.input_entries.append(input_entry)

        nombre_label = ctkLabel(self, text="Nombre del vector:")
        self.nombre_entry = ctkEntry(self, width=60, placeholder_text="u")
        agregar_button = ctkButton(self, text="Agregar", command=self.agregar_vector)
        limpiar_button = ctkButton(self, text="Limpiar casillas", command=self.generar_casillas)

        nombre_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        agregar_button.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        limpiar_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    def agregar_vector(self) -> None:
        """
        Crea un vector con los datos ingresados, y lo agrega al diccionario.
        """

        componentes = []
        for entry in self.input_entries:
            try:
                valor = Fraction(entry.get())
            except ValueError:
                self.mensaje_frame = ErrorFrame(
                    self, "Todos los valores deben ser números racionales!"
                )
                self.mensaje_frame.grid(row=6, column=0, columnspan=2, sticky="n", padx=5, pady=5)
                return
            except ZeroDivisionError:
                self.mensaje_frame = ErrorFrame(self, "El denominador no puede ser 0!")
                self.mensaje_frame.grid(row=6, column=0, columnspan=2, sticky="n", padx=5, pady=5)
                return
            componentes.append(valor)

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        nombre_nuevo_vector = self.nombre_entry.get()
        nuevo_vector = Vector(componentes)

        nombre_valido = (
            nombre_nuevo_vector.isalpha()
            and nombre_nuevo_vector.islower()
            and len(nombre_nuevo_vector) == 1
        )

        if not nombre_valido:
            self.mensaje_frame = ErrorFrame(
                self, "El nombre del vector debe ser una letra minúscula!"
            )
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return
        if nombre_nuevo_vector in self.vecs_manager.vecs_ingresados:
            self.mensaje_frame = ErrorFrame(
                self, f"Ya existe un vector llamado '{nombre_nuevo_vector}'!"
            )
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, sticky="n", padx=5, pady=5)
            return

        self.vecs_manager.vecs_ingresados[nombre_nuevo_vector] = nuevo_vector
        self.master_frame.update_all()
        self.mensaje_frame = SuccessFrame(self, "El vector se ha agregado exitosamente!")
        self.mensaje_frame.grid(row=6, column=0, columnspan=2, sticky="n", padx=5, pady=5)

    def update(self) -> None:
        self.update_idletasks()


class SumaRestaTab(ctkFrame):
    """
    Frame para sumar y restar vectores ingresados por el usuario.
    """

    def __init__(self, master_frame, master_tab, app, vecs_manager: VectoresManager) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.tabview = ctkTabview(self)

        self.tab_sumar = self.tabview.add("Sumar")
        self.tab_restar = self.tabview.add("Restar")
        self.setup_tab(self.tab_sumar, "Sumar")
        self.setup_tab(self.tab_restar, "Restar")

        self.resultado_suma = ctkFrame(self.tab_sumar)
        self.resultado_resta = ctkFrame(self.tab_restar)

        self.vec1 = self.select_1.get()
        self.vec2 = self.select_2.get()

        self.resultado_suma.columnconfigure(0, weight=1)
        self.resultado_resta.columnconfigure(0, weight=1)

        self.tabview.grid(row=0, column=0, sticky="n")
        self.resultado_suma.grid(row=4, column=0, sticky="n")
        self.resultado_resta.grid(row=4, column=0, sticky="n")

    def setup_tab(self, tab, operacion: str) -> None:
        """
        Para configurar las tabs de sumar y restar.
        """

        tab.columnconfigure(0, weight=1)
        instruct_sr = ctkLabel(tab, text=f"Seleccione los vectores para {operacion.lower()}:")

        self.select_1 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            command=self.update_select1,
        )

        self.select_2 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            command=self.update_select2,
        )

        ejecutar_button = ctkButton(
            tab,
            text=operacion,
            command=lambda: self.ejecutar_operacion(operacion, self.vec1, self.vec2),
        )

        self.vec1 = self.select_1.get()
        self.vec2 = self.select_2.get()

        instruct_sr.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_1.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.select_2.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        ejecutar_button.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def ejecutar_operacion(self, operacion: str, nombre_vec1: str, nombre_vec2: str) -> None:
        """
        Ejecuta la suma o resta de vectores, dependiendo en la elección del usuario.
        """

        self.update_select1(self.select_1.get())
        self.update_select2(self.select_2.get())

        if operacion == "Sumar":
            self.ejecutar_suma(nombre_vec1, nombre_vec2)
            return
        if operacion == "Restar":
            self.ejecutar_resta(nombre_vec1, nombre_vec2)
            return

    def ejecutar_suma(self, nombre_vec1: str, nombre_vec2: str) -> None:
        """
        Ejecuta la suma de dos vectores.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.vecs_manager.sumar_vecs(nombre_vec1, nombre_vec2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_suma, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_suma, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def ejecutar_resta(self, nombre_vec1: str, nombre_vec2: str) -> None:
        """
        Ejecuta la resta de dos vectores.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.vecs_manager.restar_vecs(nombre_vec1, nombre_vec2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_resta, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_resta, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def update(self) -> None:
        self.setup_tab(self.tab_sumar, "Sumar")
        self.setup_tab(self.tab_restar, "Restar")
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()

    def update_select1(self, valor: str) -> None:
        self.vec1 = valor

    def update_select2(self, valor: str) -> None:
        self.vec2 = valor


class MultiplicacionTab(ctkFrame):
    """
    Frame para realizar multiplicaciones de vectores por escalares,
    producto punto y producto matriz-vector.
    """

    def __init__(self, master_frame, master_tab, app, vecs_manager: VectoresManager) -> None:
        super().__init__(master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.tabview = ctkTabview(self)

        self.tab_escalar = self.tabview.add("Escalar por Vector")
        self.tab_vector = self.tabview.add("Producto Punto")
        self.tab_matriz_vector = self.tabview.add("Producto Matriz-Vector")
        self.setup_tabs()

        self.select_escalar_vec = ctkOptionMenu(self.tab_escalar, width=60)
        self.escalar_entry = ctkEntry(self.tab_escalar, width=60)
        self.select_vec1 = ctkOptionMenu(self.tab_vector, width=60)
        self.select_vec2 = ctkOptionMenu(self.tab_vector, width=60)
        self.select_vmat = ctkOptionMenu(self.tab_matriz_vector, width=60)
        self.select_mvec = ctkOptionMenu(self.tab_matriz_vector, width=60)

        self.escalar_vec = ""
        self.vec1 = ""
        self.vec2 = ""
        self.vmat = ""
        self.mvec = ""

        self.resultado_escalar = ctkFrame(self.tab_escalar)
        self.resultado_vectores = ctkFrame(self.tab_vector)
        self.resultado_mat_vec = ctkFrame(self.tab_matriz_vector)

        self.resultado_escalar.columnconfigure(0, weight=1)
        self.resultado_vectores.columnconfigure(0, weight=1)
        self.resultado_mat_vec.columnconfigure(0, weight=1)

        self.tabview.grid(row=0, column=0, sticky="n")
        self.resultado_escalar.grid(row=4, column=0, padx=5, sticky="n")
        self.resultado_vectores.grid(row=4, column=0, padx=5, sticky="n")
        self.resultado_mat_vec.grid(row=4, column=0, padx=5, sticky="n")

    def setup_tabs(self) -> None:
        """
        Wrapper para llamar todos los métodos de configuración de tabs.
        """

        self.setup_escalar_tab(self.tab_escalar)
        self.setup_vector_tab(self.tab_vector)
        self.setup_matriz_vector_tab(self.tab_matriz_vector)

    def setup_escalar_tab(self, tab: ctkFrame) -> None:
        """
        Setup de la tab para multiplicar un vector por un escalar.
        """

        tab.columnconfigure(0, weight=1)
        instruct_e = ctkLabel(tab, text="Seleccione el vector e ingrese el escalar:")

        self.select_escalar_vec = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            command=self.update_escalar_vec,
        )

        self.escalar_entry = ctkEntry(tab, width=60)
        multiplicar_button = ctkButton(
            tab,
            text="Multiplicar",
            command=lambda: self.mult_por_escalar(self.escalar_vec),
        )

        self.escalar_vec = self.select_escalar_vec.get()

        instruct_e.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_escalar_vec.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.escalar_entry.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        multiplicar_button.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def setup_vector_tab(self, tab: ctkFrame) -> None:
        """
        Setup de la tab para multiplicar vectores.
        """

        tab.columnconfigure(0, weight=1)
        instruct_v = ctkLabel(tab, text="Seleccione los vectores para multiplicar:")

        self.select_vec1 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            command=self.update_vec1,
        )

        self.select_vec2 = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            command=self.update_vec2,
        )

        multiplicar_button = ctkButton(
            tab,
            text="Multiplicar",
            command=lambda: self.mult_vectores(self.vec1, self.vec2),
        )

        self.vec1 = self.select_vec1.get()
        self.vec2 = self.select_vec2.get()

        instruct_v.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_vec1.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.select_vec2.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        multiplicar_button.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def setup_matriz_vector_tab(self, tab: ctkFrame) -> None:
        """
        Setup de la tab para multiplicar matrices y vectores.
        """

        tab.columnconfigure(0, weight=1)
        instruct_mv = ctkLabel(tab, text="Seleccione la matriz y el vector para multiplicar:")

        self.select_vmat = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_matrices,
            command=self.update_vmat,
        )

        self.select_mvec = ctkOptionMenu(
            tab,
            width=60,
            values=self.master_frame.nombres_vectores,
            command=self.update_mvec,
        )

        multiplicar_button = ctkButton(
            tab,
            text="Multiplicar",
            command=lambda: self.matriz_vector(self.vmat, self.mvec),
        )


        self.vmat = self.select_vmat.get()
        self.mvec = self.select_mvec.get()

        instruct_mv.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_vmat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.select_mvec.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        multiplicar_button.grid(row=3, column=0, padx=5, pady=5, sticky="n")

    def mult_por_escalar(self, vec: str) -> None:
        """
        Realiza la multiplicación de un vector por un escalar.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            escalar = Fraction(self.escalar_entry.get())
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

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_escalar, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def mult_vectores(self, nombre_vec1: str, nombre_vec2: str) -> None:
        """
        Realiza el producto punto de dos vectores.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.vecs_manager.producto_punto(nombre_vec1, nombre_vec2)
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_vectores, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_vectores, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def matriz_vector(self, nombre_mat: str, nombre_vec: str) -> None:
        """
        Realiza el producto de una matriz por un vector.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            header, resultado = self.app.ops_manager.matriz_por_vector(
                nombre_mat, nombre_vec
            )
        except ArithmeticError as e:
            self.mensaje_frame = ErrorFrame(self.resultado_mat_vec, str(e))
            self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.mensaje_frame = ResultadoFrame(
            self.resultado_mat_vec, header=f"{header}:", resultado=str(resultado)
        )
        self.mensaje_frame.grid(row=0, column=0, padx=5, pady=5)

    def update(self) -> None:
        self.setup_tabs()
        self.tabview.configure(fg_color="transparent")
        self.update_idletasks()

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
