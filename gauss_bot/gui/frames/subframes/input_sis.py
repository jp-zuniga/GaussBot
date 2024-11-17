"""
Implementación de los subframes de ManejarSistemas.
"""

from fractions import Fraction
from random import randint
from typing import (
    TYPE_CHECKING,
    Optional,
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

        self.key_binder = KeyBindingManager(es_matriz=True)
        self.mensaje_frame: Optional[ctkFrame] = None
        self.input_entries: list[list[CustomEntry]] = []

        # frames para contener secciones de la interfaz
        self.pre_sis_frame = ctkFrame(self, fg_color="transparent")
        self.sis_frame = ctkFrame(self, fg_color="transparent")
        self.post_sis_frame = ctkFrame(self, fg_color="transparent")
        self.nombre_entry: ctkEntry

        # crear widgets iniciales para las dimensiones
        ecuaciones_label = ctkLabel(self.pre_sis_frame, text="Ecuaciones:")
        variables_label = ctkLabel(self.pre_sis_frame, text="Variables:")

        self.ecuaciones_entry = ctkEntry(
            self.pre_sis_frame,
            width=30,
            placeholder_text="3"
        )

        self.variables_entry = ctkEntry(
            self.pre_sis_frame,
            width=30,
            placeholder_text="3"
        )

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

        # crear bindings para todas las entry's iniciales
        # para que se pueda navegar con las flechas
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

        # si habian widgets debajo de
        # self.pre_sis_frame, borrarlos
        for widget in self.sis_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.post_sis_frame.winfo_children():
            widget.destroy()  # type: ignore

        delete_msg_frame(self.mensaje_frame)
        try:
            ecuaciones, variables = self.validar_dimensiones()  # type: ignore
        except TypeError:
            # hubo input invalido
            return
        delete_msg_frame(self.mensaje_frame)

        # crear separador para la columna de constantes
        sep_label = ctkLabel(
            self.sis_frame,
            text="",
            image=generate_sep(True, (40, 40 * ecuaciones)),
        )

        # crear entries para ingresar elementos
        self.input_entries.clear()
        for i in range(ecuaciones):
            fila_entries = []
            for j in range(variables):
                input_entry = CustomEntry(
                    self.sis_frame,
                    width=60,
                    placeholder_text=randint(-15, 15)
                )

                if j != variables - 1:
                    input_entry.grid(row=i, column=j, padx=5, pady=5)
                else:
                    # si ya es la ultima columna, poner el separador primero
                    sep_label.grid(row=0, rowspan=ecuaciones, column=j, pady=5)
                    input_entry.grid(row=i, column=j + 1, padx=5, pady=5)
                fila_entries.append(input_entry)
            self.input_entries.append(fila_entries)

        # crear post_sis_frame widgets
        nombre_label = ctkLabel(self.post_sis_frame, text="Nombre del sistema:")
        self.nombre_entry = ctkEntry(
            self.post_sis_frame,
            width=30,
            placeholder_text="A",
        )

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

        # colocar parent frames
        self.sis_frame.grid(
            row=1, column=0,
            padx=5, pady=5,
            sticky="n",
        )

        self.post_sis_frame.grid(
            row=2, column=0,
            padx=5, pady=5,
            sticky="n",
        )

        # colocar widgets
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        # configurar atributos de keybinder y crear bindings
        self.key_binder.entry_list = self.input_entries  # type: ignore
        self.key_binder.extra_entries = (self.nombre_entry, self.ecuaciones_entry)  # type: ignore
        self.key_binder.create_key_bindings()

        # encargarse de bindings de nombre_entry
        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
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
            ecuaciones, variables = self.validar_dimensiones()  # type: ignore
        except TypeError:
            # hubo input invalido
            return
        delete_msg_frame(self.mensaje_frame)

        # si los inputs de ecuaciones/variables
        # cambiaron despues de generar las casillas
        dimensiones_validas = (
            ecuaciones == len(self.input_entries)
            and
            variables == len(self.input_entries[0])
        )

        if not dimensiones_validas:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg="Las dimensiones del sistema ingresado " +
                    "no coinciden con las dimensiones indicadas!",
                tipo="error",
                row=3,
            )
            return
        delete_msg_frame(self.mensaje_frame)

        # recorrer las entries y guardar los valores
        valores = []
        for fila_entries in self.input_entries:
            fila_valores = []
            for entry in fila_entries:
                try:
                    valor = Fraction(entry.get())
                except (ValueError, ZeroDivisionError) as e:
                    if isinstance(e, ValueError):
                        msg = "Todos los valores deben ser números racionales!"
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
                fila_valores.append(valor)
            valores.append(fila_valores)
        delete_msg_frame(self.mensaje_frame)

        nombre_nuevo_sis = self.nombre_entry.get()
        nuevo_sis = Matriz(
            aumentada=True, filas=ecuaciones,
            columnas=variables, valores=valores
        )

        # validar nombre del sistema
        nombre_repetido = nombre_nuevo_sis in self.mats_manager.sis_ingresados
        nombre_valido = (
            nombre_nuevo_sis.isalpha() and
            nombre_nuevo_sis.isupper() and
            len(nombre_nuevo_sis) == 1
        )

        if not nombre_valido or nombre_repetido:
            msg = (
                "El nombre del sistema debe ser una letra mayúscula!"
                if not nombre_valido
                else f"Ya existe un sistema nombrado '{nombre_nuevo_sis}'!"
            )

            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg=msg,
                tipo="error",
                row=3,
            )
            return
        delete_msg_frame(self.mensaje_frame)

        self.mats_manager.sis_ingresados[nombre_nuevo_sis] = nuevo_sis
        self.mensaje_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.mensaje_frame,
            msg="El sistema se ha agregado exitosamente!",
            tipo="success",
            row=3,
        )

        # mandar a actualizar los datos
        self.master_frame.update_all()
        self.app.sistemas.update_frame()  # type: ignore

    def validar_dimensiones(self) -> Optional[tuple[int, int]]:
        """
        Valida si las dimensiones ingresadas por el usuario
        son válidas y las retorna.

        Retorna una tupla con las ecuaciones y variables
        si son válidas, o None si son inválidas.
        """

        try:
            ecuaciones = int(self.ecuaciones_entry.get())
            variables = int(self.variables_entry.get()) + 1
            if ecuaciones <= 0 or variables - 1 <= 0:
                raise ValueError
        except ValueError:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg="Debe ingresar números enteros " +
                    "positivos como ecuaciones y variables!",
                tipo="error",
                row=1,
            )
            return None
        return (ecuaciones, variables)

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


class MostrarSistemas(CustomScrollFrame):
    """
    Frame para mostrar los sistemas guardados.
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

        self.print_frame: Optional[ctkFrame] = None

        # definir los filtros que se mandaran
        # a self.mats_manager.get_sistemas()
        self.opciones: dict[str, int] = {
            "Mostrar todos": -1,
            "Sistemas ingresados": 0,
            "Sistemas calculados": 1,
        }

        # crear widgets
        select_label = ctkLabel(self, text="Seleccione un filtro:")
        self.select_opcion = CustomDropdown(
            self,
            height=30,
            values=list(self.opciones.keys()),
            command=self.update_opcion,
        )

        self.opcion_seleccionada = self.opciones[self.select_opcion.get()]
        mostrar_button = IconButton(
            self,
            self.app,
            image=MOSTRAR_ICON,
            tooltip_text="Mostrar",
            command=self.mostrar_sis
        )

        # colocar widgets
        select_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
        self.select_opcion.grid(row=1, column=0, ipadx=10, padx=5, pady=5, sticky="e")
        mostrar_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def mostrar_sis(self) -> None:
        """
        Muestra los sistemas guardados, usando el filtro seleccionado.
        """

        delete_msg_frame(self.print_frame)
        self.update_opcion(self.select_opcion.get())

        sis_text = self.mats_manager.get_sistemas(self.opcion_seleccionada)
        if "!" in sis_text:
            self.print_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.print_frame,
                msg=sis_text,
                tipo="error",
                row=2,
                columnspan=2,
            )
        else:
            self.print_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.print_frame,
                msg=sis_text,
                tipo="resultado",
                row=2,
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

    def update_opcion(self, valor: str) -> None:
        """
        Actualiza self.opcion_seleccionada
        con la opción seleccionada en el dropdown
        """

        self.opcion_seleccionada = self.opciones[valor]


class EliminarSistemas(CustomScrollFrame):
    """
    Frame para eliminar sistemas de ecuaciones.
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

        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())
        self.mensaje_frame: Optional[ctkFrame] = None
        self.select_sis: CustomDropdown
        self.sis_seleccionado = ""
        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Crear y colocar las widgets del frame.
        """

        delete_msg_frame(self.mensaje_frame)
        if len(self.nombres_sistemas) == 0:
            self.mensaje_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.mensaje_frame,
                msg="No hay sistemas de ecuaciones guardados!",
                tipo="error",
                row=0,
                columnspan=2,
            )
            return

        # crear widgets
        instruct_eliminar = ctkLabel(self, text="¿Cuál sistema desea eliminar?")
        self.select_sis = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_sistemas,
            command=self.update_sis,
        )

        button = IconButton(
            self,
            self.app,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar sistema",
            command=self.eliminar_sis,
        )

        self.sis_seleccionado = self.select_sis.get()

        # colocar widgets
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

        self.mensaje_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.mensaje_frame,
            msg=f"Sistema '{self.sis_seleccionado}' eliminado!",
            tipo="success",
            row=2,
            columnspan=2,
        )

        self.master_frame.update_all()
        self.app.sistemas.update_frame()  # type: ignore

    def update_frame(self) -> None:
        """
        Actualiza el frame y sus datos.
        """

        self.nombres_sistemas = list(self.mats_manager.sis_ingresados.keys())

        if (
            len(self.nombres_sistemas) == 0
            and
            isinstance(self.mensaje_frame, SuccessFrame)
        ):

            def clear_after_wait() -> None:
                delete_msg_frame(self.mensaje_frame)
                self.mensaje_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.mensaje_frame,
                    msg="No hay sistemas guardados!",
                    tipo="error",
                    row=0,
                    columnspan=2,
                )

                for widget in self.winfo_children():
                    if not isinstance(widget, ctkFrame):
                        widget.destroy()
            self.after(2000, clear_after_wait)

        elif isinstance(self.mensaje_frame, ErrorFrame):
            self.setup_frame()
        else:
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
            self.select_sis.configure(
                variable=Variable(value=self.nombres_sistemas[0]),
                values=self.nombres_sistemas
            )

            self.after(2000, lambda: delete_msg_frame(self.mensaje_frame))

    def update_sis(self, valor: str) -> None:
        """
        Actualiza sis_seleccionado con el valor seleccionado en el dropdown.
        """

        self.sis_seleccionado = valor
