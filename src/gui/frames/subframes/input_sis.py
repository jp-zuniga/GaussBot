"""
Implementación de los subframes de ManejarSistemas.
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
    generate_sep,
    place_msg_frame,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.frames import ManejarSistemas


class AgregarSistemas(CustomScrollFrame):
    """
    Frame para agregar nuevos sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarSistemas",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de agregar sistemas de ecuaciones.
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
        self.pre_sis_frame = CTkFrame(self, fg_color="transparent")
        self.sis_frame = CTkFrame(self, fg_color="transparent")
        self.post_sis_frame = CTkFrame(self, fg_color="transparent")
        self.nombre_entry: CustomEntry

        # crear widgets iniciales para las dimensiones
        ecuaciones_label = CTkLabel(self.pre_sis_frame, text="Ecuaciones:")
        variables_label = CTkLabel(self.pre_sis_frame, text="Variables:")

        self.ecuaciones_entry = CustomEntry(
            self.pre_sis_frame,
            width=60,
            placeholder_text="3",
        )

        self.variables_entry = CustomEntry(
            self.pre_sis_frame,
            width=60,
            placeholder_text="3",
        )

        ingresar_button = IconButton(
            self.pre_sis_frame,
            image=ENTER_ICON,
            tooltip_text="Ingresar datos del sistema",
            command=self.generar_casillas,
        )

        aleatorio_button = IconButton(
            self.pre_sis_frame,
            image=SHUFFLE_ICON,
            tooltip_text="Generar ecuaciones con coeficientes aleatorios",
            command=self.generar_aleatoria,
        )

        # crear bindings para todas las entries iniciales
        self.ecuaciones_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.ecuaciones_entry.bind("<Down>", lambda _: self.key_binder.focus_first())
        self.variables_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.variables_entry.bind("<Down>", lambda _: self.key_binder.focus_first())

        self.ecuaciones_entry.bind(
            "<Left>",
            lambda _: self.key_binder.focus_columnas(self.variables_entry),
        )

        self.ecuaciones_entry.bind(
            "<Right>",
            lambda _: self.key_binder.focus_columnas(self.variables_entry),
        )

        self.variables_entry.bind(
            "<Left>",
            lambda _: self.key_binder.focus_filas(self.ecuaciones_entry),
        )

        self.variables_entry.bind(
            "<Right>",
            lambda _: self.key_binder.focus_filas(self.ecuaciones_entry),
        )

        # colocar widgets
        self.pre_sis_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        ecuaciones_label.grid(row=0, column=0, padx=5, pady=5)
        self.ecuaciones_entry.grid(row=0, column=1, padx=5, pady=5)
        variables_label.grid(row=0, column=2, padx=5, pady=5)
        self.variables_entry.grid(row=0, column=3, padx=5, pady=5)
        ingresar_button.grid(row=0, column=4, padx=3, pady=5)
        aleatorio_button.grid(row=0, column=5, padx=3, pady=5)

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
        Generar casillas para ingresar un sistema con las dimensiones indicadas.
        """

        # si habian widgets debajo de
        # self.pre_sis_frame, borrarlos
        for widget in self.sis_frame.winfo_children():
            widget.destroy()
        for widget in self.post_sis_frame.winfo_children():
            widget.destroy()

        delete_msg_frame(self.msg_frame)
        try:
            ecuaciones, variables = self.validar_dimensiones()
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

        # crear separador para la columna de constantes
        sep_label = CTkLabel(
            self.sis_frame,
            text="",
            image=generate_sep(True, (8, 40 * ecuaciones)),
        )

        # crear entries para ingresar elementos
        self.input_entries.clear()
        for i in range(ecuaciones):
            fila_entries = []
            for j in range(variables):
                input_entry = CustomEntry(
                    self.sis_frame,
                    width=80,
                    placeholder_text=str(randint(-15, 15)),
                )

                if j != variables - 1:
                    input_entry.grid(row=i, column=j, padx=5, pady=5)
                else:
                    # si ya es la ultima columna, poner el separador primero
                    sep_label.grid(row=0, rowspan=ecuaciones, column=j, padx=3, pady=5)
                    input_entry.grid(row=i, column=j + 1, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        # crear post_sis_frame widgets
        nombre_label = CTkLabel(self.post_sis_frame, text="Nombre del sistema:")
        self.nombre_entry = CustomEntry(
            self.post_sis_frame,
            width=60,
            placeholder_text=choice(
                [
                    x
                    for x in ascii_uppercase
                    if x not in self.mats_manager.sis_ingresados.values()
                ],
            ),
        )

        agregar_button = IconButton(
            self.post_sis_frame,
            image=ACEPTAR_ICON,
            tooltip_text="Agregar sistema",
            command=self.agregar_sis,
        )

        limpiar_button = IconButton(
            self.post_sis_frame,
            image=LIMPIAR_ICON,
            tooltip_text="Limpiar casillas",
            command=self.limpiar_casillas,
        )

        # colocar parent frames
        self.sis_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n")

        self.post_sis_frame.grid(row=2, column=0, padx=5, pady=5, sticky="n")

        # colocar widgets
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        # configurar atributos de keybinder y crear bindings
        self.key_binder.entry_list = self.input_entries
        self.key_binder.extra_entries = (self.nombre_entry, self.ecuaciones_entry)
        self.key_binder.create_key_bindings()

        # encargarse de bindings de nombre_entry
        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
        self.nombre_entry.bind("<Return>", lambda _: self.agregar_sis())

    def generar_aleatoria(self) -> None:
        """
        Generar sistema con valores aleatorios.
        """

        self.generar_casillas()
        for fila_entries in self.input_entries:
            for entry in fila_entries:
                entry.insert(0, randint(-15, 15))

    def agregar_sis(self) -> None:
        """
        Agregar el sistema ingresado al diccionario de sistemas ingresados.
        """

        delete_msg_frame(self.msg_frame)
        try:
            ecuaciones, variables = self.validar_dimensiones()
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

        # si los inputs de ecuaciones/variables
        # cambiaron despues de generar las casillas
        dimensiones_validas = ecuaciones == len(
            self.input_entries,
        ) and variables == len(self.input_entries[0])

        if not dimensiones_validas:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="Las dimensiones del sistema ingresado "
                "no coinciden con las dimensiones indicadas.",
                tipo="error",
                row=3,
            )
            return
        delete_msg_frame(self.msg_frame)

        # recorrer las entries y guardar los valores
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

        nombre_nuevo_sis = self.nombre_entry.get()
        nuevo_sis = Matriz(
            aumentada=True,
            filas=ecuaciones,
            columnas=variables,
            valores=valores,
        )

        # validar nombre del sistema
        nombre_repetido = nombre_nuevo_sis in self.mats_manager.sis_ingresados
        nombre_valido = (
            nombre_nuevo_sis.isalpha()
            and nombre_nuevo_sis.isupper()
            and len(nombre_nuevo_sis) == 1
        )

        if not nombre_valido or nombre_repetido:
            msg = (
                "El nombre del sistema debe ser una letra mayúscula."
                if not nombre_valido
                else f"¡Ya existe un sistema nombrado {nombre_nuevo_sis}!"
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

        self.mats_manager.sis_ingresados[nombre_nuevo_sis] = nuevo_sis
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"¡El sistema {nombre_nuevo_sis} se ha agregado exitosamente!",
            tipo="success",
            row=3,
        )

        # mandar a actualizar los datos
        self.master_frame.update_all()
        self.app.sistemas.update_all()

    def validar_dimensiones(self) -> tuple[int, int]:
        """
        Validar dimensiones ingresadas.

        Returns:
            (int, int): Ecuaciones, variables.

        """

        ecuaciones = int(self.ecuaciones_entry.get())
        variables = int(self.variables_entry.get())

        if ecuaciones <= 0 or variables <= 0:
            raise ValueError(
                "Debe ingresar números enteros positivos como ecuaciones y variables.",
            )
        return (ecuaciones, variables)

    def update_frame(self) -> None:
        """
        Actualizar colores de widgets.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")
            if isinstance(widget, CTkFrame):
                for subwidget in widget.winfo_children():
                    subwidget.configure(bg_color="transparent")


class MostrarSistemas(CustomScrollFrame):
    """
    Frame para mostrar los sistemas guardados.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarSistemas",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de mostrar sistemas de ecuaciones.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.show_frame: CTkFrame | None = None

        # definir los filtros que se mandaran
        # a self.mats_manager.get_sistemas()
        self.opciones: dict[str, Literal[-1, 0, 1]] = {
            "Mostrar todos": -1,
            "Sistemas ingresados": 0,
            "Sistemas calculados": 1,
        }

        self.select_opcion: CustomDropdown
        self.opcion_seleccionada: Literal[-1, 0, 1] = -1

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar widgets del frame.
        """

        delete_msg_frame(self.show_frame)
        if len(self.mats_manager.sis_ingresados.keys()) == 0:
            self.show_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.show_frame,
                msg="¡No se ha guardado ningún sistema de ecuaciones!",
                tipo="error",
                columnspan=2,
            )

            return

        for widget in self.winfo_children():
            widget.destroy()

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
            command=self.mostrar_sis,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def mostrar_sis(self) -> None:
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
        sis_text = self.mats_manager.get_sistemas(self.opcion_seleccionada)
        self.show_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.show_frame,
            msg=sis_text,
            tipo="resultado",
            row=1,
            columnspan=2,
        )

        self.show_frame.columnconfigure(0, weight=1)

    def update_frame(self) -> None:
        """
        Eliminar self.show_frame y configurar backgrounds.
        """

        delete_msg_frame(self.show_frame)
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


class EliminarSistemas(CustomScrollFrame):
    """
    Frame para eliminar sistemas de ecuaciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarSistemas",
        mats_manager: MatricesManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de eliminar sistemas de ecuaciones.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.mats_manager = mats_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())
        self.msg_frame: CTkFrame | None = None

        self.select_sis: CustomDropdown
        self.sis_seleccionado = ""

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Crear y colocar las widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        if len(self.nombres_sistemas) == 0:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="¡No se ha guardado ningún sistema de ecuaciones!",
                tipo="error",
                columnspan=2,
            )

            return

        for widget in self.winfo_children():
            widget.destroy()

        # crear widgets
        instruct_eliminar = CTkLabel(self, text="¿Cuál sistema desea eliminar?")
        self.select_sis = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_sistemas,
            command=self.update_sis,
        )

        button = IconButton(
            self,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar sistema",
            command=self.eliminar_sis,
        )

        self.sis_seleccionado = self.select_sis.get()

        # colocar widgets
        instruct_eliminar.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="n",
        )
        self.select_sis.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_sis(self) -> None:
        """
        Eliminar sistema seleccionado.
        """

        delete_msg_frame(self.msg_frame)
        self.update_sis(self.select_sis.get())
        self.mats_manager.sis_ingresados.pop(self.sis_seleccionado)

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"¡Sistema {self.sis_seleccionado} eliminado!",
            tipo="success",
            row=2,
            columnspan=2,
        )

        self.master_frame.update_all()
        self.app.sistemas.update_all()

    def update_frame(self) -> None:
        """
        Actualizar frame y datos.
        """

        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        if len(self.nombres_sistemas) == 0 and isinstance(self.msg_frame, SuccessFrame):

            def clear_after_wait() -> None:
                delete_msg_frame(self.msg_frame)
                self.msg_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.msg_frame,
                    msg="¡No se ha guardado ningún sistema de ecuaciones!",
                    tipo="error",
                    columnspan=2,
                )

                for widget in self.winfo_children():
                    if not isinstance(widget, CTkFrame):
                        widget.destroy()

            self.after(1000, clear_after_wait)

        elif isinstance(self.msg_frame, ErrorFrame):
            self.setup_frame()

        else:
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")
            self.select_sis.configure(
                values=self.nombres_sistemas,
                variable=Variable(value=self.nombres_sistemas[0]),
            )

            self.after(1000, lambda: delete_msg_frame(self.msg_frame))

    def update_sis(self, valor: str) -> None:
        """
        Actualizar 'self.mat_seleccionada'.

        Args:
            valor: Selección del dropdown.

        """
        self.sis_seleccionado = valor
