"""
Implementación de los subframes de ManejarMats.
"""

from fractions import Fraction
from random import randint
from time import sleep
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from tkinter import Variable
from customtkinter import (
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from gauss_bot import (
    ENTER_ICON,
    SHUFFLE_ICON,
    ACEPTAR_ICON,
    LIMPIAR_ICON,
    MOSTRAR_ICON,
    ELIMINAR_ICON,
    delete_msg_frame,
)

from gauss_bot.models import Matriz
from gauss_bot.managers import MatricesManager
from gauss_bot.gui.custom import (
    IconButton,
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    SuccessFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import ManejarMats


class AgregarMats(CustomScrollFrame):
    """
    Frame para agregar una nueva matriz.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarMats",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[list[CustomEntry]] = []

        self.pre_mat_frame = ctkFrame(self)
        self.matriz_frame = ctkFrame(self)
        self.post_mat_frame = ctkFrame(self)
        self.nombre_entry: ctkEntry

        filas_label = ctkLabel(self.pre_mat_frame, text="Filas:")
        self.filas_entry = ctkEntry(self.pre_mat_frame, width=30, placeholder_text="3")
        columnas_label = ctkLabel(self.pre_mat_frame, text="Columnas:")
        self.columnas_entry = ctkEntry(self.pre_mat_frame, width=30, placeholder_text="3")

        ingresar_button = IconButton(
            self.pre_mat_frame,
            self.app,
            image=ENTER_ICON,
            tooltip_text="Ingresar datos de la matriz",
            command=self.generar_casillas
        )

        aleatoria_button = IconButton(
            self.pre_mat_frame,
            self.app,
            image=SHUFFLE_ICON,
            tooltip_text="Generar matriz con datos aleatorios",
            command=self.generar_aleatoria,
        )

        self.filas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.filas_entry.bind("<Left>", lambda _: self.focus_set_columnas())
        self.filas_entry.bind("<Right>", lambda _: self.focus_set_columnas())
        self.filas_entry.bind("<Down>", lambda _: self.move_down())
        self.columnas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.columnas_entry.bind("<Left>", lambda _: self.focus_set_filas())
        self.columnas_entry.bind("<Right>", lambda _: self.focus_set_filas())
        self.columnas_entry.bind("<Down>", lambda _: self.move_down())

        self.pre_mat_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        filas_label.grid(row=0, column=0, padx=5, pady=5)
        self.filas_entry.grid(row=0, column=1, padx=5, pady=5)
        columnas_label.grid(row=0, column=2, padx=5, pady=5)
        self.columnas_entry.grid(row=0, column=3, padx=5, pady=5)
        ingresar_button.grid(row=0, column=4, padx=3, pady=5)
        aleatoria_button.grid(row=0, column=5, padx=3, pady=5)

    def limpiar_casillas(self) -> None:
        """
        Borra todos los valores ingresados en las casillas de la matriz.
        """

        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")

    def generar_casillas(self) -> None:
        """
        Genera casillas para ingresar una matriz de las dimensiones indicadas.
        """

        for widget in self.matriz_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.post_mat_frame.winfo_children():
            widget.destroy()

        delete_msg_frame(self.mensaje_frame)
        try:
            filas = int(self.filas_entry.get())
            columnas = int(self.columnas_entry.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos como filas y columnas!"
            )
            self.mensaje_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            return
        delete_msg_frame(self.mensaje_frame)

        self.input_entries.clear()
        self.input_entries = []
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                input_entry = CustomEntry(self.matriz_frame, width=60)
                input_entry.grid(row=i, column=j, padx=5, pady=5)
                self.bind_entry_keys(input_entry, i, j)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        nombre_label = ctkLabel(self.post_mat_frame, text="Nombre de la matriz:")
        self.nombre_entry = ctkEntry(self.post_mat_frame, width=30, placeholder_text="A")

        agregar_button = IconButton(
            self.post_mat_frame,
            self.app,
            image=ACEPTAR_ICON,
            tooltip_text="Agregar matriz",
            command=self.agregar_matriz
        )

        limpiar_button = IconButton(
            self.post_mat_frame,
            self.app,
            image=LIMPIAR_ICON,
            tooltip_text="Limpiar casillas",
            command=self.limpiar_casillas
        )

        self.matriz_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.post_mat_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        self.nombre_entry.bind("<Up>", lambda _: self.nombre_entry_up())
        self.nombre_entry.bind("<Return>", lambda _: self.agregar_matriz())

    def generar_aleatoria(self) -> None:
        """
        Genera una matriz de las dimensiones indicadas,
        con valores enteros aleatorios.
        """

        self.generar_casillas()
        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.insert(0, randint(-15, 15))

    def agregar_matriz(self) -> None:
        """
        Agrega la matriz ingresada a la lista de matrices ingresadas.
        """

        delete_msg_frame(self.mensaje_frame)
        try:
            filas = int(self.filas_entry.get())
            columnas = int(self.columnas_entry.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos como filas y columnas!"
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        input_f = len(self.input_entries)
        input_c = len(self.input_entries[0])
        dimensiones_validas = (
            filas == input_f and columnas == input_c
        )

        if not dimensiones_validas:
            self.mensaje_frame = ErrorFrame(
                self,
                "Las dimensiones de la matriz ingresada no coinciden con las dimensiones indicadas!"
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        valores = []
        for fila_entries in self.input_entries:
            fila_valores = []
            for entry in fila_entries:
                try:
                    valor = Fraction(entry.get())
                except ValueError:
                    self.mensaje_frame = ErrorFrame(
                        self, "Todos los valores deben ser números racionales!"
                    )
                    self.mensaje_frame.grid(
                        row=3, column=0, padx=5, pady=5, sticky="n"
                    )
                    return
                except ZeroDivisionError:
                    self.mensaje_frame = ErrorFrame(
                        self, "El denominador no puede ser 0!"
                    )
                    self.mensaje_frame.grid(
                        row=3, column=0, padx=5, pady=5, sticky="n"
                    )
                    return
                fila_valores.append(valor)
            valores.append(fila_valores)

        delete_msg_frame(self.mensaje_frame)
        nombre_nueva_matriz = self.nombre_entry.get()
        nueva_matriz = Matriz(
            aumentada=False, filas=filas,
            columnas=columnas, valores=valores
        )

        nombre_repetido = nombre_nueva_matriz in self.mats_manager.mats_ingresadas
        nombre_valido = (
            nombre_nueva_matriz.isalpha()
            and nombre_nueva_matriz.isupper()
            and len(nombre_nueva_matriz) == 1
        )

        if not nombre_valido or nombre_repetido:
            msj = (
                "El nombre de la matriz debe ser una letra mayúscula!"
                if not nombre_valido
                else f"Ya existe una matriz nombrada '{nombre_nueva_matriz}'!"
            )

            self.mensaje_frame = ErrorFrame(self, msj)
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        self.mats_manager.mats_ingresadas[nombre_nueva_matriz] = nueva_matriz
        self.mensaje_frame = SuccessFrame(
            self, "La matriz se ha agregado exitosamente!"
        )

        self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.master_frame.update_all()
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore

    def focus_set_columnas(self) -> None:
        self.columnas_entry.focus_set()

    def focus_set_filas(self) -> None:
        self.filas_entry.focus_set()

    def move_down(self) -> None:
        try:
            self.input_entries[0][0].focus_set()
        except IndexError:
            pass

    def bind_entry_keys(self, entry: CustomEntry, i: int, j: int) -> None:
        entry.bind("<Up>", lambda _: self.entry_move_up(i, j))
        entry.bind("<Down>", lambda _: self.entry_move_down(i, j))
        entry.bind("<Left>", lambda _: self.entry_move_left(i, j))
        entry.bind("<Right>", lambda _: self.entry_move_right(i, j))

    def entry_move_up(self, i: int, j: int) -> None:
        if i > 0:
            self.input_entries[i - 1][j].focus_set()
        elif i == 0:
            self.focus_set_filas()

    def entry_move_down(self, i: int, j: int) -> None:
        if i < len(self.input_entries) - 1:
            self.input_entries[i + 1][j].focus_set()
        elif i == len(self.input_entries) - 1:
            self.nombre_entry.focus_set()

    def entry_move_left(self, i: int, j: int) -> None:
        if j > 0:
            self.input_entries[i][j - 1].focus_set()
        elif j == 0:
            if i > 0:
                self.input_entries[i - 1][-1].focus_set()

    def entry_move_right(self, i: int, j: int) -> None:
        if j < len(self.input_entries[i]) - 1:
            self.input_entries[i][j + 1].focus_set()
        elif j == len(self.input_entries[i]) - 1:
            if i < len(self.input_entries) - 1:
                self.input_entries[i + 1][0].focus_set()
            elif i == len(self.input_entries) - 1:
                self.nombre_entry.focus_set()

    def nombre_entry_up(self) -> None:
        self.input_entries[-1][-1].focus_set()

    def update_frame(self) -> None:
        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore
            if isinstance(widget, ctkFrame):
                for subwidget in widget.winfo_children():
                    subwidget.configure(bg_color="transparent")  # type: ignore


class MostrarMats(CustomScrollFrame):
    """
    Frame para mostrar todas las matrices ingresadas.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarMats",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.options: dict[str, int] = {
            "Mostrar todas": -1,
            "Matrices ingresadas": 0,
            "Matrices calculadas": 1,
        }

        select_label = ctkLabel(self, text="Seleccione un filtro:")
        self.select_option = CustomDropdown(
            self,
            height=30,
            values=list(self.options.keys()),
            command=self.update_option,
        )

        self.option_seleccionada = self.options[self.select_option.get()]
        mostrar_button = IconButton(
            self,
            self.app,
            image=MOSTRAR_ICON,
            tooltip_text="Mostrar",
            command=self.setup_mostrar
        )

        self.print_frame: Optional[Union[ErrorFrame, ResultadoFrame]] = None

        select_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_option.grid(row=1, column=0, ipadx=10, padx=5, pady=5, sticky="e")
        mostrar_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def setup_mostrar(self) -> None:
        delete_msg_frame(self.print_frame)
        self.update_option(self.select_option.get())

        calculada = self.option_seleccionada
        mats_text = self.mats_manager.get_matrices(calculada)

        if "!" in mats_text:
            self.print_frame = ErrorFrame(self, mats_text)
            self.print_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")
        else:
            self.print_frame = ResultadoFrame(
                self,
                header=mats_text,
                resultado="",
                solo_header=True
            )
            self.print_frame.grid(
                row=0, column=0,
                columnspan=2,
                padx=10, pady=10,
                sticky="n",
            )
            self.print_frame.header.grid(ipadx=10, ipady=10)
        self.print_frame.columnconfigure(0, weight=1)
        self.print_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")

    def update_frame(self) -> None:
        try:
            self.print_frame.destroy()  # type: ignore
        except AttributeError:
            pass
        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

    def update_option(self, valor: str) -> None:
        self.option_seleccionada = self.options[valor]


class EliminarMats(CustomScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarMats",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mensaje_frame: Optional[Union[ErrorFrame, SuccessFrame]] = None
        self.select_mat: CustomDropdown
        self.mat_seleccionada = ""
        self.setup_frame()

    def setup_frame(self) -> None:
        delete_msg_frame(self.mensaje_frame)
        if len(self.nombres_matrices) == 0:
            self.mensaje_frame = ErrorFrame(self, "No hay matrices guardadas!")
            self.mensaje_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            return

        placeholder = Variable(self, value=self.nombres_matrices[0])
        instruct_eliminar = ctkLabel(self, text="¿Cuál matriz desea eliminar?")

        self.select_mat = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_matrices,
            variable=placeholder,
            command=self.update_mat,
        )

        button = IconButton(
            self,
            self.app,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar matriz",
            command=lambda: self.eliminar_matriz(),
        )

        self.mat_seleccionada = self.select_mat.get()

        instruct_eliminar.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_mat.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_matriz(self) -> None:
        """
        Elimina la matriz seleccionada.
        """

        delete_msg_frame(self.mensaje_frame)
        self.update_mat(self.select_mat.get())
        self.mats_manager.mats_ingresadas.pop(self.mat_seleccionada)

        self.mensaje_frame = SuccessFrame(
            self,
            message=f"Matriz '{self.mat_seleccionada}' eliminada!"
        )

        self.mensaje_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.master_frame.update_all()
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore

    def update_frame(self) -> None:
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        if len(self.nombres_matrices) == 0 and isinstance(self.mensaje_frame, SuccessFrame):
            sleep(1.5)
            delete_msg_frame(self.mensaje_frame)
            self.mensaje_frame = ErrorFrame(self, "No hay matrices guardadas!")
            self.mensaje_frame.grid(
                row=0, column=0,
                columnspan=2,
                padx=5, pady=5,
                sticky="n"
            )

            for widget in self.winfo_children():
                if not isinstance(widget, ctkFrame):
                    widget.destroy()

        elif isinstance(self.mensaje_frame, ErrorFrame):
            self.setup_frame()
        else:
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
            self.select_mat.configure(
                variable=Variable(value=self.nombres_matrices[0]),
                values=self.nombres_matrices,
            )
            self.after(1500, lambda: delete_msg_frame(self.mensaje_frame))

    def update_mat(self, valor: str) -> None:
        self.mat_seleccionada = valor
