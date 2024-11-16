"""
Implementación de los subframes de ManejarSistemas.
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
    generate_sep,
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
    from gauss_bot.gui.frames import ManejarSistemas


class AgregarSistemas(CustomScrollFrame):
    """
    Frame para agregar un nuevo sistema.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarSistemas",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)

        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[list[CustomEntry]] = []

        self.pre_sis_frame = ctkFrame(self)
        self.sis_frame = ctkFrame(self)
        self.post_sis_frame = ctkFrame(self)
        self.nombre_entry: ctkEntry

        ecuas_label = ctkLabel(self.pre_sis_frame, text="Ecuaciones:")
        self.ecuas_entry = ctkEntry(self.pre_sis_frame, width=30, placeholder_text="3")
        vars_label = ctkLabel(self.pre_sis_frame, text="Variables:")
        self.vars_entry = ctkEntry(self.pre_sis_frame, width=30, placeholder_text="3")

        ingresar_button = IconButton(
            self.pre_sis_frame,
            self.app,
            image=ENTER_ICON,
            tooltip_text="Ingresar datos del sistema",
            command=self.generar_casillas
        )

        aleatorio_button = IconButton(
            self.pre_sis_frame,
            self.app,
            image=SHUFFLE_ICON,
            tooltip_text="Generar ecuaciones con coeficientes aleatorios",
            command=self.generar_aleatoria,
        )

        self.ecuas_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.ecuas_entry.bind("<Left>", lambda _: self.focus_set_vars())
        self.ecuas_entry.bind("<Right>", lambda _: self.focus_set_vars())
        self.ecuas_entry.bind("<Down>", lambda _: self.move_down())
        self.vars_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.vars_entry.bind("<Left>", lambda _: self.focus_set_ecuas())
        self.vars_entry.bind("<Right>", lambda _: self.focus_set_ecuas())
        self.vars_entry.bind("<Down>", lambda _: self.move_down())

        self.pre_sis_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        ecuas_label.grid(row=0, column=0, padx=5, pady=5)
        self.ecuas_entry.grid(row=0, column=1, padx=5, pady=5)
        vars_label.grid(row=0, column=2, padx=5, pady=5)
        self.vars_entry.grid(row=0, column=3, padx=5, pady=5)
        ingresar_button.grid(row=0, column=4, padx=3, pady=5)
        aleatorio_button.grid(row=0, column=5, padx=3, pady=5)

    def limpiar_casillas(self) -> None:
        """
        Borra todos los valores ingresados en las casillas del sistema.
        """

        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")

    def generar_casillas(self) -> None:
        """
        Genera casillas para ingresar un sistema con las dimensiones indicadas.
        """

        for widget in self.sis_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.post_sis_frame.winfo_children():
            widget.destroy()

        delete_msg_frame(self.mensaje_frame)
        try:
            eqts = int(self.ecuas_entry.get())
            vars = int(self.vars_entry.get()) + 1
            if eqts <= 0 or vars - 1 <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos como ecuaciones y variables!"
            )
            self.mensaje_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n")
            return
        delete_msg_frame(self.mensaje_frame)

        sep_label = ctkLabel(
            self.sis_frame,
            text="",
            image=generate_sep(True, (40, 40 * eqts))
        )

        self.input_entries.clear()
        self.input_entries = []
        for i in range(eqts):
            fila_entries = []
            for j in range(vars):
                input_entry = CustomEntry(self.sis_frame, width=60)
                if j != vars - 1:
                    input_entry.grid(row=i, column=j, padx=5, pady=5)
                else:
                    sep_label.grid(row=0, rowspan=eqts, column=j, pady=5)
                    input_entry.grid(row=i, column=j + 1, padx=5, pady=5)
                self.bind_entry_keys(input_entry, i, j)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        nombre_label = ctkLabel(self.post_sis_frame, text="Nombre del sistema:")
        self.nombre_entry = ctkEntry(self.post_sis_frame, width=30, placeholder_text="A")

        agregar_button = IconButton(
            self.post_sis_frame,
            self.app,
            image=ACEPTAR_ICON,
            tooltip_text="Agregar sistema",
            command=self.agregar_sis
        )

        limpiar_button = IconButton(
            self.post_sis_frame,
            self.app,
            image=LIMPIAR_ICON,
            tooltip_text="Limpiar casillas",
            command=self.limpiar_casillas
        )

        self.sis_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.post_sis_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        self.nombre_entry.bind("<Up>", lambda _: self.nombre_entry_up())
        self.nombre_entry.bind("<Return>", lambda _: self.agregar_sis())

    def generar_aleatoria(self) -> None:
        """
        Genera un sistema de las dimensiones indicadas,
        con valores enteros aleatorios.
        """

        self.generar_casillas()
        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.insert(0, randint(-15, 15))

    def agregar_sis(self) -> None:
        """
        Agrega el sistema ingresado a la lista de sistemas ingresados.
        """

        delete_msg_frame(self.mensaje_frame)
        try:
            eqts = int(self.ecuas_entry.get())
            vars = int(self.vars_entry.get()) + 1
            if eqts <= 0 or vars - 1 <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = ErrorFrame(
                self, "Debe ingresar números enteros positivos como ecuaciones y variables!"
            )
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        input_f = len(self.input_entries)
        input_c = len(self.input_entries[0])
        dimensiones_validas = (
            eqts == input_f and vars == input_c
        )

        if not dimensiones_validas:
            self.mensaje_frame = ErrorFrame(
                self,
                "Las dimensiones del sistema ingresado no coinciden con las dimensiones indicadas!"
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
        nombre_nuevo_sis = self.nombre_entry.get()
        nuevo_sis = Matriz(
            aumentada=True, filas=eqts,
            columnas=vars, valores=valores
        )

        nombre_repetido = nombre_nuevo_sis in self.mats_manager.sis_ingresados
        nombre_valido = (
            nombre_nuevo_sis.isalpha()
            and nombre_nuevo_sis.isupper()
            and len(nombre_nuevo_sis) == 1
        )

        if not nombre_valido or nombre_repetido:
            msj = (
                "El nombre del sistema debe ser una letra mayúscula!"
                if not nombre_valido
                else f"Ya existe un sistema nombrado '{nombre_nuevo_sis}'!"
            )

            self.mensaje_frame = ErrorFrame(self, msj)
            self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
            return

        self.mats_manager.sis_ingresados[nombre_nuevo_sis] = nuevo_sis
        self.mensaje_frame = SuccessFrame(
            self, "El sistema se ha agregado exitosamente!"
        )

        self.mensaje_frame.grid(row=3, column=0, padx=5, pady=5, sticky="n")
        self.master_frame.update_all()
        self.app.sistemas.update_frame()  # type: ignore

    def focus_set_vars(self) -> None:
        self.vars_entry.focus_set()

    def focus_set_ecuas(self) -> None:
        self.ecuas_entry.focus_set()

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
            self.focus_set_ecuas()

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


class MostrarSistemas(CustomScrollFrame):
    """
    Frame para mostrar todos los sitemas ingresados.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarSistemas",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.options: dict[str, int] = {
            "Mostrar todos": -1,
            "Sistemas ingresados": 0,
            "Sistemas calculados": 1,
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

        calculado = self.option_seleccionada
        sis_text = self.mats_manager.get_sistemas(calculado)

        if "!" in sis_text:
            self.print_frame = ErrorFrame(self, sis_text)
            self.print_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")
        else:
            self.print_frame = ResultadoFrame(
                self,
                header=sis_text,
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


class EliminarSistemas(CustomScrollFrame):
    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarSistemas",
        mats_manager: MatricesManager
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        self.mensaje_frame: Optional[Union[ErrorFrame, SuccessFrame]] = None
        self.select_sis: CustomDropdown
        self.sis_seleccionado = ""
        self.setup_frame()

    def setup_frame(self) -> None:
        delete_msg_frame(self.mensaje_frame)
        if len(self.nombres_sistemas) == 0:
            self.mensaje_frame = ErrorFrame(self, "No hay sistemas guardados!")
            self.mensaje_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            return

        placeholder = Variable(self, value=self.nombres_sistemas[0])
        instruct_eliminar = ctkLabel(self, text="¿Cuál sistema desea eliminar?")

        self.select_sis = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_sistemas,
            variable=placeholder,
            command=self.update_sis,
        )

        button = IconButton(
            self,
            self.app,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar sistema",
            command=lambda: self.eliminar_sis(),
        )

        self.sis_seleccionado = self.select_sis.get()

        instruct_eliminar.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_sis.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_sis(self) -> None:
        """
        Elimina el sistema seleccionado.
        """

        delete_msg_frame(self.mensaje_frame)
        self.update_sis(self.select_sis.get())
        self.mats_manager.sis_ingresados.pop(self.sis_seleccionado)

        self.mensaje_frame = SuccessFrame(
            self,
            message=f"Sistema '{self.sis_seleccionado}' eliminado!"
        )

        self.mensaje_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.master_frame.update_all()
        self.app.sistemas.update_frame()  # type: ignore

    def update_frame(self) -> None:
        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())
        if len(self.nombres_sistemas) == 0 and isinstance(self.mensaje_frame, SuccessFrame):
            sleep(2.0)
            delete_msg_frame(self.mensaje_frame)
            self.mensaje_frame = ErrorFrame(self, "No hay sistemas guardados!")
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
            self.select_sis.configure(
                variable=Variable(value=self.nombres_sistemas[0]),
                values=self.nombres_sistemas,
            )
            self.after(2000, lambda: delete_msg_frame(self.mensaje_frame))

    def update_sis(self, valor: str) -> None:
        self.sis_seleccionado = valor
