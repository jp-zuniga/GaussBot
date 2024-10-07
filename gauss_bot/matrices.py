from fractions import Fraction
from typing import List, Tuple
from copy import deepcopy

from utils import Mat, DictMatrices, limpiar_pantalla
from sistemas_ecuaciones import resolver_sistema
from validaciones import validar_mats


class Matriz:
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


    def main_matriciales(self) -> None:
        option = self.menu_matrices()
        while option != 7:
            match option:
                case 1:
                    self.agregar_matriz()
                    option = self.menu_matrices()
                    continue
                case 2:
                    nombre_mat = self.seleccionar_matriz("r")
                    nombre_mat_resuelta = f"{nombre_mat}_r"
                    M = deepcopy(self.mats_ingresadas[nombre_mat][0])
                    M = resolver_sistema(M)

                    matriz_existe = any(M == mat[0] for mat in self.mats_ingresadas.values())
                    if not matriz_existe:
                        self.mats_ingresadas[nombre_mat_resuelta] = (M, True)

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
                    self.suma_resta_matrices()
                    option = self.menu_matrices()
                    continue
                case 4:
                    self.mult_matrices()
                    option = self.menu_matrices()
                    continue
                case 5:
                    nombre_mat = self.seleccionar_matriz("t")
                    nombre_mat_resuelta = f"{nombre_mat}_t"
                    copia = deepcopy(self.mats_ingresadas[nombre_mat])
                    M = self.transponer(copia[0], copia[1])

                    matriz_existe = any(M == mat[0] for mat in self.mats_ingresadas.values())
                    if not matriz_existe:
                        self.mats_ingresadas[nombre_mat_resuelta] = (M, copia[1])

                    input("\nPresione cualquier tecla para continuar...")
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
                raise KeyError(f"Error: Ya hay un vector con el nombre {nombre}!")

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


    def seleccionar_matriz(self, operacion: str) -> str | List[str]:
        if not validar_mats(self.mats_ingresadas):
            return []

        es_sistema = transponer = mult_suma_resta = False
        match operacion:
            case "r":
                es_sistema = True
            case "t":
                transponer = True
            case "msr":
                mult_suma_resta = True

        if es_sistema:
            mensaje = "\n¿Cuál matriz desea resolver? "
        elif transponer:
            mensaje = "\n¿Cuál matriz desea transponer? "
        elif mult_suma_resta:
            mensaje = "\n¿Cuáles matrices desea seleccionar? (nombres separados por comas) "

        try:
            limpiar_pantalla()
            self.imprimir_matrices()
            input_mats = input(mensaje).strip().split(",")
            aumentadas = all(self.mats_ingresadas[mat][1] for mat in input_mats)
            mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)

            if mat is not None:
                raise KeyError(f"Error: La matriz {mat} no existe!")
            elif mult_suma_resta and len(input_mats) != 2:
                raise ValueError("Error: Debe seleccionar dos matrices!")
            elif (es_sistema or transponer) and len(input_mats) != 1:
                raise ValueError("Error: Solo debe seleccionar una matriz!")
            elif es_sistema and not aumentadas:
                raise ValueError("Error: La matriz seleccionada no es aumentada!")

        except KeyError as k:
            input(k)
            return self.seleccionar_matriz(operacion)
        except ValueError as v:
            input(v)
            return self.seleccionar_matriz(operacion)

        if es_sistema or transponer:
            return input_mats[0]
        else:
            return input_mats


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
