"""
Implementación de los subframes de ManejarMats.
"""

from fractions import Fraction
from random import randint
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

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
from gauss_bot.managers import (
    KeyBindingManager,
    MatricesManager,
)

from gauss_bot.gui.custom import (
    IconButton,
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    ErrorFrame,
    SuccessFrame,
    place_msg_frame,
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

        self.key_binder = KeyBindingManager(es_matriz=True)
        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[list[CustomEntry]] = []

        # frames para contener secciones de la interfaz
        self.pre_mat_frame = ctkFrame(self, fg_color="transparent")
        self.matriz_frame = ctkFrame(self, fg_color="transparent")
        self.post_mat_frame = ctkFrame(self, fg_color="transparent")
        self.nombre_entry: ctkEntry

        # crear widgets iniciales para ingresar dimensiones de matriz
        filas_label = ctkLabel(self.pre_mat_frame, text="Filas:")
        columnas_label = ctkLabel(self.pre_mat_frame, text="Columnas:")

        self.filas_entry = ctkEntry(
            self.pre_mat_frame,
            width=30,
            placeholder_text="3",
        )

        self.columnas_entry = ctkEntry(
            self.pre_mat_frame,
            width=30,
            placeholder_text="3",
        )

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

        # crear bindings para todas las entry's iniciales
        # para que se pueda navegar con las flechas
        self.filas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.filas_entry.bind(
            "<Left>",
            lambda _: self.key_binder.focus_columnas(self.columnas_entry)
        )

        self.filas_entry.bind(
            "<Right>",
            lambda _: self.key_binder.focus_columnas(self.columnas_entry)
        )

        self.filas_entry.bind("<Down>", lambda _: self.key_binder.focus_first())
        self.columnas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.columnas_entry.bind(
            "<Left>",
            lambda _: self.key_binder.focus_filas(self.filas_entry)
        )

        self.columnas_entry.bind(
            "<Right>",
            lambda _: self.key_binder.focus_filas(self.filas_entry)
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

        # si habian widgets creadas debajo
        # de self.pre_mat_frame, eliminarlas
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.post_mat_frame.winfo_children():
            widget.destroy()

        delete_msg_frame(self.mensaje_frame)
        dimensiones = self.validar_dimensiones()
        if dimensiones is None:
            return
        filas, columnas = dimensiones
        delete_msg_frame(self.mensaje_frame)

        self.input_entries.clear()
        self.input_entries = []
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                input_entry = CustomEntry(self.matriz_frame, width=60)
                input_entry.insert(0, randint(-15, 15))
                input_entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        nombre_label = ctkLabel(self.post_mat_frame, text="Nombre de la matriz:")
        self.nombre_entry = ctkEntry(
            self.post_mat_frame,
            width=30,
            placeholder_text="A",
        )

        agregar_button = IconButton(
            self.post_mat_frame,
            self.app,
            image=ACEPTAR_ICON,
            tooltip_text="Agregar matriz",
            command=self.agregar_matriz,
        )

        limpiar_button = IconButton(
            self.post_mat_frame,
            self.app,
            image=LIMPIAR_ICON,
            tooltip_text="Limpiar casillas",
            command=self.limpiar_casillas,
        )

        self.matriz_frame.grid(
            row=1, column=0,
            columnspan=2,
            padx=5, pady=5,
            sticky="n",
        )

        self.post_mat_frame.grid(
            row=2, column=0,
            columnspan=2,
            padx=5, pady=5,
            sticky="n",
        )

        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        self.key_binder.entry_list = self.input_entries  # type: ignore
        self.key_binder.extra_entries = (self.nombre_entry, self.filas_entry)  # type: ignore
        self.key_binder.create_key_bindings()

        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
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
            filas, columnas = self.validar_dimensiones()  # type: ignore
        except TypeError:
            return
        delete_msg_frame(self.mensaje_frame)

        dimensiones_validas = (
            filas == len(self.input_entries)
            and
            columnas == len(self.input_entries[0])
        )

        if not dimensiones_validas:
            place_msg_frame(
                parent_frame=self,
                msj_frame=self.mensaje_frame,
                msj="Las dimensiones de la matriz ingresada " +
                    "no coinciden con las dimensiones indicadas!",
                tipo="error",
                row=3,
            )
            return

        valores = []
        for fila_entries in self.input_entries:
            fila_valores = []
            for entry in fila_entries:
                try:
                    valor = Fraction(entry.get())
                except (ValueError, ZeroDivisionError) as e:
                    if isinstance(e, ValueError):
                        msj = "Todos los valores deben ser números racionales!"
                    else:
                        msj = "El denominador no puede ser 0!"
                    place_msg_frame(
                        parent_frame=self,
                        msj_frame=self.mensaje_frame,
                        msj=msj,
                        tipo="error",
                        row=3,
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
            nombre_nueva_matriz.isalpha() and
            nombre_nueva_matriz.isupper() and
            len(nombre_nueva_matriz) == 1
        )

        if not nombre_valido or nombre_repetido:
            msj = (
                "El nombre de la matriz debe ser una letra mayúscula!"
                if not nombre_valido
                else f"Ya existe una matriz nombrada '{nombre_nueva_matriz}'!"
            )

            place_msg_frame(
                parent_frame=self,
                msj_frame=self.mensaje_frame,
                msj=msj,
                tipo="error",
                row=3,
            )
            return

        self.mats_manager.mats_ingresadas[nombre_nueva_matriz] = nueva_matriz
        place_msg_frame(
            parent_frame=self,
            msj_frame=self.mensaje_frame,
            msj="La matriz se ha agregado exitosamente!",
            tipo="success",
            row=3,
        )

        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore
        self.master_frame.update_all()

    def validar_dimensiones(self) -> Optional[tuple[int, int]]:
        """
        Valida si las dimensiones ingresadas por el usuario
        son válidas y las retorna.

        Retorna una tupla con las filas y columnas
        si son válidas, o None si son inválidas.
        """

        try:
            filas = int(self.filas_entry.get())
            columnas = int(self.columnas_entry.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            place_msg_frame(
                parent_frame=self,
                msj_frame=self.mensaje_frame,
                msj="Debe ingresar números enteros " +
                    "positivos como filas y columnas!",
                tipo="error",
                row=1,
            )
            return None
        return (filas, columnas)

    def update_frame(self) -> None:
        """
        Actualiza los backgrounds de todas las widgets
        por si hubo cambio de modo de apariencia.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore
            if isinstance(widget, ctkFrame):
                for subwidget in widget.winfo_children():
                    subwidget.configure(bg_color="transparent")  # type: ignore


class MostrarMats(CustomScrollFrame):
    """
    Frame para mostrar las matrices guardadas.
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

        self.print_frame: Optional[ctkFrame] = None

        # definir los filtros que se mandaran
        # a self.mats_manager.get_matrices()
        self.opciones: dict[str, int] = {
            "Mostrar todas": -1,
            "Matrices ingresadas": 0,
            "Matrices calculadas": 1,
        }

        # crear widgets
        select_label = ctkLabel(self, text="Seleccione un filtro:")
        self.select_option = CustomDropdown(
            self,
            height=30,
            values=list(self.opciones.keys()),
            command=self.update_option,
        )

        self.opcion_seleccionada = self.opciones[self.select_option.get()]
        mostrar_button = IconButton(
            self,
            self.app,
            image=MOSTRAR_ICON,
            tooltip_text="Mostrar",
            command=self.show_mats
        )

        # colocar widgets
        select_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_option.grid(row=1, column=0, ipadx=10, padx=5, pady=5, sticky="e")
        mostrar_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def show_mats(self) -> None:
        """
        Muestra las matrices guardadas, usando el filtro seleccionado.
        """

        delete_msg_frame(self.print_frame)
        self.update_option(self.select_option.get())

        mats_text = self.mats_manager.get_matrices(self.opcion_seleccionada)
        if "!" in mats_text:  # "!" significa que no hay matrices
            place_msg_frame(
                parent_frame=self,
                msj_frame=self.print_frame,
                msj=mats_text,
                tipo="error",
                row=1,
                columnspan=2,
            )
        else:
            place_msg_frame(
                parent_frame=self,
                msj_frame=self.print_frame,
                msj=mats_text,
                tipo="resultado",
                row=1,
                columnspan=2,
            )
        self.print_frame.columnconfigure(0, weight=1)  # type: ignore

    def update_frame(self) -> None:
        """
        Eliminar self.print_frame y configurar los backgrounds.
        """

        # si print_frame no estaba inicializado,
        # .destroy() tira error, pero no pasa nada
        try:
            self.print_frame.destroy()  # type: ignore
        except AttributeError:
            pass
        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

    def update_option(self, valor: str) -> None:
        """
        Actualiza self.opcion_seleccionada
        con la opción seleccionada en el dropdown
        """

        self.opcion_seleccionada = self.opciones[valor]


class EliminarMats(CustomScrollFrame):
    """
    Frame para eliminar matrices.
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

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())
        self.mensaje_frame: Optional[Union[ErrorFrame, SuccessFrame]] = None
        self.select_mat: CustomDropdown
        self.mat_seleccionada = ""
        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Crear y colocar widgets del frame.
        """

        delete_msg_frame(self.mensaje_frame)
        if len(self.nombres_matrices) == 0:
            place_msg_frame(
                parent_frame=self,
                msj_frame=self.mensaje_frame,
                msj="No hay matrices guardadas!",
                tipo="error",
                row=1,
            )
            return

        instruct_eliminar = ctkLabel(self, text="¿Cuál matriz desea eliminar?")
        self.select_mat = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_matrices,
            command=self.update_mat,
        )

        button = IconButton(
            self,
            self.app,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar matriz",
            command=self.eliminar_matriz,
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

        place_msg_frame(
            parent_frame=self,
            msj_frame=self.mensaje_frame,
            msj=f"Matriz '{self.mat_seleccionada}' eliminada!",
            tipo="success",
            row=3,
            columnspan=2,
        )

        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore
        self.master_frame.update_all()

    def update_frame(self) -> None:
        """
        Actualiza el frame y sus datos.
        """

        self.nombres_matrices = list(self.mats_manager.mats_ingresadas.keys())

        if (
            len(self.nombres_matrices) == 0
            and
            isinstance(self.mensaje_frame, SuccessFrame)
        ):

            def clear_after_wait() -> None:
                delete_msg_frame(self.mensaje_frame)
                place_msg_frame(
                    parent_frame=self,
                    msj_frame=self.mensaje_frame,
                    msj="No hay matrices guardadas!",
                    tipo="error",
                )

                for widget in self.winfo_children():
                    if not isinstance(widget, ctkFrame):
                        widget.destroy()
            self.after(3000, clear_after_wait)

        elif isinstance(self.mensaje_frame, ErrorFrame):
            self.setup_frame()
        else:
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
            self.select_mat.configure(values=self.nombres_matrices)
            self.after(3000, lambda: delete_msg_frame(self.mensaje_frame))

    def update_mat(self, valor: str) -> None:
        """
        Actualiza mat_seleccionada con el valor seleccionado en el dropdown.
        """

        self.mat_seleccionada = valor
