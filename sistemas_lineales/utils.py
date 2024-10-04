import os
from fractions import Fraction
from typing import Tuple, List, Dict

# anotaciones de tipo para identificar argumentos de funciones y tipos de return
Matriz = List[List[Fraction]]
Vector = List[Fraction]
Dict_Vectores = Dict[str, Vector]
Vec = List[Fraction]
Mat = List[List[Fraction]]
Validacion = Tuple[bool, int | None]
DictMatrices = Dict[str, Tuple[Mat, bool]]
DictVectores = Dict[str, Vec]

# esta funcion se ocupa en todos los modulos
def limpiar_pantalla() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
    return None