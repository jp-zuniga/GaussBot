"""
Implementación de los subframes de ManejarFuncs.
"""

from re import match
from tkinter import Variable
from typing import TYPE_CHECKING

from customtkinter import CTkFont, CTkFrame, CTkLabel, ThemeManager
from sympy import SympifyError

from src.gui.custom import (
    CustomDropdown,
    CustomEntry,
    ErrorFrame,
    IconButton,
    SuccessFrame,
)
from src.gui.custom.adapted import CustomMessageBox, CustomNumpad, CustomScrollFrame
from src.managers import FuncManager, KeyBindingManager
from src.models import Func
from src.utils import (
    ACEPTAR_ICON,
    ELIMINAR_ICON,
    ENTER_ICON,
    INFO_ICON,
    LIMPIAR_ICON,
    MOSTRAR_ICON,
    delete_msg_frame,
    generate_sep,
    place_msg_frame,
)

if TYPE_CHECKING:
    from src.gui import GaussUI
    from src.gui.frames import ManejarFuncs


class AgregarFuncs(CustomScrollFrame):
    """
    Frame para agregar funciones matemáticas
    para uso en el módulo de análisis númerico.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarFuncs",
        func_manager: FuncManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de agregar funciones.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.func_manager = func_manager
        self.master_frame = master_frame
        self.msg_box: CustomMessageBox | None = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.key_binder = KeyBindingManager(es_matriz=False)
        self.func_frame = CTkFrame(self, fg_color="transparent")
        self.func_frame.columnconfigure(0, weight=1)
        self.func_frame.columnconfigure(1, weight=1)

        self.msg_frame: CTkFrame | None = None
        self.input_func: CTkFrame | None = None

        self.instruct_numpad = IconButton(
            self,
            image=INFO_ICON,
            tooltip_text="El numpad le permite ingresar funciones"
            "\nmatemáticas de una forma más sencilla.\n"
            "\nCon el cursor en la entrada de términos,"
            "\npresione CTRL+TAB para abrirlo y ESC para cerrarlo.",
            tooltip_pady=10,
            command=self.mostrar_tutorial,
        )

        self.instruct_nombre = CTkLabel(self, text="Nombre de la función:")
        self.nombre_entry = CustomEntry(self, width=60, placeholder_text="f(x)")

        self.instruct_func = CTkLabel(self, text="Ingrese los términos de la función:")
        self.func_entry = CustomEntry(
            self,
            width=500,
            placeholder_text="Presione CTRL+TAB para abrir el numpad de funciones...",
        )

        self.func_entry.unbind("<Tab>")
        self.numpad = CustomNumpad(self.func_entry)
        self.leer_button = IconButton(
            self,
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

        self.instruct_nombre.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=(3, 1),
            sticky="n",
        )

        self.nombre_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=(1, 3),
            sticky="n",
        )

        self.instruct_func.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=5,
            pady=(3, 1),
            sticky="n",
        )

        self.func_entry.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=(1, 3),
            sticky="n",
        )

        self.instruct_numpad.grid(row=4, column=0, padx=2, pady=5, sticky="ne")
        self.leer_button.grid(row=4, column=1, padx=2, pady=5, sticky="nw")

    def leer_func(self) -> None:
        """
        Leer función ingresada y mostrarla.
        """

        delete_msg_frame(self.msg_frame)
        for widget in self.func_frame.winfo_children():
            widget.destroy()
        self.func_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="n")

        try:
            input_nombre = self.nombre_entry.get()
            input_terms = self.func_entry.get()

            if input_nombre == "":
                raise ValueError("Debe ingresar el nombre de la función.")  # noqa: TRY301
            if input_terms == "":
                raise ValueError("Debe ingresar los términos de la función.")  # noqa: TRY301

            new_func = Func(input_nombre, input_terms)
        except (SyntaxError, SympifyError, ValueError) as v:
            if isinstance(v, ValueError):
                msg_error = str(v)
            else:
                msg_error = "Debe ingresar una expresión matemática válida."

            self.msg_frame = place_msg_frame(
                parent_frame=self.func_frame,
                msg_frame=self.msg_frame,
                msg=msg_error,
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
            image=ACEPTAR_ICON,
            tooltip_text="Agregar función",
            command=lambda: self.agregar_func(new_func),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        IconButton(
            self.func_frame,
            image=LIMPIAR_ICON,
            tooltip_text="Eliminar función leída",
            command=self.limpiar_input,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def agregar_func(self, new_func: Func) -> None:
        """
        Agregar la función ingresada al diccionario de funciones.

        Args:
            new_func: Función a agregar.

        """

        delete_msg_frame(self.msg_frame)
        latest_nombre = self.nombre_entry.get()
        if new_func.nombre != latest_nombre:
            new_func.nombre = latest_nombre

        if (
            new_func.nombre in self.func_manager.funcs_ingresadas
            or not self.validar_nombre(new_func.nombre)
        ):
            if not self.validar_nombre(new_func.nombre):
                error_msg = "El nombre de la función debe tener la forma 'f(x)'."
            elif str(new_func.var) not in str(new_func.expr):
                error_msg = (
                    f"La función ingresada no contiene la variable {new_func.var}."
                )
            else:
                error_msg = f"¡Ya existe una función llamada {new_func.nombre}!"

            self.msg_frame = place_msg_frame(
                parent_frame=self.func_frame,
                msg_frame=self.msg_frame,
                msg=error_msg,
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
            msg=f"¡La función {new_func.nombre} ha sido agregada exitosamente!",
            tipo="success",
            row=2,
            columnspan=2,
            pady=10,
        )

        self.func_manager.funcs_ingresadas = dict(
            sorted(self.func_manager.funcs_ingresadas.items()),
        )

        self.master_frame.update_all()
        self.app.analisis.update_all()

    def validar_nombre(self, nombre: str) -> bool:
        """
        Validar nombre de función.

        Args:
            nombre: Nombre de función a validar.

        Returns:
            bool: Si se encontro un match para el regex de notación matemática.

        """

        pattern = r"^[a-z]\([a-z]\)$"
        return bool(match(pattern, nombre))

    def limpiar_input(self) -> None:
        """
        Limpiar campos de entrada.
        """

        self.nombre_entry.delete(0, "end")
        self.func_entry.delete(0, "end")
        for widget in self.func_frame.winfo_children():
            widget.destroy()
        delete_msg_frame(self.msg_frame)

    def mostrar_tutorial(self) -> None:
        """
        Mostrar CustomMessageBox explicando el uso del Numpad.
        """

        if self.msg_box is not None:
            self.msg_box.focus()
            return

        self.msg_box = CustomMessageBox(
            self.app,
            width=500,
            height=400,
            name="Detalles sobre Numpad Matemático",
            msg="\nEl numpad le permite ingresar funciones matemáticas de "
            "una forma más sencilla. Con el cursor en la entrada de términos, "
            "presione CTRL+TAB para abrirlo y ESC para cerrarlo.\n"
            "\nPara mejores resultados, asegúrese que los argumentos de la "
            "función estén en paréntesis, y operaciones complejas como "
            "multiplicación y división de funciones estén encerradas "
            "en paréntesis también.\n\nSe pueden definir funciones en "
            "cualquier variable; simplemente  especifique la variable "
            "en el nombre de la función, e.g. s(t). Esto se detectará dinámicamente, "
            "y se sobreescribirán las 'x' ingresadas con el Numpad.\n",
            button_options=("Ok", None, None),
            icon="info",
        )

        self.msg_box.get()
        self.msg_box.destroy()
        self.msg_box = None

    def update_frame(self) -> None:
        """
        Actualizar colores de widgets.
        """

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")


class MostrarFuncs(CustomScrollFrame):
    """
    Frame para mostrar las funciones ingresadas.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarFuncs",
        func_manager: FuncManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de mostrar funciones.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)

        self.funcs_guardadas = self.func_manager.get_funcs()
        self.msg_frame: CTkFrame | None = None
        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializar widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        if not self.funcs_guardadas:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="¡No se ha guardado ninguna función!",
                tipo="error",
            )

            return

        IconButton(
            self,
            border_width=3,
            border_color=ThemeManager.theme["CTkFrame"]["top_fg_color"],
            image=MOSTRAR_ICON,
            tooltip_text="Mostrar funciones",
            command=self.show_funcs,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="n")

    def show_funcs(self) -> None:
        """
        Mostrar funciones guardadas.
        """

        delete_msg_frame(self.msg_frame)
        for widget in [
            x for x in self.winfo_children() if not isinstance(x, IconButton)
        ]:
            widget.destroy()

        CTkLabel(self, text="Funciones ingresadas:", font=CTkFont(weight="bold")).grid(
            row=1,
            column=0,
            pady=5,
            sticky="n",
        )

        CTkLabel(self, text="", image=generate_sep(False, (300, 5))).grid(
            row=2,
            column=0,
            sticky="n",
        )

        r: int = 3
        for func in self.funcs_guardadas:
            CTkLabel(self, text="", image=func).grid(row=r, column=0, sticky="n")
            CTkLabel(self, text="", image=generate_sep(False, (300, 5))).grid(
                row=r + 1,
                column=0,
                sticky="n",
            )

            r += 2

    def update_frame(self) -> None:
        """
        Eliminar self.show_frame y configurar backgrounds.
        """

        for widget in [
            x for x in self.winfo_children() if not isinstance(x, IconButton)
        ]:
            widget.destroy()

        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")

        self.funcs_guardadas = self.func_manager.get_funcs()
        if isinstance(self.msg_frame, ErrorFrame):
            self.setup_frame()


class EliminarFuncs(CustomScrollFrame):
    """
    Frame para eliminar funciones.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: CTkFrame,
        master_frame: "ManejarFuncs",
        func_manager: FuncManager,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """
        Inicializar diseño de frame de eliminar funciones.
        """

        super().__init__(master_tab, fg_color="transparent", **kwargs)

        self.app = app
        self.master_frame = master_frame
        self.func_manager = func_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())
        self.msg_frame: CTkFrame | None = None
        self.select_func: CustomDropdown
        self.func_seleccionada = ""
        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Crear y colocar las widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        if len(self.nombres_funcs) == 0:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="¡No se ha guardado ninguna función!",
                tipo="error",
                columnspan=2,
            )

            return

        for widget in self.winfo_children():
            widget.destroy()

        # crear widgets
        instruct_eliminar = CTkLabel(self, text="¿Cuál función desea eliminar?")
        self.select_func = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_funcs,
            command=self.update_func,
        )

        button = IconButton(
            self,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar función",
            command=self.eliminar_func,
        )

        self.func_seleccionada = self.select_func.get()

        # colocar widgets
        instruct_eliminar.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="n",
        )
        self.select_func.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_func(self) -> None:
        """
        Eliminar función seleccionada.
        """

        delete_msg_frame(self.msg_frame)
        self.update_func(self.select_func.get())
        self.func_manager.funcs_ingresadas.pop(self.func_seleccionada)

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"¡Función {self.func_seleccionada} eliminada!",
            tipo="success",
            row=2,
            columnspan=2,
        )

        # mandar a actualizar los datos
        self.app.analisis.update_all()
        self.master_frame.update_all()

    def update_frame(self) -> None:
        """
        Actualizar frame y datos.
        """

        self.nombres_funcs = list(self.func_manager.funcs_ingresadas.keys())

        if len(self.nombres_funcs) == 0 and isinstance(self.msg_frame, SuccessFrame):

            def clear_after_wait() -> None:
                delete_msg_frame(self.msg_frame)
                self.msg_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.msg_frame,
                    msg="¡No se ha guardado ninguna función!",
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
            self.select_func.configure(
                values=self.nombres_funcs,
                variable=Variable(value=self.nombres_funcs[0]),
            )

            self.after(1000, lambda: delete_msg_frame(self.msg_frame))

    def update_func(self, valor: str) -> None:
        """
        Actualizar 'self.func_seleccionada'.

        Args:
            valor: Selección del dropdown.

        """

        self.func_seleccionada = valor
