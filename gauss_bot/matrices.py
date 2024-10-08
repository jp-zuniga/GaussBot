from fractions import Fraction
from typing import Callable, Tuple, List
from copy import deepcopy

from utils import Mat, DictMatrices, limpiar_pantalla
from sistemas_ecuaciones import reducir_matriz, imprimir_soluciones
from validaciones import validar_mats, validar_escalonada_reducida, encontrar_variables_libres


class Matriz:
    def __init__(self, aumentada: bool, filas: int, columnas: int, valores: List[List[Fraction]] = []):
        self.aumentada = aumentada
        self.filas = filas
        self.columnas = columnas

        if not valores:
            self.valores = [[Fraction(0) for _ in range(columnas)] for _ in range(filas)]
        else:
            self.valores = valores

    def __getitem__(self, indices: Tuple[int, int]) -> Fraction:
        fila, columna = indices
        return self.valores[fila][columna]

    def __setitem__(self, indices: Tuple[int, int], value: Fraction) -> None:
        fila, columna = indices
        self.valores[fila][columna] = value

    def matriz_str(self) -> List[str]:
        max_len = max(
            len(str(self.valores[i][j].limit_denominator(100)))
            for i in range(self.filas)
            for j in range(self.columnas)
        )

        output: List[str] = []
        for i in range(self.filas):
            fila = ""
            for j in range(self.columnas):
                var = str(self.valores[i][j].limit_denominator(100)).center(max_len)
                if j == 0 and j == self.columnas - 1:  # para matrices de m x 1
                    fila += f"( {var} )"
                elif j == 0:
                    fila += f"( {var}, "
                elif j == self.columnas - 2 and self.aumentada:  # para separar la columna aumentada
                    fila += f"{var} |"
                elif j == self.columnas - 1:
                    fila += f"{var} )"
                else:
                    fila += f"{var}, "
            output.append(fila)
        return output

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


class OperacionesMatrices:
    def __init__(self, default_mats: DictMatrices = {}) -> None:
        self.mats_ingresadas = default_mats


    def imprimir_matriz(self, M: Mat, es_aumentada=True) -> None:
        filas = len(M)
        columnas = len(M[0])
        max_len = max(
            len(str(M[i][j].limit_denominator(100)))
            for i in range(filas)
            for j in range(columnas)
        )

        for i in range(filas):
            for j in range(columnas):
                elem = str(M[i][j].limit_denominator(100)).center(max_len)

                if j == 0 and j == columnas - 1:  # para matrices de m x 1
                    print(f"( {elem} )")
                elif j == 0:
                    print(f"( {elem}, ", end="")
                elif j == columnas - 2 and es_aumentada:  # para separar la columna aumentada
                    print(f"{elem} |", end=" ")
                elif j == columnas - 1:
                    print(f"{elem} )")
                else:
                    print(f"{elem}, ", end="")

        return None


    def imprimir_matrices(self) -> None:
        if not validar_mats(self.mats_ingresadas):
            return None

        print("\nMatrices guardadas:")
        print("---------------------------------------------", end="")
        for nombre, mat in self.mats_ingresadas.items():
            print(f"\n{nombre}:")
            self.imprimir_matriz(mat[0], mat[1])
        print("---------------------------------------------")

        return None


    def menu_matrices(self) -> int:
        limpiar_pantalla()
        print("\n###############################")
        print("### Operaciones Matriciales ###")
        print("###############################")
        self.imprimir_matrices()
        print("\n1. Agregar una matriz")
        print("2. Resolver sistema de ecuaciones")
        print("3. Suma y resta de matrices")
        print("4. Multiplicación de matrices")
        print("5. Transposición de una matriz")
        print("6. Regresar al menú principal")

        try:
            option = int(input("\nSeleccione una opción: ").strip())
            if option < 1 or option > 6:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_matrices()

        return option


    def main_matrices(self) -> None:
        option = self.menu_matrices()
        while option != 7:
            match option:
                case 1:
                    self.agregar_matriz()
                    option = self.menu_matrices()
                    continue
                case 2:
                    self.procesar_operacion("r", self.resolver_sistema)
                    match input("\n¿Desea resolver otra matriz? (s/n) ").strip().lower():
                        case "s":
                            continue
                        case "n":
                            input("De acuerdo! Regresando al menú de matrices...")
                        case _:
                            input("Opción inválida! Regresando al menú de matrices...")
                    option = self.menu_matrices()
                    continue
                case 3:
                    self.procesar_operacion("msr", self.suma_resta_matrices)
                    option = self.menu_matrices()
                    continue
                case 4:
                    self.procesar_operacion("msr", self.mult_matrices)
                    option = self.menu_matrices()
                    continue
                case 5:
                    self.procesar_operacion("t", self.transponer)
                    option = self.menu_matrices()
                    continue
                case 6:
                    input("Regresando al menú principal...")
                    break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue

        return None


    def agregar_matriz(self) -> None:
        try:
            limpiar_pantalla()
            nombre = input("\nIngrese el nombre de la matriz (una letra mayúscula): ").strip().upper()
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError("Error: Ingrese solamente una letra mayúscula!")
            if nombre in self.mats_ingresadas:
                raise KeyError(f"Error: Ya hay una matriz con el nombre {nombre}!")

            match input("¿Se ingresará una matriz aumentada? (s/n) ").strip().lower():
                case "s":
                    es_aumentada = True
                case "n":
                    es_aumentada = False
                case _:
                    raise ValueError("Error: Ingrese una opción válida!")

        except NameError as n:
            input(n)
            return self.agregar_matriz()
        except KeyError as k:
            input(k)
            return self.agregar_matriz()
        except ValueError as v:
            input(v)
            return self.agregar_matriz()

        self.mats_ingresadas[nombre] = (self.pedir_matriz(es_aumentada, nombre), es_aumentada)
        print("\nMatriz agregada exitosamente!")

        match input("¿Desea agregar otra matriz? (s/n) ").strip().lower():
            case "s":
                return self.agregar_matriz()
            case "n":
                input("Regresando al menú de matrices...")
            case _:
                input("Opción inválida! Regresando al menú de matrices...")

        return None


    def pedir_datos_matriz(self, es_aumentada: bool, nombre: str) -> Tuple[int, int]:
        palabras = ["ecuaciones", "variables"] if es_aumentada else ["filas", "columnas"]
        print(f"\nDatos de matriz {nombre}:")
        print("----------------------------")
        try:
            filas = int(input(f"Ingrese el número de {palabras[0]}: "))
            if filas <= 0:
                raise ValueError("Error: Ingrese un número entero positivo!")
            columnas = int(input(f"Ingrese el número de {palabras[1]}: "))
            if columnas <= 0:
                raise ValueError("Error: Ingrese un número entero positivo!")

        except ValueError as v:
            input(v)
            return self.pedir_datos_matriz(es_aumentada, nombre)
        return (filas, columnas)


    def pedir_matriz(self, es_aumentada=True, nombre="M") -> Mat:
        M = []
        filas, columnas = self.pedir_datos_matriz(es_aumentada, nombre)

        fila_actual = 0
        if es_aumentada:
            columnas += 1

        while fila_actual < filas:
            columna_actual = 0
            fila = []
            print(f"\nFila {fila_actual+1}:")
            while columna_actual < columnas:
                try:
                    if not es_aumentada or columna_actual != columnas - 1:
                        dato = f"-> X{columna_actual+1} = "
                    else:
                        dato = "-> b = "

                    elem = Fraction(input(dato).strip()).limit_denominator(100)
                    fila.append(elem)
                    columna_actual += 1

                except ValueError:
                    input("\nError: Ingrese un número real!")
                    print()
                except ZeroDivisionError:
                    input("\nError: El denominador no puede ser cero!")
                    print()

            fila_actual += 1
            M.append(fila)
        return M


    def seleccionar_matriz(self, operacion: str) -> str:
        if operacion not in ("r", "t"):
            return ""
        if not validar_mats(self.mats_ingresadas):
            return ""

        match operacion:
            case "r":
                mensaje = "resolver"
            case "t":
                mensaje = "transponer"

        mensaje = f"\n¿Cuál matriz desea {mensaje}? "
        try:
            limpiar_pantalla()
            self.imprimir_matrices()
            input_mat = input(mensaje).strip()

            if input_mat not in self.mats_ingresadas:
                raise KeyError(f"Error: La matriz {input_mat} no existe!")
            elif operacion == "r" and not self.mats_ingresadas[input_mat[0]][1]:
                raise TypeError("Error: La matriz seleccionada no es aumentada!")

        except KeyError as k:
            input(k)
            return self.seleccionar_matriz(operacion)
        except TypeError as v:
            input(v)
            return self.seleccionar_matriz(operacion)

        return input_mat


    def seleccionar_matrices(self) -> List[str]:
        if not validar_mats(self.mats_ingresadas):
            return []

        mensaje = "\n¿Cuáles matrices desea seleccionar? (separadas por comas) "
        try:
            limpiar_pantalla()
            self.imprimir_matrices()
            input_mats = input(mensaje).strip().split(",")
            mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)

            if mat is not None:
                raise KeyError(f"Error: La matriz {mat} no existe!")
            elif len(input_mats) != 2:
                raise ValueError("Error: Debe seleccionar dos matrices!")

        except KeyError as k:
            input(k)
            return self.seleccionar_matrices()
        except ValueError as v:
            input(v)
            return self.seleccionar_matrices()

        return input_mats


    def procesar_operacion(self, operacion: str, func: Callable) -> None:
        match operacion:
            case "msr":
                func()
                return None
            case "r":
                nombre_mat = self.seleccionar_matriz("r")
                nombre_mat_modded = f"{nombre_mat}_r"
            case "t":
                nombre_mat = self.seleccionar_matriz("t")
                nombre_mat_modded = f"{nombre_mat}_t"

        copia = deepcopy(self.mats_ingresadas[nombre_mat])
        modded_copia = func(copia[0], copia[1])

        mat_existe = any(modded_copia == mat[0] for mat in self.mats_ingresadas.values())
        if not mat_existe:
            self.mats_ingresadas[nombre_mat_modded] = (modded_copia, copia[1])

        input("\nPresione cualquier tecla para continuar...")
        return None


    def resolver_sistema(self, M: Mat, es_aumentada=True) -> Mat | None:
        M = reducir_matriz(M)
        if not M:
            return None

        libres = encontrar_variables_libres(M)
        if validar_escalonada_reducida(M) and not libres:  # solucion unica:
            imprimir_soluciones(M, unica=True, libres=[], validacion=(True, -1))
            return M

        # solucion general:
        imprimir_soluciones(M, unica=False, libres=libres, validacion=(True, -1))
        return M


    def suma_resta_matrices(self) -> Mat | None:
        inputs = self.seleccionar_matriz("msr")
        A, B = self.mats_ingresadas[inputs[0]][0], self.mats_ingresadas[inputs[1]][0]
        filas_A = len(A)
        filas_B = len(B)
        columnas_A = len(A[0])
        columnas_B = len(B[0])

        if filas_A != filas_B or columnas_A != columnas_B:
            input("\nError: Las matrices deben tener las mismas dimensiones!")
            return self.suma_resta_matrices()

        operacion = input("\n¿Desea sumar o restar las matrices? (+/-) ").strip()
        if operacion not in ("+", "-"):
            input("Error: Ingrese un operador válido!")
            return self.suma_resta_matrices()

        limpiar_pantalla()
        print(f"\n{inputs[0]}:")
        self.imprimir_matriz(A, es_aumentada=False)
        print(f"\n{inputs[1]}:")
        self.imprimir_matriz(B, es_aumentada=False)

        if operacion == "+":
            C = [[A[i][j] + B[i][j] for j in range(columnas_A)] for i in range(filas_A)]
        elif operacion == "-":
            C = [[A[i][j] - B[i][j] for j in range(columnas_A)] for i in range(filas_A)]

        print(f"\n{inputs[0]} {operacion} {inputs[1]}:")
        self.imprimir_matriz(C, es_aumentada=False)
        input("\nPresione cualquier tecla para continuar...")
        return C


    def mult_matrices(self) -> Mat | None:
        inputs = self.seleccionar_matriz("msr")
        A, B = self.mats_ingresadas[inputs[0]][0], self.mats_ingresadas[inputs[1]][0]
        filas_A = len(A)
        filas_B = len(B)
        columnas_A = len(A[0])
        columnas_B = len(B[0])

        if columnas_A != filas_B:
            input(f"\nError: El número de columnas de {inputs[0]} debe ser igual al número de filas de {inputs[1]}!")
            return self.mult_matrices()

        limpiar_pantalla()
        print(f"\n{inputs[0]}:")
        self.imprimir_matriz(A, es_aumentada=False)
        print(f"\n{inputs[1]}:")
        self.imprimir_matriz(B, es_aumentada=False)

        C = [[Fraction(0) for _ in range(columnas_B)] for _ in range(filas_A)]
        for i in range(filas_A):
            for j in range(columnas_B):
                for k in range(columnas_A):
                    C[i][j] += A[i][k] * B[k][j]

        print(f"\n{inputs[0]} * {inputs[1]}:")
        self.imprimir_matriz(C, es_aumentada=False)
        input("\nPresione cualquier tecla para continuar...")
        return C


    def transponer(self, M: Mat, es_aumentada: bool) -> Mat:
        filas = len(M)
        columnas = len(M[0])

        M_t = [[Fraction(0) for _ in range(filas)] for _ in range(columnas)]
        for i in range(filas):
            for j in range(columnas):
                M_t[j][i] = M[i][j]

        print("\nTransposición:")
        self.imprimir_matriz(M_t, es_aumentada)
        return M_t
