from fractions import Fraction
from typing import Tuple, List, overload

Validacion = Tuple[bool, int]

class Matriz:
    def __init__(self, aumentada: bool, filas: int, columnas: int, valores: List[List[Fraction]] = []) -> None:
        self._aumentada = aumentada
        self._filas = filas
        self._columnas = columnas

        if valores == []:
            self._valores = [[Fraction(0) for _ in range(columnas)] for _ in range(filas)]
        else:
            self._valores = valores

    @property
    def aumentada(self) -> bool:
        return self._aumentada

    @property
    def filas(self) -> int:
        return self._filas

    @property
    def columnas(self) -> int:
        return self._columnas

    @property
    def valores(self) -> List[List[Fraction]]:
        return self._valores

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
        max_len = max(
            len(str(self.valores[i][j].limit_denominator(100)))
            for i in range(self.filas)
            for j in range(self.columnas)
        )

        matriz = ""
        for i in range(self.filas):
            for j in range(self.columnas):
                var = str(self.valores[i][j].limit_denominator(100)).center(max_len)
                if j == 0 and j == self.columnas - 1:
                    matriz += f"( {var} )"
                elif j == 0:
                    matriz += f"( {var}, "
                elif j == self.columnas - 2 and self.aumentada:
                    matriz += f"{var} | "
                elif j == self.columnas - 1:
                    matriz += f"{var} )"
                else:
                    matriz += f"{var}, "
            matriz += "\n"
        return matriz

    def __add__(self, mat2: "Matriz") -> "Matriz":
        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        M_sumada = [
            [a + b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]
        return Matriz(self.aumentada, self.filas, self.columnas, M_sumada)

    def __sub__(self, mat2: "Matriz") -> "Matriz":
        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        M_resta = [
            [a - b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]
        return Matriz(self.aumentada, self.filas, self.columnas, M_resta)

    def __mul__(self, mat2: "Matriz") -> "Matriz":
        if self.columnas != mat2.filas:
            raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz")

        M_mult = [[Fraction(0) for _ in range(mat2.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(mat2.columnas):
                for k in range(self.columnas):
                    M_mult[i][j] += self.valores[i][k] * mat2.valores[k][j]

        return Matriz(self.aumentada, self.filas, mat2.columnas, M_mult)

    def mult_escalar(self, escalar: Fraction) -> "Matriz":
        M_multiplicada = [[escalar * valor for valor in fila] for fila in self.valores]
        return Matriz(self.aumentada, self.filas, self.columnas, M_multiplicada)

    def transponer(self) -> "Matriz":
        M_t = [[self.valores[j][i] for j in range(self.filas)] for i in range(self.columnas)]
        return Matriz(self.aumentada, self.columnas, self.filas, M_t)
    
    def es_matriz_cero(self) -> bool:
        return all(all(x == Fraction(0) for x in fila) for fila in self.valores)
