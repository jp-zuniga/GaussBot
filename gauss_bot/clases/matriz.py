from fractions import Fraction
from typing import Union, Tuple, List, Dict, overload

DictMatrices = Dict[str, "Matriz"]
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
    def __getitem__(self, indices: Tuple[int, int]) -> Fraction: ...

    @overload
    def __getitem__(self, indice_fila: int) -> List[Fraction]: ...

    def __getitem__(self, indice: int | Tuple[int, int]) -> Fraction | List[Fraction]:
        if isinstance(indice, int):
            if indice < 0 or indice >= self.filas:
                raise IndexError("Índice inválido")
            return self.valores[indice]
        elif isinstance(indice, tuple) and len(indice) == 2:
            fila, columna = indice
            if fila < 0 or columna < 0 or fila >= self.filas or columna >= self.columnas:
                raise IndexError("Índice inválido")
            return self.valores[fila][columna]
        else:
            raise TypeError("Índice inválido")

    def __setitem__(self, indices: Tuple[int, int], valor: Fraction) -> None:
        fila, columna = indices
        if fila < 0 or columna < 0 or fila >= self.filas or columna >= self.columnas:
            raise IndexError("Índice inválido")
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
            raise ArithmeticError("Las matrices deben tener las mismas dimensiones")
        mat_sumada = [
            [a + b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]
        return Matriz(self.aumentada, self.filas, self.columnas, mat_sumada)

    def __sub__(self, mat2: "Matriz") -> "Matriz":
        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ArithmeticError("Las matrices deben tener las mismas dimensiones")
        mat_restada = [
            [a - b for a, b in zip(filas1, filas2)]
            for filas1, filas2 in zip(self.valores, mat2.valores)
        ]
        return Matriz(self.aumentada, self.filas, self.columnas, mat_restada)

    @overload
    def __mul__(self, mat2: "Matriz") -> "Matriz": ...

    @overload
    def __mul__(self, escalar: Fraction) -> "Matriz": ...

    def __mul__(self, multiplicador: Union["Matriz", Fraction]) -> "Matriz":
        if isinstance(multiplicador, Matriz):
            if self.columnas != multiplicador.filas:
                raise ArithmeticError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz")

            mat_multiplicada = [[Fraction(0) for _ in range(multiplicador.columnas)] for _ in range(self.filas)]
            for i in range(self.filas):
                for j in range(multiplicador.columnas):
                    for k in range(self.columnas):
                        mat_multiplicada[i][j] += self.valores[i][k] * multiplicador.valores[k][j]

            return Matriz(self.aumentada, self.filas, multiplicador.columnas, mat_multiplicada)
        elif isinstance(multiplicador, Fraction):
            mat_multiplicada = [[multiplicador * valor for valor in fila] for fila in self.valores]
            return Matriz(self.aumentada, self.filas, self.columnas, mat_multiplicada)
        else:
            raise TypeError("Tipo de dato inválido")

    def transponer(self) -> "Matriz":
        mat_transpuesta = [[self.valores[j][i] for j in range(self.filas)] for i in range(self.columnas)]
        return Matriz(self.aumentada, self.columnas, self.filas, mat_transpuesta)

    def es_matriz_cero(self) -> bool:
        return all(all(x == Fraction(0) for x in fila) for fila in self.valores)
