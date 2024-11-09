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

from gauss_bot.models import Vector
from gauss_bot.managers import VectoresManager
from gauss_bot.gui.custom import (
    CustomEntry,
    CustomDropdown,
    CustomScrollFrame,
    IconButton,
    ErrorFrame,
    SuccessFrame,
    ResultadoFrame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import ManejarVecs


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

        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[CustomEntry] = []

        self.pre_vec_frame = ctkFrame(self)
        self.vector_frame = ctkFrame(self)
        self.post_vec_frame = ctkFrame(self)
        self.nombre_entry: ctkEntry

        dimension_label = ctkLabel(self.pre_vec_frame, text="Dimensiones:")
        self.dimension_entry = ctkEntry(self.pre_vec_frame, width=30, placeholder_text="3")

        ingresar_button = IconButton(
            self.pre_vec_frame, self.app,
            image=ENTER_ICON,
            command=self.generar_casillas
        )

        aleatorio_button = IconButton(
            self.pre_vec_frame, self.app,
            image=SHUFFLE_ICON,
            command=self.generar_aleatorio
        )

        self.dimension_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.dimension_entry.bind("<Down>", lambda _: self.move_down())

        self.pre_vec_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        dimension_label.grid(row=0, column=0, padx=5, pady=5)
        self.dimension_entry.grid(row=0, column=1, padx=5, pady=5)
        ingresar_button.grid(row=0, column=2, padx=5, pady=5)
        aleatorio_button.grid(row=0, column=3, padx=5, pady=5)

    def limpiar_casillas(self) -> None:
        """
        Borra todos los valores ingresados en las casillas del vector.
        """

        for entry in self.input_entries:
            entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")

    def generar_casillas(self) -> None:
        """
        Genera las casillas para ingresar los valores del vector.
        """

        for widget in self.vector_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.post_vec_frame.winfo_children():
            widget.destroy()

        delete_msg_frame(self.mensaje_frame)
        try:
            dimension = int(self.dimension_entry.get())
            if dimension <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar un número entero positivo como dimensión!"
            )
            self.mensaje_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            return
        delete_msg_frame(self.mensaje_frame)

        self.input_entries.clear()
        self.input_entries = []
        for i in range(dimension):
            input_entry = CustomEntry(self.vector_frame, width=60)
            input_entry.grid(row=i, column=0, padx=5, pady=5)
            self.bind_entry_keys(input_entry, i)
            self.input_entries.append(input_entry)

        nombre_label = ctkLabel(self.post_vec_frame, text="Nombre del vector:")
        self.nombre_entry = ctkEntry(self.post_vec_frame, width=30, placeholder_text="u")

        agregar_button = IconButton(
            self.post_vec_frame, self.app,
            image=ACEPTAR_ICON,
            command=self.agregar_vector
        )

        limpiar_button = IconButton(
            self.post_vec_frame, self.app,
            image=LIMPIAR_ICON,
            command=self.limpiar_casillas
        )

        self.vector_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.post_vec_frame.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        self.nombre_entry.bind("<Up>", lambda _: self.nombre_entry_up())
        self.nombre_entry.bind("<Return>", lambda _: self.agregar_vector())

    def generar_aleatorio(self) -> None:
        """
        Genera casillas con valores aleatorios para el vector.
        """

        self.generar_casillas()
        for entry in self.input_entries:
            entry.insert(0, str(randint(-15, 15)))

    def agregar_vector(self) -> None:
        """
        Crea un vector con los datos ingresados, y lo agrega al diccionario.
        """

        delete_msg_frame(self.mensaje_frame)
        try:
            dimension = int(self.dimension_entry.get())
            if dimension <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar un número entero positivo como dimensión!"
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        input_d = len(self.input_entries)
        if dimension != input_d:
            self.mensaje_frame = ErrorFrame(
                self,
                "Las dimensiones del vector ingresado no coinciden con las dimensions indicadas!",
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        delete_msg_frame(self.mensaje_frame)
        componentes = []
        for entry in self.input_entries:
            try:
                valor = Fraction(entry.get())
            except ValueError:
                self.mensaje_frame = ErrorFrame(
                    self, "Todos los valores deben ser números racionales!"
                )
                self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
                return
            except ZeroDivisionError:
                self.mensaje_frame = ErrorFrame(self, "El denominador no puede ser 0!")
                self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
                return
            componentes.append(valor)
        delete_msg_frame(self.mensaje_frame)

        nombre_nuevo_vector = self.nombre_entry.get()
        nuevo_vector = Vector(componentes)

        nombre_repetido = nombre_nuevo_vector in self.vecs_manager.vecs_ingresados
        nombre_valido = (
            nombre_nuevo_vector.isalpha()
            and nombre_nuevo_vector.islower()
            and len(nombre_nuevo_vector) == 1
        )

        if not nombre_valido or nombre_repetido:
            msj = (
                "El nombre del vector debe ser una letra minúscula!"
                if not nombre_valido
                else f"Ya existe un vector con nombrada {nombre_nuevo_vector}!"
            )

            self.mensaje_frame = ErrorFrame(self, msj)
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        self.vecs_manager.vecs_ingresados[nombre_nuevo_vector] = nuevo_vector
        self.mensaje_frame = SuccessFrame(self, "El vector se ha agregado exitosamente!")
        self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.master_frame.update_all()
        self.app.vectores.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore

    def move_down(self) -> None:
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
        self.columnconfigure(1, weight=1)

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
        mostrar_button = IconButton(
            self, self.app,
            image=MOSTRAR_ICON,
            command=self.setup_mostrar
        )

        self.print_frame: Optional[Union[ErrorFrame, ResultadoFrame]] = None

        select_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_option.grid(row=1, column=0, ipadx=10, padx=5, pady=5, sticky="e")
        mostrar_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def setup_mostrar(self) -> None:
        delete_msg_frame(self.print_frame)
        self.update_option(self.select_option.get())

        calculado = self.option_seleccionada
        vecs_text: str = self.vecs_manager.get_vectores(calculado)

        if "!" in vecs_text:
            self.print_frame = ErrorFrame(self, vecs_text)
            self.print_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")
        else:
            self.print_frame = ResultadoFrame(
                self,
                header=vecs_text,
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
        self.columnconfigure(1, weight=1)

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_vec: CustomDropdown
        self.vec_seleccionado = ""
        self.setup_frame()

    def setup_frame(self) -> None:
        delete_msg_frame(self.mensaje_frame)
        if len(self.nombres_vectores) == 0:
            if isinstance(self.mensaje_frame, ErrorFrame):
                return
            self.mensaje_frame = ErrorFrame(self, "No hay vectores guardados!")
            self.mensaje_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            return

        placeholder = Variable(self, value=self.nombres_vectores[0])
        instruct_eliminar = ctkLabel(self, text="¿Cuál vector desea eliminar?")

        self.select_vec = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_vectores,
            variable=placeholder,
            command=self.update_vec,
        )

        button = IconButton(
            self, self.app,
            image=ELIMINAR_ICON,
            command=lambda: self.eliminar_vector(),
        )

        self.vec_seleccionado = self.select_vec.get()

        instruct_eliminar.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_vec.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_vector(self) -> None:
        """
        Elimina el vector seleccionado.
        """

        delete_msg_frame(self.mensaje_frame)
        self.update_vec(self.select_vec.get())
        self.vecs_manager.vecs_ingresados.pop(self.vec_seleccionada)

        self.mensaje_frame = SuccessFrame(
            self, message=f"Vector '{self.vec_seleccionada}' eliminado!"
        )

        self.mensaje_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.master_frame.update_all()
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore

    def update_frame(self) -> None:
        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        if len(self.nombres_vectores) == 0 and isinstance(self.mensaje_frame, SuccessFrame):
            SuccessFrame(
                self, self.mensaje_frame.mensaje_exito.cget("text")
            ).grid(row=0, column=0, padx=5, columnspan=2, pady=5, sticky="n")

            delete_msg_frame(self.mensaje_frame)
            self.mensaje_frame = ErrorFrame(self, "No hay vectores guardados!")
            self.after(
                1000,
                self.mensaje_frame.grid(
                    row=1, column=0,
                    columnspan=2,
                    padx=5, pady=5,
                    sticky="n"
                ),
            )

            for widget in self.winfo_children():
                if not isinstance(widget, ctkFrame):
                    widget.destroy()

        elif isinstance(self.mensaje_frame, ErrorFrame):
            self.setup_frame()
        else:
            self.select_vec.configure(values=self.nombres_vectores)
            self.select_vec.configure(variable=Variable(value=self.nombres_vectores[0]))

    def update_vec(self, valor: str) -> None:
        self.vec_seleccionada = valor
