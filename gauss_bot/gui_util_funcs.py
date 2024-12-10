"""
Funciones para colocar y eliminar los
frames de mensaje de la aplicación.
"""

from typing import (
    TYPE_CHECKING,
    Literal,
    Optional,
    Union,
)

from customtkinter import (
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkToplevel as ctkTop,
)

from .icons import APP_ICON
from .gui.custom import (
    CustomScrollFrame,
    ErrorFrame,
    ResultadoFrame,
    SuccessFrame,
)

if TYPE_CHECKING:
    from .gui import GaussUI


__all__= [
    "delete_msg_frame",
    "delete_msg_if",
    "place_msg_frame",
    "toggle_proc",
]


def delete_msg_frame(msg_frame: Optional[ctkFrame]) -> None:
    """
    Elimina un frame de mensaje si existe.
    * msg_frame: frame a eliminar
    """

    if msg_frame is not None:
        msg_frame.destroy()
        msg_frame = None


def delete_msg_if(
    msg_frame: Optional[ctkFrame],
    masters: tuple[ctkFrame, ctkFrame]
) -> None:

    """
    Llama delete_msg_frame() si msg_frame
    esta colocado en uno de los frames indicados.
    * msg_frame: frame a eliminar
    * masters: frames donde buscar msg_frame
    """

    try:
        if msg_frame.master in masters:  # type: ignore
            delete_msg_frame(msg_frame)
    except AttributeError:
        # si msg_frame == None,
        # .master va a tirar error
        pass


def place_msg_frame(
    parent_frame: Union[ctkFrame, CustomScrollFrame],  # noqa
    msg_frame: Optional[ctkFrame],
    msg: Optional[str] = None,
    tipo: Literal["error", "success", "resultado"] = "error",
    **grid_kwargs,
) -> ctkFrame:

    """
    Inicializa msg_frame y lo coloca en la interfaz con grid_kwargs.
    * parent_frame: frame que contendrá msg_frame
    * msg_frame: frame a colocar
    * msg: mensaje a mostrar en el frame
    * tipo: tipo de frame a crear
    * grid_kwargs: kwargs a pasar a msg_frame.grid()
    """

    if tipo == "error":
        msg_frame = ErrorFrame(parent_frame, msg)  # noqa
    elif tipo == "success":
        msg_frame = SuccessFrame(parent_frame, msg)  # noqa

    elif tipo == "resultado":
        bc = grid_kwargs.pop("border_color", None)
        img = grid_kwargs.pop("img", None)
        msg_frame = ResultadoFrame(parent_frame, msg, img, bc)  # noqa

    else:
        raise ValueError("Valor inválido para argumento 'tipo'!")

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
    parent_frame: CustomScrollFrame,
    window_title: str,
    proc_label: Optional[ctkLabel],
    label_txt: str,
    proc_hidden: bool,
) -> None:

    """
    Muestra o esconde la ventana de procedimiento.
    """

    if (
        not proc_hidden
        or
        any(
            type(widget) is ctkTop  # pylint: disable=unidiomatic-typecheck
            for widget in app.winfo_children()
        )
    ):
        return

    new_window = ctkTop(app)
    new_window.title(window_title)

    new_window.geometry("800x800")
    parent_frame.after(100, new_window.focus)  # type: ignore

    if app.modo_actual == "dark":
        i = 0
    elif app.modo_actual == "light":
        i = 1

    parent_frame.after(
        250,
        lambda: new_window.iconbitmap(APP_ICON[i]),  # pylint: disable=E0606
    )

    new_window.protocol(
        "WM_DELETE_WINDOW",
        lambda: delete_window(new_window),
    )

    dummy_frame = ctkFrame(
        new_window,
        fg_color="transparent",
        corner_radius=20,
        border_width=3,
    )

    dummy_frame.pack(expand=True, fill="both", padx=20, pady=20)
    proc_frame = CustomScrollFrame(
        dummy_frame,
        fg_color="transparent",
    )

    proc_frame.pack(expand=True, fill="both", padx=10, pady=10)
    proc_label = ctkLabel(
        proc_frame,
        text=label_txt.strip(),
        font=ctkFont(size=14),
    )

    proc_label.pack(expand=True, fill="both", padx=10, pady=10)
    proc_hidden = False

    def delete_window(new_window: ctkTop) -> None:
        proc_hidden = True  # pylint: disable=W0612  # noqa
        new_window.destroy()
        proc_label = None  # pylint: disable=W0612  # noqa
