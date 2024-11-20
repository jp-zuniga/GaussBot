"""
Implementación de los subframes de ManejarFuncs.
"""

from typing import (
    TYPE_CHECKING,
    Optional,
)

from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from gauss_bot import (
    INFO_ICON,
    delete_msg_frame,
)

from gauss_bot.models import Func
from gauss_bot.managers import (
    FuncManager,
    KeyBindingManager,
)

from gauss_bot.gui.custom import (
    CustomEntry,
    CustomNumpad,
    CustomScrollFrame,
    IconButton,
    place_msg_frame,
)

if TYPE_CHECKING:
    from gauss_bot.gui import GaussUI
    from gauss_bot.gui.frames import ManejarFuncs


class AgregarFuncs(CustomScrollFrame):
    """
    Frame para agregar funciones para uso
    en el módulo de análisis númerico.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarFuncs",
        func_manager: FuncManager,
    ) -> None:

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.func_frame = ctkFrame(self, fg_color="transparent")
        self.func_frame.columnconfigure(0, weight=1)

        self.key_binder = KeyBindingManager(es_matriz=False)
        self.msg_frame: Optional[ctkFrame] = None
        self.input_frame: Optional[ctkFrame] = None
        self.func = ""

        self.instruct_numpad = IconButton(
            self,
            self.app,
            image=INFO_ICON,
            tooltip_text="\nEl numpad le permite ingresar funciones\n" +
                         "matemáticas de forma más sencilla.\n\n" +
                         "Presione ALT para abrirlo, y ESC para cerrarlo.\n\n" +
                         "Para mejores resultados,\nasegúrese que los argumentos " +
                         "de la función\nestén en paréntesis, y operaciones " +
                         "complejas\ncomo multiplicación y división de funciones\n" +
                         "estén encerradas en paréntesis también.\n",
        )

        self.instruct_numpad.tooltip.configure_tooltip(x_offset=30, y_offset=30)
        self.instruct_nombre = ctkLabel(self, text="Nombre de la función:")
        self.nombre_entry = CustomEntry(self, width=40, placeholder_text="f(x)")

        self.instruct_func = ctkLabel(
            self,
            text="Ingrese los términos de la función:",
        )

        self.func_entry = CustomEntry(
            self,
            width=600,
            placeholder_text="Presione ALT para abrir el numpad de funciones...",
        )

        self.numpad = CustomNumpad(self.func_entry)
        self.leer_button = ctkButton(
            self,
            height=30,
            text="Leer función",
            command=self.leer_func,
        )

        self.key_binder.entry_list = [self.nombre_entry, self.func_entry]
        self.nombre_entry.bind("<Down>", lambda _: self.key_binder.focus_last())
        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
        self.func_entry.bind("<Up>", lambda _: self.key_binder.focus_first())
        self.func_entry.bind("<Down>", lambda _: self.key_binder.focus_first())
        self.func_entry.bind("<Return>", lambda _: self.leer_func())

        self.instruct_numpad.grid(row=0, column=0, padx=5, sticky="n")
        self.instruct_nombre.grid(row=1, column=0, padx=5, pady=(3, 1), sticky="n")
        self.nombre_entry.grid(row=2, column=0, padx=5, pady=(1, 3), sticky="n")
        self.instruct_func.grid(row=3, column=0, padx=5, pady=(3, 1), sticky="n")
        self.func_entry.grid(row=4, column=0, padx=5, pady=(1, 3), sticky="n")
        self.leer_button.grid(row=5, column=0, padx=5, pady=5, sticky="n")
        self.func_frame.grid(row=6, column=0, padx=5, pady=10, sticky="n")

    def leer_func(self) -> None:
        """
        Lee la función ingresada por el usuario,
        la muestra en pantalla, y permite agregarla
        a self.func_manager.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.func_frame.winfo_children():
            widget.destroy()  # type: ignore

        try:
            new_func = Func(self.nombre_entry.get(), self.func_entry.get())
        except ValueError as v:
            self.msg_frame = place_msg_frame(
                parent_frame=self.func_frame,
                msg_frame=self.msg_frame,
                msg=str(v),
                tipo="error",
            )

            return

        self.msg_frame = place_msg_frame(
            parent_frame=self.func_frame,
            msg_frame=self.input_frame,
            img=new_func.get_png(with_name=True),
            tipo="resultado",
        )

        ctkButton(
            self.func_frame,
            text="Agregar función",
            command=lambda: self.agregar_func(new_func),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="n")

    def agregar_func(self, new_func: Func) -> None:
        """
        Agrega la función indicada al diccionario de funciones.
        """

        self.func_manager.funcs_ingresadas[new_func.nombre] = new_func
        delete_msg_frame(self.msg_frame)
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"La función {new_func.nombre} ha sido agregada exitosamente!",
            tipo="success",
            row=6,
            pady=10,
        )

    def update_frame(self) -> None:
        """
        Actualiza los backgrounds de todas las widgets.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.func_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore

class MostrarFuncs:
    """
    Frame para mostrar las funciones ingresadas.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarFuncs",
        func_manager: FuncManager,
    ) -> None:
        pass


class EliminarFuncs:
    """
    Frame para eliminar funciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarFuncs",
        func_manager: FuncManager,
    ) -> None:
        pass
