"""
Implementación de los subframes de ManejarMats.
"""

from fractions import Fraction
from os import path
from random import randint
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from tkinter import (
    Variable,
    TclError,
)

from PIL.Image import open as open_img

from customtkinter import (
    CTkBaseClass as ctkBase,
    CTkButton as ctkButton,
    CTkCheckBox as ctkCheckBox,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
)

from gauss_bot import ASSET_PATH

from gauss_bot.models.matriz import Matriz
from gauss_bot.managers.mats_manager import MatricesManager

from gauss_bot.gui.custom_frames import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    SuccessFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui.gui import GaussUI
    from gauss_bot.gui.frames.inputs import ManejarMats


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
        self.columnconfigure(1, weight=1)

        self.aumentada = False
        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[list[CustomEntry]] = []
        self.post_matriz_widgets: list[ctkBase] = []

        checkbox_label = ctkLabel(self, text="¿Es un sistema de ecuaciones?")
        self.check_aumentada = ctkCheckBox(self, text="", command=self.toggle_aumentada)
        filas_label = ctkLabel(self, text="Número de filas:")
        self.filas_entry = ctkEntry(self, width=60, placeholder_text="3")
        columnas_label = ctkLabel(self, text="Número de columnas:")
        self.columnas_entry = ctkEntry(self, width=60, placeholder_text="3")

        ingresar_button = ctkButton(
            self, height=30, text="Ingresar datos", command=self.generar_casillas
        )

        aleatoria_button = ctkButton(
            self,
            height=30,
            text="Generar matriz aleatoria",
            command=self.generar_aleatoria,
        )

        self.matriz_frame = ctkFrame(self)

        self.filas_entry.bind("<Return>", lambda x: self.generar_casillas())
        self.filas_entry.bind("<Up>", lambda x: self.focus_set_columnas())
        self.filas_entry.bind("<Down>", lambda x: self.focus_set_columnas())
        self.columnas_entry.bind("<Return>", lambda x: self.generar_casillas())
        self.columnas_entry.bind("<Up>", lambda x: self.focus_set_filas())
        self.columnas_entry.bind("<Down>", lambda x: self.columnas_move_down())

        checkbox_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.check_aumentada.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        filas_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.filas_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        columnas_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.columnas_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ingresar_button.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        aleatoria_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.matriz_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ns")
        self.update_scrollbar_visibility()

    def limpiar_casillas(self) -> None:
        """
        Borra todos los valores ingresados en las casillas de la matriz.
        """

        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.delete(0, "end")
        self.input_entries.clear()
        try:
            self.nombre_entry.delete(0, "end")
        except AttributeError:
            pass

    def generar_casillas(self) -> None:
        """
        Genera casillas para ingresar una matriz de las dimensiones indicadas.
        """

        try:
            self.limpiar_casillas()
            for widget in self.matriz_frame.winfo_children():
                widget.destroy()  # type: ignore
            for widget in self.post_matriz_widgets:
                widget.destroy()
        except TclError:
            pass

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            filas = int(self.filas_entry.get())
            columnas = int(self.columnas_entry.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos como filas y columnas!"
            )
            self.mensaje_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        if self.aumentada:
            columnas += 1

        height = 35 * filas
        sep_icon = ctkImage(
            dark_image=open_img(
                path.join(ASSET_PATH, "light_separator.png")
            ),
            light_image=open_img(
                path.join(ASSET_PATH, "dark_separator.png")
            ),
            size=(35, height),
        )

        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                input_entry = CustomEntry(self.matriz_frame, width=60)
                if not self.aumentada or j != columnas - 1:
                    input_entry.grid(row=i, column=j, padx=5, pady=5)
                elif self.aumentada and j == columnas - 1:
                    sep_placed = ctkLabel(self.matriz_frame, image=sep_icon, text="")
                    sep_placed.grid(row=0, rowspan=filas, column=j)
                    input_entry.grid(row=i, column=j+1, padx=5, pady=5)
                self.bind_entry_keys(input_entry, i, j)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        nombre_label = ctkLabel(self, text="Nombre de la matriz:")
        self.nombre_entry = ctkEntry(self, width=25, placeholder_text="A")
        agregar_button = ctkButton(self, height=30, text="Agregar", command=self.agregar_matriz)
        limpiar_button = ctkButton(
            self, height=30, text="Limpiar casillas", command=self.limpiar_casillas
        )

        nombre_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        agregar_button.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        limpiar_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.nombre_entry.bind("<Up>", lambda x: self.nombre_entry_up())
        self.nombre_entry.bind("<Return>", lambda x: self.agregar_matriz())
        self.update_scrollbar_visibility()

        self.post_matriz_widgets = [
            nombre_label,
            self.nombre_entry,
            agregar_button,
            limpiar_button,
        ]

    def generar_aleatoria(self) -> None:
        """
        Genera una matriz de las dimensiones indicadas,
        con valores racionales aleatorios.
        """

        self.generar_casillas()
        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.delete(0, "end")
                entry.insert(0, str(randint(-15, 15)))

    def agregar_matriz(self) -> None:
        """
        Agrega la matriz ingresada a la lista de matrices ingresadas.
        """

        try:
            filas = int(self.filas_entry.get())
            columnas = int(self.columnas_entry.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos como filas y columnas!"
            )
            self.mensaje_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        input_f = len(self.input_entries)
        input_c = len(self.input_entries[0])
        dimensiones_validas = (
            filas == input_f and columnas == input_c
            if not self.aumentada
            else filas == input_f and input_c - 1 == columnas
        )

        if not dimensiones_validas:
            self.mensaje_frame = ErrorFrame(
                self,
                "Las dimensiones de la matriz ingresada no coinciden con las dimensions indicadas!"
            )
            self.mensaje_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        if self.aumentada:
            columnas += 1

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
                        row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n"
                    )
                    self.update_scrollbar_visibility()
                    return
                except ZeroDivisionError:
                    self.mensaje_frame = ErrorFrame(
                        self, "El denominador no puede ser 0!"
                    )
                    self.mensaje_frame.grid(
                        row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n"
                    )
                    self.update_scrollbar_visibility()
                    return
                fila_valores.append(valor)
            valores.append(fila_valores)

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        nombre_nueva_matriz = self.nombre_entry.get()
        nueva_matriz = Matriz(
            aumentada=self.aumentada, filas=filas,
            columnas=columnas, valores=valores
        )

        nombre_valido = (
            nombre_nueva_matriz.isalpha()
            and nombre_nueva_matriz.isupper()
            and len(nombre_nueva_matriz) == 1
        )

        if not nombre_valido:
            self.mensaje_frame = ErrorFrame(
                self, "El nombre de la matriz debe ser una letra mayúscula!"
            )
            self.mensaje_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return
        if nombre_nueva_matriz in self.mats_manager.mats_ingresadas:
            self.mensaje_frame = ErrorFrame(
                self, f"Ya existe una matriz llamada '{nombre_nueva_matriz}'!"
            )
            self.mensaje_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.mats_manager.mats_ingresadas[nombre_nueva_matriz] = nueva_matriz
        self.mensaje_frame = SuccessFrame(
            self, "La matriz se ha agregado exitosamente!"
        )
        self.mensaje_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.master_frame.update_all()
        self.app.ecuaciones.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore
        self.update_scrollbar_visibility()

    def toggle_aumentada(self) -> None:
        self.aumentada = not self.aumentada

    def focus_set_columnas(self) -> None:
        self.columnas_entry.focus_set()

    def focus_set_filas(self) -> None:
        self.filas_entry.focus_set()

    def columnas_move_down(self) -> None:
        if len(self.matriz_frame.winfo_children()) == 0:
            self.focus_set_filas()
        else:
            self.input_entries[0][0].focus_set()

    def bind_entry_keys(self, entry: CustomEntry, i: int, j: int) -> None:
        entry.bind("<Up>", lambda x: self.entry_move_up(i, j))
        entry.bind("<Down>", lambda x: self.entry_move_down(i, j))
        entry.bind("<Left>", lambda x: self.entry_move_left(i, j))
        entry.bind("<Right>", lambda x: self.entry_move_right(i, j))

    def entry_move_up(self, i: int, j: int) -> None:
        if i > 0:
            self.input_entries[i - 1][j].focus_set()
        elif i == 0:
            self.focus_set_columnas()

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
        self.update_idletasks()
        self.update_scrollbar_visibility()


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

        self.options: dict[str, tuple[int, int]] = {
            "Mostrar todo": (-1, -1),
            "Sistemas ingresados": (1, 0),
            "Matrices ingresadas": (0, 0),
            "Matrices calculadas": (-1, 1)
        }

        select_label = ctkLabel(self, text="Seleccione un filtro:")
        self.select_option = CustomDropdown(
            self,
            height=30,
            values=list(self.options.keys()),
            command=self.update_option,
        )

        self.option_seleccionada = self.options[self.select_option.get()]
        mostrar_button = ctkButton(
            self, height=30, text="Mostrar", command=self.setup_mostrar
        )

        self.mostrar_frame = ctkFrame(self)
        self.print_frame: Optional[Union[ErrorFrame, ResultadoFrame]] = None

        select_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_option.grid(row=1, column=0, ipadx=10, padx=5, pady=5, sticky="n")
        mostrar_button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.mostrar_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def setup_mostrar(self) -> None:
        self.update_option(self.select_option.get())
        aumentada, calculada = self.option_seleccionada
        mats_text: str = self.mats_manager.get_matrices(aumentada, calculada)

        if self.print_frame is not None:
            self.print_frame.destroy()
            self.print_frame = None

        if mats_text.startswith("No"):
            self.print_frame = ErrorFrame(self.mostrar_frame, mats_text)
            self.print_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        else:
            self.print_frame = ResultadoFrame(
                self.mostrar_frame, header=mats_text, resultado="", solo_header=True
            )
            self.print_frame.grid(
                row=0, column=0,
                padx=10, pady=10, sticky="n",
            )
            self.print_frame.header.grid(ipadx=10, ipady=10)
        self.print_frame.columnconfigure(0, weight=1)
        self.update_scrollbar_visibility()

    def update_frame(self) -> None:
        for widget in self.mostrar_frame.winfo_children():
            widget.destroy()  # type: ignore
        self.update_idletasks()
        self.update_scrollbar_visibility()

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

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if len(self.nombres_matrices) > 0:
            placeholder = Variable(self, value=self.nombres_matrices[0])
        else:
            placeholder = None

        self.mensaje_frame: Optional[ctkFrame] = None
        self.instruct_eliminar = ctkLabel(self, text="¿Cuál matriz desea eliminar?")

        self.select_mat = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_matrices,
            variable=placeholder,
            command=self.update_mat,
        )

        self.button = ctkButton(
            self,
            height=30,
            text="Eliminar",
            command=lambda: self.eliminar_matriz(self.mat_seleccionada),
        )

        self.mat_seleccionada = self.select_mat.get()

        if len(self.nombres_matrices) == 0:
            self.mensaje_frame = ErrorFrame(
                self, "No hay matrices guardadas!"
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.instruct_eliminar.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_mat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def eliminar_matriz(self, nombre_tmat: str) -> None:
        """
        Elimina la matriz seleccionada.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.update_mat(self.select_mat.get())
        self.mats_manager.mats_ingresadas.pop(self.mat_seleccionada)

        self.mensaje_frame = SuccessFrame(
            self, message=f"Matriz '{self.mat_seleccionada}' eliminada!"
        )
        self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()
        self.master_frame.update_all()
        self.app.ecuaciones.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore

    def update_frame(self) -> None:
        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if len(self.nombres_matrices) == 0:
            if isinstance(self.mensaje_frame, ErrorFrame):
                return
            for widget in self.winfo_children():
                if isinstance(widget, SuccessFrame):
                    old_mensaje_frame = SuccessFrame(self, widget.mensaje_exito.cget("text"))
                widget.destroy()
            old_mensaje_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.mensaje_frame = ErrorFrame(self, "No hay matrices guardadas!")
            self.after(500, self.mensaje_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n"))

        elif len(self.nombres_matrices) > 0:
            placeholder = Variable(self, value=self.nombres_matrices[0])
            self.instruct_eliminar = ctkLabel(self, text="¿Cuál matriz desea eliminar?")
            self.select_mat = CustomDropdown(
                self,
                height=30,
                width=60,
                values=self.nombres_matrices,
                variable=placeholder,
                command=self.update_mat,
            )

            self.button = ctkButton(
                self,
                height=30,
                text="Eliminar",
                command=lambda: self.eliminar_matriz(self.mat_seleccionada),
            )

            if isinstance(self.mensaje_frame, ErrorFrame):
                self.mensaje_frame.destroy()
                self.mensaje_frame = None

            self.update_mat(self.select_mat.get())
            self.instruct_eliminar.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.select_mat.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()
        self.update_idletasks()

    def update_mat(self, valor: str) -> None:
        self.mat_seleccionada = valor
