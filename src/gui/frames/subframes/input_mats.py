"""
Implementación de los subframes de ManejarMats.
"""

from fractions import Fraction
from random import choice, randint
from string import ascii_uppercase
from tkinter import Variable
from typing import TYPE_CHECKING, Literal

from customtkinter import CTkFrame, CTkLabel

from src.gui.custom import (
    CustomDropdown,
    CustomEntry,
    ErrorFrame,
    IconButton,
    SuccessFrame,
)
from src.gui.custom.adapted import CustomScrollFrame
from src.managers import KeyBindingManager, MatricesManager
from src.models import Matriz
from src.utils import (
    ACEPTAR_ICON,
    ELIMINAR_ICON,
    ENTER_ICON,
    LIMPIAR_ICON,
    MOSTRAR_ICON,
    SHUFFLE_ICON,
    delete_msg_frame,
    place_msg_frame,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.frames import ManejarMats


class AgregarMats(CustomScrollFrame):
    """
    Frame para agregar nuevas matrices.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarMats",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de agregar matrices.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.key_binder = KeyBindingManager(es_matriz=True)
        self.msg_frame: CTkFrame | None = None
        self.input_entries: list[list[CustomEntry]] = []

        # frames para contener secciones de la interfaz
        self.pre_mat_frame = CTkFrame(self, fg_color="transparent")
        self.matriz_frame = CTkFrame(self, fg_color="transparent")
        self.post_mat_frame = CTkFrame(self, fg_color="transparent")
        self.nombre_entry: CustomEntry

        # crear widgets iniciales para ingresar dimensiones de matriz
        filas_label = CTkLabel(self.pre_mat_frame, text="Filas:")
        columnas_label = CTkLabel(self.pre_mat_frame, text="Columnas:")

        self.filas_entry = CustomEntry(
            self.pre_mat_frame,
            width=60,
            placeholder_text="3",
        )

        self.columnas_entry = CustomEntry(
            self.pre_mat_frame,
            width=60,
            placeholder_text="3",
        )

        ingresar_button = IconButton(
            self.pre_mat_frame,
            image=ENTER_ICON,
            tooltip_text="Ingresar datos de la matriz",
            command=self.generar_casillas,
        )

        aleatoria_button = IconButton(
            self.pre_mat_frame,
            image=SHUFFLE_ICON,
            tooltip_text="Generar matriz con datos aleatorios",
            command=self.generar_aleatoria,
        )

        # crear bindings para todas las entries iniciales
        self.filas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.filas_entry.bind(
            "<Left>",
            lambda _: self.key_binder.focus_columnas(self.columnas_entry),
        )

        self.filas_entry.bind(
            "<Right>",
            lambda _: self.key_binder.focus_columnas(self.columnas_entry),
        )

        self.filas_entry.bind("<Down>", lambda _: self.key_binder.focus_first())
        self.columnas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.columnas_entry.bind(
            "<Left>",
            lambda _: self.key_binder.focus_filas(self.filas_entry),
        )

        self.columnas_entry.bind(
            "<Right>",
            lambda _: self.key_binder.focus_filas(self.filas_entry),
        )

        self.columnas_entry.bind("<Down>", lambda _: self.key_binder.focus_first())

        # colocar widgets
        self.pre_mat_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        filas_label.grid(row=0, column=0, padx=5, pady=5)
        self.filas_entry.grid(row=0, column=1, padx=5, pady=5)
        columnas_label.grid(row=0, column=2, padx=5, pady=5)
        self.columnas_entry.grid(row=0, column=3, padx=5, pady=5)
        ingresar_button.grid(row=0, column=4, padx=3, pady=5)
        aleatoria_button.grid(row=0, column=5, padx=3, pady=5)

    def limpiar_casillas(self) -> None:
        """
        Eliminar valores ingresados previamente.
        """

        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")

    def generar_casillas(self) -> None:
        """
        Generar casillas para ingresar una matriz de las dimensiones indicadas.
        """

        # si habian widgets creadas debajo
        # de self.pre_mat_frame, eliminarlas
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()
        for widget in self.post_mat_frame.winfo_children():
            widget.destroy()

        delete_msg_frame(self.msg_frame)
        try:
            filas, columnas = self.validar_dimensiones()
        except ValueError as v:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg=str(v),
                tipo="error",
                row=1,
            )

            return
        delete_msg_frame(self.msg_frame)

        # crear entries para ingresar la matriz
        self.input_entries.clear()
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                input_entry = CustomEntry(
                    self.matriz_frame,
                    width=80,
                    placeholder_text=str(randint(-15, 15)),
                )

                input_entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        # crear post_mat_frame widgets
        nombre_label = CTkLabel(self.post_mat_frame, text="Nombre de la matriz:")
        self.nombre_entry = CustomEntry(
            self.post_mat_frame,
            width=60,
            placeholder_text=choice(
                [
                    x
                    for x in ascii_uppercase
                    if x not in self.mats_manager.mats_ingresadas.values()
                ],
            ),
        )

        agregar_button = IconButton(
            self.post_mat_frame,
            image=ACEPTAR_ICON,
            tooltip_text="Agregar matriz",
            command=self.agregar_matriz,
        )

        limpiar_button = IconButton(
            self.post_mat_frame,
            image=LIMPIAR_ICON,
            tooltip_text="Limpiar casillas",
            command=self.limpiar_casillas,
        )

        # colocar parent frames
        self.matriz_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n")

        self.post_mat_frame.grid(row=2, column=0, padx=5, pady=5, sticky="n")

        # colocar widgets
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        # configurar atributos de self.key_binder y crear bindings
        self.key_binder.entry_list = self.input_entries
        self.key_binder.extra_entries = (self.nombre_entry, self.filas_entry)
        self.key_binder.create_key_bindings()

        # encargarse de los bindings de nombre_entry
        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
        self.nombre_entry.bind("<Return>", lambda _: self.agregar_matriz())

    def generar_aleatoria(self) -> None:
        """
        Generar matriz con valores aleatorios.
        """

        self.generar_casillas()
        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.insert(0, randint(-15, 15))

    def agregar_matriz(self) -> None:
        """
        Agregar matriz ingresada al diccionario de matrices ingresadas.
        """

        delete_msg_frame(self.msg_frame)
        try:
            filas, columnas = self.validar_dimensiones()
        except ValueError as v:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg=str(v),
                tipo="error",
                row=1,
            )

            return
        delete_msg_frame(self.msg_frame)

        # si los inputs de filas/columnas
        # cambiaron despues de generar las casillas
        dimensiones_validas = filas == len(self.input_entries) and columnas == len(
            self.input_entries[0],
        )

        if not dimensiones_validas:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="Las dimensiones de la matriz ingresada "
                "no coinciden con las dimensiones indicadas.",
                tipo="error",
                row=3,
            )
            return

        # recorrer los entries y guardar los valores
        valores = []
        for fila_entries in self.input_entries:
            fila_valores = []
            for entry in fila_entries:
                try:
                    valor = Fraction(entry.get())
                except (ValueError, ZeroDivisionError) as e:
                    if isinstance(e, ValueError):
                        msg = "Todos los valores deben ser números racionales."
                    else:
                        msg = "El denominador de una fracción no puede ser 0."
                    self.msg_frame = place_msg_frame(
                        parent_frame=self,
                        msg_frame=self.msg_frame,
                        msg=msg,
                        tipo="error",
                        row=3,
                    )
                    return
                fila_valores.append(valor)
            valores.append(fila_valores)
        delete_msg_frame(self.msg_frame)

        nombre_nueva_matriz = self.nombre_entry.get()
        nueva_matriz = Matriz(filas, columnas, valores=valores)

        # validar nombre de la matriz
        nombre_repetido = nombre_nueva_matriz in self.mats_manager.mats_ingresadas
        nombre_valido = (
            nombre_nueva_matriz.isalpha()
            and nombre_nueva_matriz.isupper()
            and len(nombre_nueva_matriz) == 1
        )

        if not nombre_valido or nombre_repetido:
            msg = (
                "El nombre de la matriz debe ser una letra mayúscula."
                if not nombre_valido
                else f"¡Ya existe una matriz nombrada {nombre_nueva_matriz}!"
            )

            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg=msg,
                tipo="error",
                row=3,
            )
            return
        delete_msg_frame(self.msg_frame)

        self.mats_manager.mats_ingresadas[nombre_nueva_matriz] = nueva_matriz
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"¡La matriz {nombre_nueva_matriz} se ha agregado exitosamente!",
            tipo="success",
            row=3,
        )

        # mandar a actualizar los datos
        self.app.matrices.update_all()
        self.app.vectores.update_all()
        self.master_frame.update_all()

    def validar_dimensiones(self) -> tuple[int, int]:
        """
        Validar dimensiones ingresadas.

        Returns:
            (int, int): Filas, columnas.

        """

        filas = int(self.filas_entry.get())
        columnas = int(self.columnas_entry.get())

        if filas <= 0 or columnas <= 0:
            raise ValueError(
                "Debe ingresar números enteros positivos como filas y columnas.",
            )
        return (filas, columnas)

    def update_frame(self) -> None:
        """
        Actualizar colores de widgets.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if isinstance(widget, CTkFrame):
                for subwidget in widget.winfo_children():
                    subwidget.configure(bg_color="transparent")


class MostrarMats(CustomScrollFrame):
    """
    Frame para mostrar matrices.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarMats",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de mostrar matrices.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.show_frame: CTkFrame | None = None

        # definir los filtros que se mandaran
        # a self.mats_manager.get_matrices()
        self.opciones: dict[str, Literal[-1, 0, 1]] = {
            "Mostrar todas": -1,
            "Matrices ingresadas": 0,
            "Matrices calculadas": 1,
        }

        self.select_opcion: CustomDropdown
        self.opcion_seleccionada: Literal[-1, 0, 1] = -1

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar widgets del frame.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if len(self.mats_manager.mats_ingresadas.keys()) == 0:
            self.show_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.show_frame,
                msg="¡No se ha guardado ninguna matriz!",
                tipo="error",
                columnspan=2,
            )

            return

        self.select_opcion = CustomDropdown(
            self,
            height=30,
            variable=Variable(value="Seleccione un filtro:"),
            values=list(self.opciones.keys()),
            command=self.update_opcion,
        )

        self.select_opcion.grid(row=0, column=0, ipadx=10, padx=5, pady=5, sticky="e")
        IconButton(
            self,
            image=MOSTRAR_ICON,
            tooltip_text="Mostrar",
            command=self.show_mats,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def show_mats(self) -> None:
        """
        Mostrar matrices según el filtro seleccionado..
        """

        delete_msg_frame(self.show_frame)
        if "filtro" in self.select_opcion.get():
            self.show_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.show_frame,
                msg="Debe seleccionar un filtro.",
                tipo="error",
                row=1,
                columnspan=2,
            )

            return

        self.update_opcion(self.select_opcion.get())

        mats_text = self.mats_manager.get_matrices(self.opcion_seleccionada)
        tipo: str = "error" if "!" in mats_text else "resultado"

        self.show_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.show_frame,
            msg=mats_text,
            tipo=tipo,
            row=1,
            columnspan=2,
        )

        self.show_frame.columnconfigure(0, weight=1)

    def update_frame(self) -> None:
        """
        Eliminar self.show_frame y configurar backgrounds.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

        if isinstance(self.show_frame, ErrorFrame):
            self.setup_frame()
        else:
            self.select_opcion.configure(
                variable=Variable(value="Seleccione un filtro:"),
            )

    def update_opcion(self, valor: str) -> None:
        """
        Actualizar 'self.opcion_seleccionada'.

        Args:
            valor: Selección del dropdown.

        """

        self.opcion_seleccionada = self.opciones[valor]


class EliminarMats(CustomScrollFrame):
    """
    Frame para eliminar matrices.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarMats",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de eliminar matrices.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.msg_frame: CTkFrame | None = None

        self.select_mat: CustomDropdown
        self.mat_seleccionada = ""

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Crear y colocar las widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        if len(self.nombres_matrices) == 0:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="¡No se ha guardado ninguna matriz!",
                tipo="error",
                columnspan=2,
            )

            return

        for widget in self.winfo_children():
            widget.destroy()

        # crear widgets
        instruct_eliminar = CTkLabel(self, text="¿Cuál matriz desea eliminar?")
        self.select_mat = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_matrices,
            command=self.update_mat,
        )

        button = IconButton(
            self,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar matriz",
            command=self.eliminar_matriz,
        )

        self.mat_seleccionada = self.select_mat.get()

        # colocar widgets
        instruct_eliminar.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="n",
        )
        self.select_mat.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_matriz(self) -> None:
        """
        Eliminar matriz seleccionada.
        """

        delete_msg_frame(self.msg_frame)
        self.update_mat(self.select_mat.get())
        self.mats_manager.mats_ingresadas.pop(self.mat_seleccionada)

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"¡Matriz {self.mat_seleccionada} eliminada!",
            tipo="success",
            row=2,
            columnspan=2,
        )

        # mandar a actualizar los datos
        self.app.matrices.update_all()
        self.app.vectores.update_all()
        self.master_frame.update_all()

    def update_frame(self) -> None:
        """
        Actualizar frame y datos.
        """

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if len(self.nombres_matrices) == 0 and isinstance(self.msg_frame, SuccessFrame):

            def clear_after_wait() -> None:
                delete_msg_frame(self.msg_frame)
                self.msg_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.msg_frame,
                    msg="¡No se ha guardado ninguna matriz!",
                    tipo="error",
                    columnspan=2,
                )

                for widget in self.winfo_children():
                    if not isinstance(widget, CTkFrame):
                        widget.grid_remove()

            self.after(1000, clear_after_wait)

        elif isinstance(self.msg_frame, ErrorFrame):
            self.setup_frame()

        else:
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")
            self.select_mat.configure(
                values=self.nombres_matrices,
                variable=Variable(value=self.nombres_matrices[0]),
            )

            self.after(1000, lambda: delete_msg_frame(self.msg_frame))

    def update_mat(self, valor: str) -> None:
        """
        Actualizar 'self.mat_seleccionada'.

        Args:
            valor: Selección del dropdown.

        """

        self.mat_seleccionada = valor
