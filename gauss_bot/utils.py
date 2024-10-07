import os
from fractions import Fraction
from typing import Tuple, List, Dict


# anotaciones de tipo para identificar argumentos de funciones y tipos de return
Vec = List[Fraction]
Mat = List[List[Fraction]]
DictMatrices = Dict[str, Tuple[Mat, bool]]
DictVectores = Dict[str, Vec]
Validacion = Tuple[bool, int]

def limpiar_pantalla() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
    return None
