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

    @filas.setter
    def filas(self, value: int) -> None:
        self._filas = value

    @property
    def columnas(self) -> int:
        return self._columnas

    @columnas.setter
    def columnas(self, value: int) -> None:
        self._columnas = value

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

    def es_matriz_cero(self) -> bool:
        return all(all(x == Fraction(0) for x in fila) for fila in self.valores)

    def get_mat_str(self) -> str:
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

    def agregar_fila(self, fila: List[Fraction]) -> None:
        if len(fila) != self.columnas:
            raise ValueError("La longitud de la fila debe coincidir con el número de columnas")
        self.valores.append(fila)
        self.filas += 1

    def agregar_columna(self, columna: List[Fraction]) -> None:
        if len(columna) != self.filas:
            raise ValueError("La longitud de la columna debe coincidir con el número de filas")
        for i in range(self.filas):
            self.valores[i].append(columna[i])
        self.columnas += 1

    def eliminar_fila(self, indice_fila: int) -> None:
        if 0 <= indice_fila < self.filas:
            self.valores.pop(indice_fila)
            self.filas -= 1
        else:
            raise IndexError("Índice de fila fuera de rango")

    def eliminar_columna(self, indice_columna: int) -> None:
        if 0 <= indice_columna < self.columnas:
            for fila in self.valores:
                fila.pop(indice_columna)
            self.columnas -= 1
        else:
            raise IndexError("Índice de columna fuera de rango")

    def validar_consistencia(self) -> Validacion:
        if self.valores == [] or self.es_matriz_cero():
            return (True, -1)

        for i in range(self.filas):
            # validar forma de 0 = b (donde b != 0)
            if [0 for _ in range(len(self.valores[0]) - 1)] == self.valores[i][:-1] and self.valores[i][-1] != 0:
                return (False, i)

        return (True, -1)

    def validar_escalonada(self) -> bool:
        fila_cero = [0 for _ in range(self.columnas)]
        entrada_anterior = -1

        if self.valores == [] or self.es_matriz_cero():
            return False

        # buscar filas no-cero despues de una fila cero, significa que no es escalonada
        for i in range(self.filas):
            if self.valores[i] != fila_cero:
                continue
            if any(self.valores[j] != fila_cero for j in range(i + 1, self.filas)):
                return False

        # validar entradas principales
        for i in range(self.filas):
            try:
                entrada_actual = next(j for j in range(self.columnas - 1) if self.valores[i][j] != 0)
            except StopIteration:
                continue
            if entrada_actual <= entrada_anterior:
                return False
            if any(self.valores[k][entrada_actual] != 0 for k in range(i + 1, self.filas)):
                return False
            entrada_anterior = entrada_actual

        return True

    def validar_escalonada_reducida(self) -> bool:
        if not self.validar_escalonada():  # si no es escalonada, no puede ser escalonada reducida
            return False

        # validar entradas principales
        for i in range(self.filas):
            try:
                entrada_principal = next(j for j in range(self.columnas - 1) if self.valores[i][j] == 1)
            except StopIteration:
                continue
            if any(self.valores[k][entrada_principal] != 0 and k != i for k in range(self.filas)):
                return False

        return True

    def sumar_mats(self, mat2: "Matriz") -> "Matriz":
        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        M_sumada = [[self.valores[i][j] + mat2.valores[i][j] for j in range(self.columnas)] for i in range(self.filas)]
        return Matriz(self.aumentada, self.filas, self.columnas, M_sumada)

    def restar_mats(self, mat2: "Matriz") -> "Matriz":
        if self.filas != mat2.filas or self.columnas != mat2.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        M_resta = [[self.valores[i][j] - mat2.valores[i][j] for j in range(self.columnas)] for i in range(self.filas)]
        return Matriz(self.aumentada, self.filas, self.columnas, M_resta)

    def mult_escalar(self, escalar: Fraction) -> "Matriz":
        M_multiplicada = [[escalar * valor for valor in fila] for fila in self.valores]
        return Matriz(self.aumentada, self.filas, self.columnas, M_multiplicada)

    def mult_matrices(self, mat2: "Matriz") -> "Matriz":
        if self.columnas != mat2.filas:
            raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz")

        M_mult = [[Fraction(0) for _ in range(mat2.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(mat2.columnas):
                for k in range(self.columnas):
                    M_mult[i][j] += self.valores[i][k] * mat2.valores[k][j]

        return Matriz(self.aumentada, self.filas, mat2.columnas, M_mult)

    def transponer(self) -> "Matriz":
        M_t = [[self.valores[j][i] for j in range(self.filas)] for i in range(self.columnas)]
        return Matriz(self.aumentada, self.columnas, self.filas, M_t)
