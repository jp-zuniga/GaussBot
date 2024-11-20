"""
Implementación de los subframes de ManejarFuncs.
"""

from typing import (
    TYPE_CHECKING,
    Optional,
)

from customtkinter import (
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
)

from gauss_bot import (
    ACEPTAR_ICON,
    ENTER_ICON,
    INFO_ICON,
    LIMPIAR_ICON,
    MOSTRAR_ICON,
    delete_msg_frame,
    generate_sep,
    resize_image,
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
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.func_frame = ctkFrame(self, fg_color="transparent")
        self.func_frame.columnconfigure(0, weight=1)
        self.func_frame.columnconfigure(1, weight=1)

        self.key_binder = KeyBindingManager(es_matriz=False)
        self.msg_frame: Optional[ctkFrame] = None
        self.input_func: Optional[ctkFrame] = None

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
            width=500,
            placeholder_text="Presione ALT para abrir el numpad de funciones...",
        )

        self.numpad = CustomNumpad(self.func_entry)
        self.leer_button = IconButton(
            self,
            app=self.app,
            image=ENTER_ICON,
            tooltip_text="Leer función",
            command=self.leer_func,
        )

        self.key_binder.entry_list = [self.nombre_entry, self.func_entry]
        self.nombre_entry.bind("<Down>", lambda _: self.key_binder.focus_last())
        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
        self.func_entry.bind("<Up>", lambda _: self.key_binder.focus_first())
        self.func_entry.bind("<Down>", lambda _: self.key_binder.focus_first())
        self.func_entry.bind("<Return>", lambda _: self.leer_func())

        self.instruct_numpad.grid(row=0, column=0, columnspan=2, padx=5, sticky="n")
        self.instruct_nombre.grid(
            row=1, column=0,
            columnspan=2,
            padx=5, pady=(3, 1),
            sticky="n",
        )

        self.nombre_entry.grid(
            row=2, column=0,
            columnspan=2,
            padx=5, pady=(1, 3),
            sticky="n",
        )

        self.instruct_func.grid(
            row=3, column=0,
            columnspan=2,
            padx=5, pady=(3, 1),
            sticky="n",
        )

        self.func_entry.grid(row=4, column=0, padx=5, pady=(1, 3), sticky="e")
        self.leer_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.func_frame.grid(
            row=5, column=0,
            columnspan=2,
            padx=5, pady=5,
            sticky="n",
        )

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
                columnspan=2,
            )

            return

        self.input_func = place_msg_frame(
            parent_frame=self.func_frame,
            msg_frame=self.input_func,
            img=new_func.get_png(),
            tipo="resultado",
            columnspan=2,
        )

        IconButton(
            self.func_frame,
            app=self.app,
            image=ACEPTAR_ICON,
            tooltip_text="\nAgregar función\n" +
                         "(Nota:\nSe agregará la función\n" +
                         "presentada en la imagen)\n",
            command=lambda: self.agregar_func(new_func),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        IconButton(
            self.func_frame,
            app=self.app,
            image=LIMPIAR_ICON,
            tooltip_text="Eliminar función leída",
            command=self.limpiar_input,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def agregar_func(self, new_func: Func) -> None:
        """
        Agrega la función indicada al diccionario de funciones.
        """

        delete_msg_frame(self.msg_frame)
        latest_nombre = self.nombre_entry.get()
        if new_func.nombre != latest_nombre:
            new_func.nombre = latest_nombre

        if new_func.nombre in self.func_manager.funcs_ingresadas:
            self.msg_frame = place_msg_frame(
                parent_frame=self.func_frame,
                msg_frame=self.msg_frame,
                msg=f"Ya existe una función llamada {new_func.nombre}!",
                tipo="error",
                row=2,
                columnspan=2,
                pady=10,
            )

            return

        self.func_manager.funcs_ingresadas[new_func.nombre] = new_func
        self.msg_frame = place_msg_frame(
            parent_frame=self.func_frame,
            msg_frame=self.msg_frame,
            msg=f"La función {new_func.nombre} ha sido agregada exitosamente!",
            tipo="success",
            row=2,
            columnspan=2,
            pady=10,
        )

        self.master_frame.update_all()

    def limpiar_input(self) -> None:
        """
        Limpia los campos de entrada.
        """

        self.nombre_entry.delete(0, "end")
        self.func_entry.delete(0, "end")
        for widget in self.func_frame.winfo_children():
            widget.destroy()  # type: ignore
        delete_msg_frame(self.msg_frame)

    def update_frame(self) -> None:
        """
        Actualiza los backgrounds de todas las widgets.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.func_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore

class MostrarFuncs(CustomScrollFrame):
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

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.msg_frame: Optional[ctkFrame] = None
        self.show_frame = ctkFrame(self, fg_color="transparent")
        self.show_frame.columnconfigure(0, weight=1)

        IconButton(
            self,
            self.app,
            width=30,
            height=30,
            corner_radius=16,
            border_width=3,
            border_color=self.app.theme_config["CTkFrame"]["top_fg_color"],
            image=resize_image(MOSTRAR_ICON, (0.75, 1)),
            tooltip_text="Mostrar funciones",
            command=self.show_funcs
        ).grid(row=0, column=0, padx=5, pady=(5, 0), sticky="n")
        self.show_frame.grid(row=1, column=0, padx=5, sticky="n")

    def show_funcs(self) -> None:
        """
        Muestra las funciones guardadas.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.show_frame.winfo_children():
            widget.destroy()  # type: ignore

        funcs_guardadas = self.func_manager.get_funcs()
        if not funcs_guardadas:
            self.msg_frame = place_msg_frame(
                parent_frame=self.show_frame,
                msg_frame=self.msg_frame,
                msg="No se ha guardado ninguna función!",
                tipo="error",
            )

            return

        ctkLabel(
            self.show_frame,
            text="",
            image=generate_sep(False, (200, 10)),
        ).grid(row=0, column=0, padx=5, sticky="n")

        ctkLabel(
            self.show_frame,
            text="Funciones ingresadas:",
            font=("Roboto", 12, "bold"),
        ).grid(row=1, column=0, padx=5, sticky="n")

        ctkLabel(
            self.show_frame,
            text="",
            image=generate_sep(False, (200, 10)),
        ).grid(row=2, column=0, padx=5, sticky="n")

        for i, func in enumerate(funcs_guardadas):
            ctkLabel(
                self.show_frame,
                text="",
                image=func,
            ).grid(row=i + 3, column=0, padx=5, pady=5, sticky="n")

    def update_frame(self) -> None:
        """
        Elimina self.show_frame y configura los backgrounds.
        """

        for widget in self.show_frame.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore
        for widget in self.winfo_children():  # type: ignore
            widget.configure(bg_color="transparent")  # type: ignore


class EliminarFuncs(CustomScrollFrame):
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

        super().__init__(app, master_tab, corner_radius=0, fg_color="transparent")
        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager

    def update_frame(self) -> None:
        """
        Actualiza los datos del dropdown y
        los backgrounds de todas las widgets.
        """
