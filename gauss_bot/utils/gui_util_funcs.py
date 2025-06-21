"""
Funciones para colocar y eliminar los
frames de mensaje de la aplicación.
"""

from typing import TYPE_CHECKING, Literal, Optional, Union

from PIL.ImageTk import PhotoImage
from customtkinter import (
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkImage as ctkImage,
    CTkLabel as ctkLabel,
    CTkToplevel as ctkTop,
)

from .icons import APP_ICON

if TYPE_CHECKING:
    from ..gui import GaussUI
    from ..gui.custom import CustomScrollFrame


def delete_msg_frame(msg_frame: Optional[ctkFrame]) -> None:
    """
    Eliminar un frame de mensaje, si existe.

    Args:
        msg_frame: Frame a eliminar.
    ---
    """

    if msg_frame is not None:
        msg_frame.destroy()
        msg_frame = None


def delete_msg_if(
    msg_frame: Optional[ctkFrame], masters: tuple[ctkFrame, ctkFrame]
) -> None:
    """
    Eliminar un frame si está colocado en uno de los frames indicados.

    Args:
        msg_frame: Frame a eliminar.
        masters:   Frames donde buscar msg_frame.master.
    ---
    """

    try:
        if msg_frame.master in masters:  # type: ignore
            delete_msg_frame(msg_frame)
    except AttributeError:
        # por si msg_frame es None
        pass


def place_msg_frame(
    parent_frame: Union[ctkFrame, "CustomScrollFrame"],
    msg_frame: Optional[ctkFrame],
    msg: Optional[str] = None,
    tipo: Literal["error", "success", "resultado"] = "error",
    **grid_kwargs,
) -> ctkFrame:
    """
    Inicializar msg_frame y colocarlo en la interfaz.

    Args:
        parent_frame: Frame que contendrá msg_frame.
        msg_frame:    Frame a colocar.
        msg:          Mensaje a mostrar en el frame.
        tipo:         Tipo de frame a crear.
        grid_kwargs:  Kwargs a pasar a msg_frame.grid().

    Returns:
        CTkFrame: El frame colocado.

    Raises:
        ValueError: Si 'tipo' no es igual a "error", "success", o "resultado".
    ---
    """

    # import local para evitar errores de imports circulares
    from ..gui.custom import ErrorFrame, ResultadoFrame, SuccessFrame

    if tipo == "error":
        msg_frame = ErrorFrame(parent_frame, msg)
    elif tipo == "success":
        msg_frame = SuccessFrame(parent_frame, msg)
    elif tipo == "resultado":
        bc: Optional[str] = grid_kwargs.pop("border_color", None)
        img: Optional[ctkImage] = grid_kwargs.pop("img", None)
        msg_frame = ResultadoFrame(parent_frame, msg, img, bc)

    else:
        raise ValueError("¡Valor inválido para argumento 'tipo'!")

    # inicializar kwargs por defecto
    if "row" not in grid_kwargs:
        grid_kwargs["row"] = 0
    if "column" not in grid_kwargs:
        grid_kwargs["column"] = 0
    if "padx" not in grid_kwargs:
        grid_kwargs["padx"] = 5
    if "pady" not in grid_kwargs:
        grid_kwargs["pady"] = 5
    if "sticky" not in grid_kwargs:
        grid_kwargs["sticky"] = "n"

    msg_frame.grid(**grid_kwargs)
    return msg_frame


def toggle_proc(
    app: "GaussUI",
    parent_frame: "CustomScrollFrame",
    window_title: str,
    proc_label: Optional[ctkLabel],
    label_txt: str,
    proc_hidden: bool,
) -> None:
    """
    Mostrar o esconder la ventana de procedimiento de una operación.

    Args:
        app:          Instancia root de GaussUI.
        parent_frame: Frame donde el usuario lanza la ventana de procedimiento.
        window_title: Título de la ventana a crear.
        proc_label:   Label que contiene el procedimiento.
        label_txt:    Texto del procedimiento.
        proc_hidden:  Bandera para identificar si esta abierta la ventana.
    ---
    """

    from ..gui.custom import CustomScrollFrame

    # si no esta escondido el procedimiento, o existe una Toplevel widget
    if not proc_hidden or any(
        type(widget) is ctkTop for widget in app.winfo_children()
    ):
        return

    new_window = ctkTop(app)
    new_window.title(window_title)
    new_window.geometry("800x800")

    parent_frame.after(100, new_window.focus)
    parent_frame.after(
        50,
        lambda: new_window.iconphoto(
            False,
            PhotoImage(file=APP_ICON[0 if app.modo_actual == "dark" else 1]),  # type: ignore
        ),
    )

    dummy_frame = ctkFrame(
        new_window, fg_color="transparent", corner_radius=20, border_width=3
    )

    dummy_frame.pack(expand=True, fill="both", padx=20, pady=20)
    proc_frame = CustomScrollFrame(dummy_frame, fg_color="transparent")

    proc_frame.pack(expand=True, fill="both", padx=10, pady=10)
    proc_label = ctkLabel(proc_frame, text=label_txt.strip(), font=ctkFont(size=14))

    proc_label.pack(expand=True, fill="both", padx=10, pady=10)
    proc_hidden = False

    new_window.protocol("WM_DELETE_WINDOW", lambda: delete_window(new_window))

    def delete_window(new_window: ctkTop) -> None:
        nonlocal proc_hidden, proc_label  # ocupar las variables del alcance exterior

        proc_hidden = True
        new_window.destroy()
        proc_label = None
