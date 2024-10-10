from fractions import Fraction
from typing import Tuple, List, overload

from gauss_bot.matrices.matriz import Matriz

class Vector(Matriz):
    def __init__(self, componentes: List[Fraction]) -> None:
        super().__init__(aumentada=False, filas=len(componentes), columnas=1, valores=[[c] for c in componentes])

    @property
    def componentes(self) -> List[Fraction]:
        return [self.valores[i][0] for i in range(self.filas)]

    def __len__(self) -> int:
        return self.filas

    @overload
    def __getitem__(self, indice_fila: int) -> List[Fraction]: ...

    @overload
    def __getitem__(self, indices: Tuple[int, int]) -> Fraction: ...

    def __getitem__(self, indice: int | Tuple[int, int]) -> List[Fraction] | Fraction:
        if isinstance(indice, int):
            return self.valores[indice]
        elif isinstance(indice, tuple) and len(indice) == 2:
            fila, columna = indice
            return self.valores[fila][columna]
        else:
            raise TypeError("Índice inválido")

    def __setitem__(self, indices: Tuple[int, int], valor: Fraction) -> None:
        fila, columna = indices
        self.valores[fila][columna] = valor

    def __str__(self) -> str:
        return f"[{', '.join(str(c) for c in self.componentes)}]"

    def __add__(self, vec2: 'Vector') -> 'Vector':
        if len(self) != len(vec2):
            raise ValueError("Vectores deben tener la misma longitud")
        return Vector([a + b for a, b in zip(self.componentes, vec2.componentes)])

    def __sub__(self, vec2: 'Vector') -> 'Vector':
        if len(self) != len(vec2):
            raise ValueError("Vectores deben tener la misma longitud")
        return Vector([a - b for a, b in zip(self.componentes, vec2.componentes)])

    def mult_escalar(self, escalar: Fraction) -> 'Vector':
        return Vector([escalar * c for c in self.componentes])

    def prod_punto(self, vec2: 'Vector') -> Fraction:
        if len(self) != len(vec2):
            raise ValueError("Vectores deben tener la misma longitud")
        return Fraction(sum(a * b for a, b in zip(self.componentes, vec2.componentes)))
