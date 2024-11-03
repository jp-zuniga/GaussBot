"""
Implementación de los subframes de ManejarVecs.
"""

from fractions import Fraction
from random import randint
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from tkinter import Variable, TclError
from customtkinter import (
    CTkBaseClass as ctkBase,
    CTkButton as ctkButton,
    CTkEntry as ctkEntry,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from gauss_bot.models.vector import Vector
from gauss_bot.managers.vecs_manager import VectoresManager

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
    from gauss_bot.gui.frames.inputs import ManejarVecs


class AgregarVecs(CustomScrollFrame):
    """
    Frame para agregar un vector a la lista de vectores ingresados,
    ingresando datos manualmente o generándolos aleatoriamente.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarVecs",
        vecs_manager: VectoresManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[CustomEntry] = []
        self.post_vector_widgets: list[ctkBase] = []

        dimension_label = ctkLabel(self, text="Dimensiones del vector:")
        self.dimension_entry = ctkEntry(self, width=60)

        generar_button = ctkButton(
            self, height=30, text="Ingresar datos", command=self.generar_casillas
        )

        aleatorio_button = ctkButton(
            self, height=30, text="Generar vector aleatorio", command=self.generar_aleatorio
        )

        self.vector_frame = ctkFrame(self)

        self.dimension_entry.bind("<Return>", lambda x: self.generar_casillas())
        self.dimension_entry.bind("<Down>", lambda x: self.dimensiones_move_down())

        dimension_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.dimension_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        generar_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        aleatorio_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.vector_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ns")
        self.update_scrollbar_visibility()

    def limpiar_casillas(self) -> None:
        """
        Borra todos los valores ingresados en las casillas del vector.
        """

        for entry in self.input_entries:
            entry.delete(0, "end")
        self.input_entries.clear()
        try:
            self.nombre_entry.delete(0, "end")
        except AttributeError:
            pass

    def generar_casillas(self) -> None:
        """
        Genera las casillas para ingresar los valores del vector.
        """

        try:
            self.limpiar_casillas()
            for widget in self.vector_frame.winfo_children():
                widget.destroy()  # type: ignore
            for widget in self.post_vector_widgets:
                widget.destroy()
        except TclError:
            pass

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        try:
            dimension = int(self.dimension_entry.get())
            if dimension <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar un número entero positivo como dimensión!"
            )
            self.mensaje_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        for i in range(dimension):
            input_entry = CustomEntry(self.vector_frame, width=60)
            input_entry.grid(row=i, column=0, padx=5, pady=5)
            self.bind_entry_keys(input_entry, i)
            self.input_entries.append(input_entry)

        nombre_label = ctkLabel(self, text="Nombre del vector:")
        self.nombre_entry = ctkEntry(self, width=25, placeholder_text="u")
        agregar_button = ctkButton(self, height=30, text="Agregar", command=self.agregar_vector)
        limpiar_button = ctkButton(
            self, height=30, text="Limpiar casillas", command=self.limpiar_casillas
        )

        nombre_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        agregar_button.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        limpiar_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.nombre_entry.bind("<Up>", lambda x: self.nombre_entry_up())
        self.nombre_entry.bind("<Return>", lambda x: self.agregar_vector())
        self.update_scrollbar_visibility()

        self.post_vector_widgets = [
            nombre_label,
            self.nombre_entry,
            agregar_button,
            limpiar_button,
        ]

    def generar_aleatorio(self) -> None:
        """
        Genera casillas con valores aleatorios para el vector.
        """

        self.generar_casillas()
        for entry in self.input_entries:
            entry.delete(0, "end")
            entry.insert(0, str(randint(-15, 15)))

    def agregar_vector(self) -> None:
        """
        Crea un vector con los datos ingresados, y lo agrega al diccionario.
        """

        try:
            dimension = int(self.dimension_entry.get())
            if dimension <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar un número entero positivo como dimensión!"
            )
            self.mensaje_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        input_d = len(self.input_entries)
        if dimension != input_d:
            self.mensaje_frame = ErrorFrame(
                self,
                "Las dimensiones del vector ingresado no coinciden con las dimensions indicadas!",
            )
            self.mensaje_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        componentes = []
        for entry in self.input_entries:
            try:
                valor = Fraction(entry.get())
            except ValueError:
                self.mensaje_frame = ErrorFrame(
                    self, "Todos los valores deben ser números racionales!"
                )
                self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
                self.update_scrollbar_visibility()
                return
            except ZeroDivisionError:
                self.mensaje_frame = ErrorFrame(self, "El denominador no puede ser 0!")
                self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
                self.update_scrollbar_visibility()
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
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return
        if nombre_nuevo_vector in self.vecs_manager.vecs_ingresados:
            self.mensaje_frame = ErrorFrame(
                self, f"Ya existe un vector llamado '{nombre_nuevo_vector}'!"
            )
            self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.vecs_manager.vecs_ingresados[nombre_nuevo_vector] = nuevo_vector
        self.mensaje_frame = SuccessFrame(self, "El vector se ha agregado exitosamente!")
        self.mensaje_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()
        self.master_frame.update_all()
        self.app.vectores.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore

    def dimensiones_move_down(self) -> None:
        if len(self.vector_frame.winfo_children()) != 0:
            self.input_entries[0].focus_set()

    def bind_entry_keys(self, entry: CustomEntry, i: int) -> None:
        entry.bind("<Up>", lambda event: self.entry_move_up(i))
        entry.bind("<Down>", lambda event: self.entry_move_down(i))

    def entry_move_up(self, i: int) -> None:
        if i > 0:
            self.input_entries[i - 1].focus_set()
        elif i == 0:
            self.dimension_entry.focus_set()

    def entry_move_down(self, i: int) -> None:
        if i < len(self.input_entries) - 1:
            self.input_entries[i + 1].focus_set()
        elif i == len(self.input_entries) - 1:
            self.nombre_entry.focus_set()

    def nombre_entry_up(self) -> None:
        self.input_entries[-1].focus_set()

    def update_frame(self) -> None:
        self.update_idletasks()


class MostrarVecs(CustomScrollFrame):
    """
    Frame para mostrar todos los vectores ingresados por el usuario.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarVecs",
        vecs_manager: VectoresManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        self.options: dict[str, int] = {
            "Mostrar todos": -1,
            "Vectores ingresados": 0,
            "Vectores calculados": 1
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
        calculado = self.option_seleccionada
        vecs_text: str = self.vecs_manager.get_vectores(calculado)

        if self.print_frame is not None:
            self.print_frame.destroy()
            self.print_frame = None

        if vecs_text.startswith("No"):
            self.print_frame = ErrorFrame(self.mostrar_frame, vecs_text)
            self.print_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        else:
            self.print_frame = ResultadoFrame(
                self.mostrar_frame, header=vecs_text, resultado="", solo_header=True
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


class EliminarVecs(CustomScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarVecs",
        vecs_manager: VectoresManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())

        if len(self.nombres_vectores) > 0:
            placeholder = Variable(self, value=self.nombres_vectores[0])
        else:
            placeholder = None

        self.mensaje_frame: Optional[ctkFrame] = None
        self.instruct_eliminar = ctkLabel(self, text="¿Cuál vector desea eliminar?")

        self.select_vec = CustomDropdown(
            self,
            width=60,
            height=30,
            values=self.nombres_vectores,
            variable=placeholder,
            command=self.update_vec,
        )

        self.button = ctkButton(
            self,
            height=30,
            text="Eliminar",
            command=lambda: self.eliminar_vector(self.vec_seleccionada),
        )

        self.vec_seleccionada = self.select_vec.get()

        if len(self.nombres_vectores) == 0:
            self.mensaje_frame = ErrorFrame(
                self, "No hay vectores guardados!"
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            self.update_scrollbar_visibility()
            return

        self.instruct_eliminar.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.select_vec.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()

    def eliminar_vector(self, nombre_vec: str) -> None:
        """
        Elimina el vector seleccionado.
        """

        if self.mensaje_frame is not None:
            self.mensaje_frame.destroy()
            self.mensaje_frame = None

        self.update_vec(self.select_vec.get())
        self.vecs_manager.vecs_ingresados.pop(self.vec_seleccionada)

        self.mensaje_frame = SuccessFrame(
            self, message=f"Vector '{self.vec_seleccionada}' eliminado!"
        )
        self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5)
        self.update_scrollbar_visibility()
        self.master_frame.update_all()
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore

    def update_frame(self) -> None:
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())

        if len(self.nombres_vectores) == 0:
            if isinstance(self.mensaje_frame, ErrorFrame):
                return
            for widget in self.winfo_children():
                if isinstance(widget, SuccessFrame):
                    old_mensaje_frame = SuccessFrame(self, widget.mensaje_exito.cget("text"))
                widget.destroy()
            old_mensaje_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.mensaje_frame = ErrorFrame(self, "No hay vectores guardados!")
            self.after(500, self.mensaje_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n"))

        elif len(self.nombres_vectores) > 0:
            placeholder = Variable(self, value=self.nombres_vectores[0])
            self.instruct_eliminar = ctkLabel(self, text="¿Cuál vector desea eliminar?")
            self.select_vec = CustomDropdown(
                self,
                width=60,
                height=30,
                values=self.nombres_vectores,
                variable=placeholder,
                command=self.update_vec,
            )

            self.button = ctkButton(
                self,
                height=30,
                text="Eliminar",
                command=lambda: self.eliminar_vector(self.vec_seleccionada),
            )

            if isinstance(self.mensaje_frame, ErrorFrame):
                self.mensaje_frame.destroy()
                self.mensaje_frame = None

            self.update_vec(self.select_vec.get())
            self.instruct_eliminar.grid(row=0, column=0, padx=5, pady=5, sticky="n")
            self.select_vec.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            self.button.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        self.update_scrollbar_visibility()
        self.update_idletasks()

    def update_vec(self, valor: str) -> None:
        self.vec_seleccionada = valor
