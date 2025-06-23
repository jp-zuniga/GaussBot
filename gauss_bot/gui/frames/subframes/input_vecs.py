"""
Implementación de los subframes de ManejarVecs.
"""

from fractions import Fraction
from random import choice, randint
from string import ascii_lowercase
from tkinter import Variable
from typing import TYPE_CHECKING, Optional

from customtkinter import CTkFrame as ctkFrame, CTkLabel as ctkLabel

from ...custom import (
    CustomDropdown,
    CustomEntry,
    CustomScrollFrame,
    ErrorFrame,
    IconButton,
    SuccessFrame,
)
from ....managers import KeyBindingManager, VectoresManager
from ....models import Vector
from ....utils import (
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
    from .. import ManejarVecs
    from ... import GaussUI


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
        vecs_manager: VectoresManager,
        **kwargs,
    ) -> None:
        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.master_frame = master_frame
        self.app = app
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)

        self.key_binder = KeyBindingManager(es_matriz=False)
        self.msg_frame: Optional[ctkFrame] = None
        self.input_entries: list[CustomEntry] = []

        # frames para contener secciones de la interfaz
        self.pre_vec_frame = ctkFrame(self, fg_color="transparent")
        self.vector_frame = ctkFrame(self, fg_color="transparent")
        self.post_vec_frame = ctkFrame(self, fg_color="transparent")
        self.nombre_entry: CustomEntry

        # crear widgets iniciales para ingresar dimensiones
        dimension_label = ctkLabel(self.pre_vec_frame, text="Dimensiones:")
        self.dimension_entry = CustomEntry(
            self.pre_vec_frame, width=30, placeholder_text="3"
        )

        ingresar_button = IconButton(
            self.pre_vec_frame,
            self.app,
            image=ENTER_ICON,
            tooltip_text="Ingresar datos del vector",
            command=self.generar_casillas,
        )

        aleatorio_button = IconButton(
            self.pre_vec_frame,
            self.app,
            image=SHUFFLE_ICON,
            tooltip_text="Generar vector con valores aleatorios",
            command=self.generar_aleatorio,
        )

        # crear bindings iniciales
        self.dimension_entry.bind("<Return>", lambda _: self.generar_casillas())
        self.dimension_entry.bind("<Down>", lambda _: self.key_binder.focus_first())

        # colocar widgets
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

        # si habian widgets creadas debajo
        # de self.pre_vec_frame, eliminarlas
        for widget in self.vector_frame.winfo_children():
            widget.destroy()  # type: ignore
        for widget in self.post_vec_frame.winfo_children():
            widget.destroy()  # type: ignore

        delete_msg_frame(self.msg_frame)
        dimension = self.validar_dimensiones()
        if dimension is None:
            # hubo input invalido
            return
        delete_msg_frame(self.msg_frame)

        # crear entries para ingresar el vector
        self.input_entries.clear()
        for i in range(dimension):
            input_entry = CustomEntry(
                self.vector_frame, width=60, placeholder_text=str(randint(-15, 15))
            )

            input_entry.grid(row=i, column=0, padx=5, pady=5)
            self.input_entries.append(input_entry)

        # crear post_vec_frame widgets
        nombre_label = ctkLabel(self.post_vec_frame, text="Nombre del vector:")
        self.nombre_entry = CustomEntry(
            self.post_vec_frame,
            width=30,
            placeholder_text=choice(
                [
                    x
                    for x in ascii_lowercase
                    if x not in self.vecs_manager.vecs_ingresados.values()
                ]
            ),
        )

        agregar_button = IconButton(
            self.post_vec_frame,
            self.app,
            image=ACEPTAR_ICON,
            tooltip_text="Agregar vector",
            command=self.agregar_vector,
        )

        limpiar_button = IconButton(
            self.post_vec_frame,
            self.app,
            image=LIMPIAR_ICON,
            tooltip_text="Limpiar casillas",
            command=self.limpiar_casillas,
        )

        # colocar widgets
        self.vector_frame.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.post_vec_frame.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        agregar_button.grid(row=0, column=2, padx=2, pady=5)
        limpiar_button.grid(row=0, column=3, padx=2, pady=5)

        # configurar atributos de self.key_binder y crear bindings
        self.key_binder.entry_list = self.input_entries  # type: ignore
        self.key_binder.extra_entries = (self.nombre_entry, self.dimension_entry)  # type: ignore
        self.key_binder.create_key_bindings()

        self.nombre_entry.bind("<Up>", lambda _: self.key_binder.focus_last())
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

        delete_msg_frame(self.msg_frame)
        dimension = self.validar_dimensiones()
        if dimension is None:
            # hubo input invalido
            return
        delete_msg_frame(self.msg_frame)

        # si los input de dimensiones cambio despues de generar las casillas
        if dimension != len(self.input_entries):
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="Las dimensiones del vector ingresado "
                + "no coinciden con las dimensiones indicadas!",
                tipo="error",
                row=3,
            )
            return
        delete_msg_frame(self.msg_frame)

        # recorrer entries para guardar los valores
        componentes = []
        for entry in self.input_entries:
            try:
                valor = Fraction(entry.get())
            except (ValueError, ZeroDivisionError) as e:
                if isinstance(e, ValueError):
                    msg = "Todos los valores deben ser números racionales!"
                else:
                    msg = "El denominador no puede ser 0!"
                self.msg_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.msg_frame,
                    msg=msg,
                    tipo="error",
                    row=3,
                )
                return
            componentes.append(valor)
        delete_msg_frame(self.msg_frame)

        nombre_nuevo_vector = self.nombre_entry.get()
        nuevo_vector = Vector(componentes)

        # validar nombre
        nombre_repetido = nombre_nuevo_vector in self.vecs_manager.vecs_ingresados
        nombre_valido = (
            nombre_nuevo_vector.isalpha()
            and nombre_nuevo_vector.islower()
            and len(nombre_nuevo_vector) == 1
        )

        if not nombre_valido or nombre_repetido:
            msg = (
                "El nombre del vector debe ser una letra minúscula!"
                if not nombre_valido
                else f"Ya existe un vector nombrado {nombre_nuevo_vector}!"
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

        self.vecs_manager.vecs_ingresados[nombre_nuevo_vector] = nuevo_vector
        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"El vector {nombre_nuevo_vector} se ha agregado exitosamente!",
            tipo="success",
            row=3,
        )

        # mandar a actualizar los datos
        self.master_frame.update_all()
        self.app.vectores.update_all()  # type: ignore
        self.app.matrices.update_all()  # type: ignore

    def validar_dimensiones(self) -> Optional[int]:
        """
        Valida si las dimensiones ingresadas por el usuario
        son válidas y las retorna si lo son, o retorna None si son inválidas.
        """

        try:
            dimension = int(self.dimension_entry.get())
            if dimension <= 0:
                raise ValueError
        except ValueError:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="Debe ingresar un número entero " + "positivo como dimensión!",
                tipo="error",
                row=1,
            )
            return None
        return dimension

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


class MostrarVecs(CustomScrollFrame):
    """
    Frame para mostrar los vectores guardados.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarVecs",
        vecs_manager: VectoresManager,
        **kwargs,
    ) -> None:
        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.show_frame: Optional[ctkFrame] = None

        # definir los filtros que se mandaran
        # a self.vecs_manager.get_vectores()
        self.opciones: dict[str, int] = {
            "Mostrar todos": -1,
            "Vectores ingresados": 0,
            "Vectores calculados": 1,
        }

        self.select_opcion: CustomDropdown
        self.opcion_seleccionada: Optional[int] = None

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Inicializa las widgets del frame.
        """

        delete_msg_frame(self.show_frame)
        if len(self.vecs_manager.vecs_ingresados.keys()) == 0:
            self.show_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.show_frame,
                msg="No se ha guardado ningún vector!",
                tipo="error",
                columnspan=2,
            )

            return

        for widget in self.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

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
            self.app,
            image=MOSTRAR_ICON,
            tooltip_text="Mostrar",
            command=self.show_vecs,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def show_vecs(self) -> None:
        """
        Muestra los vectores guardados, usando el filtro seleccionado.
        """

        delete_msg_frame(self.show_frame)
        if "filtro" in self.select_opcion.get():
            self.show_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.show_frame,
                msg="Debe seleccionar un filtro!",
                tipo="error",
                row=1,
                columnspan=2,
            )

            return

        self.update_opcion(self.select_opcion.get())
        vecs_text = self.vecs_manager.get_vectores(self.opcion_seleccionada)  # type: ignore
        self.show_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.show_frame,
            msg=vecs_text,
            tipo="resultado",
            row=1,
            columnspan=2,
        )

        self.show_frame.columnconfigure(0, weight=1)  # type: ignore

    def update_frame(self) -> None:
        """
        Elimina self.show_frame y configura los backgrounds.
        """

        delete_msg_frame(self.show_frame)
        for widget in self.winfo_children():
            widget.configure(bg_color="transparent")  # type: ignore

        if isinstance(self.show_frame, ErrorFrame):
            self.setup_frame()
        else:
            self.select_opcion.configure(
                variable=Variable(value="Seleccione un filtro:")
            )

    def update_opcion(self, valor: str) -> None:
        """
        Actualiza self.opcion_seleccionada
        con la opción seleccionada en el dropdown
        """

        self.opcion_seleccionada = self.opciones[valor]


class EliminarVecs(CustomScrollFrame):
    """
    Frame para eliminar vectores.
    """

    def __init__(
        self,
        app: "GaussUI",
        master_tab: ctkFrame,
        master_frame: "ManejarVecs",
        vecs_manager: VectoresManager,
        **kwargs,
    ) -> None:
        super().__init__(master_tab, fg_color="transparent", **kwargs)
        self.app = app
        self.master_frame = master_frame
        self.vecs_manager = vecs_manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())
        self.msg_frame: Optional[ctkFrame] = None

        self.select_vec: CustomDropdown
        self.vec_seleccionado = ""

        self.setup_frame()

    def setup_frame(self) -> None:
        """
        Crear y colocar las widgets del frame.
        """

        delete_msg_frame(self.msg_frame)
        if len(self.nombres_vectores) == 0:
            self.msg_frame = place_msg_frame(
                parent_frame=self,
                msg_frame=self.msg_frame,
                msg="No se ha guardado ningún vector!",
                tipo="error",
                columnspan=2,
            )

            return

        for widget in self.winfo_children():  # type: ignore
            widget.destroy()  # type: ignore

        # crear widgets
        instruct_eliminar = ctkLabel(self, text="¿Cuál vector desea eliminar?")
        self.select_vec = CustomDropdown(
            self,
            height=30,
            width=60,
            values=self.nombres_vectores,
            command=self.update_vec,
        )

        button = IconButton(
            self,
            self.app,
            image=ELIMINAR_ICON,
            tooltip_text="Eliminar vector",
            command=self.eliminar_vector,
        )

        self.vec_seleccionado = self.select_vec.get()

        # colocar widgets
        instruct_eliminar.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n"
        )
        self.select_vec.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def eliminar_vector(self) -> None:
        """
        Elimina el vector seleccionado.
        """

        delete_msg_frame(self.msg_frame)
        self.update_vec(self.select_vec.get())
        self.vecs_manager.vecs_ingresados.pop(self.vec_seleccionado)

        self.msg_frame = place_msg_frame(
            parent_frame=self,
            msg_frame=self.msg_frame,
            msg=f"Vector {self.vec_seleccionado} eliminado!",
            tipo="success",
            row=2,
            columnspan=2,
        )

        # mandar a actualizar los datos
        self.master_frame.update_all()
        self.app.matrices.update_all()  # type: ignore
        self.app.vectores.update_all()  # type: ignore

    def update_frame(self) -> None:
        """
        Actualiza el frame y sus datos.
        """

        self.nombres_vectores = list(self.vecs_manager.vecs_ingresados.keys())

        if len(self.nombres_vectores) == 0 and isinstance(self.msg_frame, SuccessFrame):

            def clear_after_wait() -> None:
                delete_msg_frame(self.msg_frame)
                self.msg_frame = place_msg_frame(
                    parent_frame=self,
                    msg_frame=self.msg_frame,
                    msg="No se ha guardado ningún vector!",
                    tipo="error",
                    columnspan=2,
                )

                for widget in self.winfo_children():
                    if not isinstance(widget, ctkFrame):
                        widget.destroy()

            self.after(1000, clear_after_wait)

        elif isinstance(self.msg_frame, ErrorFrame):
            self.setup_frame()

        else:
            for widget in self.winfo_children():
                widget.configure(bg_color="transparent")  # type: ignore
            self.select_vec.configure(
                values=self.nombres_vectores,
                variable=Variable(value=self.nombres_vectores[0]),
            )

            self.after(1000, lambda: delete_msg_frame(self.msg_frame))

    def update_vec(self, valor: str) -> None:
        """
        Actualiza vec_seleccionado con el valor seleccionado en el dropdown.
        """

        self.vec_seleccionado = valor
