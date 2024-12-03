"""
Implementaciones de subframes de la aplicación,
que corresponden a las funcionalidades
específicas de cada módulo de la aplicación.
"""

from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
)

from customtkinter import (
    CTkFrame as ctkFrame,
)

from ....icons import SAVE_ICON
from ....gui_util_funcs import place_msg_frame
from ...custom import (
    CustomScrollFrame,
    IconButton,
)

from .input_funcs import (
    AgregarFuncs,
    MostrarFuncs,
    EliminarFuncs,
)

from .input_sis import (
    AgregarSistemas,
    MostrarSistemas,
    EliminarSistemas,
)

from .input_mats import (
    AgregarMats,
    MostrarMats,
    EliminarMats,
)

from .input_vecs import (
    AgregarVecs,
    MostrarVecs,
    EliminarVecs,
)

from .operaciones_mats import (
    SumaRestaTab,
    MultiplicacionTab,
    TransposicionTab,
    DeterminanteTab,
    InversaTab,
)

from .operaciones_vecs import (
    MagnitudTab,
    SumaRestaTab as VSRTab,
    MultiplicacionTab as VMTab,
)

from .resolver_sis import ResolverSisFrame
from .raices import RaicesFrame
from .derivadas import DerivadasFrame
from .integrales import IntegralesFrame

if TYPE_CHECKING:
    from ....models import (
        Func,
        Matriz,
        Vector,
    )

    from ... import GaussUI
    from .. import (
        ManejarMats,
        ManejarVecs,
        ManejarFuncs,
        ManejarSistemas,
        MatricesFrame,
        VectoresFrame,
        AnalisisFrame,
        SistemasFrame,
    )


__all__ = [
    "AgregarFuncs",
    "AgregarMats",
    "AgregarSistemas",
    "AgregarVecs",
    "DerivadasFrame",
    "DeterminanteTab",
    "EliminarFuncs",
    "EliminarMats",
    "EliminarSistemas",
    "EliminarVecs",
    "InversaTab",
    "IntegralesFrame",
    "MagnitudTab",
    "MostrarFuncs",
    "MostrarMats",
    "MostrarSistemas",
    "MostrarVecs",
    "MultiplicacionTab",
    "RaicesFrame",
    "ResolverSisFrame",
    "SumaRestaTab",
    "TransposicionTab",
    "VMTab",
    "VSRTab",
]


def guardar_resultado(
    app: "GaussUI",
    frame: CustomScrollFrame,
    msg_frame: Optional[ctkFrame],
    msg_exito: str,
    msg_error: str,
    frames_to_update: list[
        Union[
            "ManejarMats",
            "ManejarVecs",
            "ManejarSistemas",
            "ManejarFuncs",
            "MatricesFrame",
            "VectoresFrame",
            "AnalisisFrame",
            "SistemasFrame",
        ]
    ],
    grid_kwargs: tuple[dict[str, Any], dict[str, Any]],
    nombre_resultado: str,
    resultado: Union["Func", "Matriz", "Vector"],
    save_dict: dict,
) -> None:

    """
    Crea un IconButton para guardar el resultado de una operación,
    imprime un mensaje de éxito y actualiza los frames especificados.
    * frame: donde se colocarán las widgets
    * msg_frame: donde se imprimirá el mensaje de éxito
    * msg_exito: mensaje a imprimir
    * frames_to_update: frames a actualizar
    * grid_kwargs: argumentos de grid() para el IconButton y msg_frame
    """

    def guardar(
        parent_frame=frame,
        msg_frame=msg_frame,
        msg_exito=msg_exito,
        kwargs=grid_kwargs[1],
    ) -> None:

        if any(
            elem == resultado
            for elem in save_dict.values()
        ):
            msg_frame = place_msg_frame(
                parent_frame=parent_frame,
                msg_frame=msg_frame,
                msg=msg_error,
                tipo="resultado",
                **kwargs,
            )

            return

        save_dict[nombre_resultado] = resultado
        msg_frame = place_msg_frame(
            parent_frame=parent_frame,
            msg_frame=msg_frame,
            msg=msg_exito,
            tipo="success",
            **kwargs,
        )

        for frame in frames_to_update:
            frame.update_all()  # type: ignore

    IconButton(
        frame,
        app,
        image=SAVE_ICON,
        tooltip_text="Guardar resultado",
        command=guardar,
    ).grid(**grid_kwargs[0])
