import os
from typing import List, Dict, Tuple
from fractions import Fraction

# anotaciones de tipo para identificar argumentos de funciones y tipos de return
Matriz = List[List[Fraction]]
Vector = List[Fraction]
Dict_Vectores = Dict[str, Vector]

# se ocupa en todos los modulos
def limpiar_pantalla() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
    return None