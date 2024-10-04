from fractions import Fraction
from typing import List
from utils import Mat, DictMatrices, limpiar_pantalla

# funciones para trabajar con matrices y resolver sistemas de ecuaciones
# --------------------------------------------------------------------------------

class Matriz:
    def __init__(self):
        from validaciones import Validaciones
        self.vals = Validaciones()
        self.mats_ingresadas = {}

    def imprimir_matriz(self, M: Mat, es_aumentada=True) -> None:
        filas = len(M)
        columnas = len(M[0])

        # calcular la longitud maxima de los elementos para alinearlos y siempre mantener el formato:
        # - crear una lista de las longitudes de todos los elementos de la matriz
        # - encontrar la longitud maxima en esa lista con max()
        max_len = max(len(str(M[i][j].limit_denominator(100))) for i in range(filas) for j in range(columnas))
        for i in range(filas):
            for j in range(columnas):
                # convertir el elemento actual a un string y ajustarlo a la derecha de la longitud maxima
                elemento = str(M[i][j].limit_denominator(100)).center(max_len)

                # si es el primer elemento, imprimir el ( y una coma despues del elemento
                if j == 0: print(f"( {elemento}, ", end='')

                # si es aumentada y j es el penultimo elemento, imprimir el | para separar las columnas
                elif j == columnas-2 and es_aumentada: print(f"{elemento} |", end=' ')

                # si el es el ultimo elemento, cerrar el )
                elif j == columnas-1: print(f"{elemento} )")

                # si es un elemento en medio, solo imprimir la coma despues del elemento    
                else: print(f"{elemento}, ", end='')

        return None

    def imprimir_matrices(self) -> None:
        if not self.vals.validar_mats(self.mats_ingresadas): return None
        print("\nMatrices guardadas:")
        print("---------------------------------------------", end='')
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
            if option < 1 or option > 6: raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_matrices()
        return option

    def operaciones_matriciales(self) -> None:
        option = self.menu_matrices()
        while option != 7:
            match option:
                case 1:
                    limpiar_pantalla()
                    self.mats_ingresadas = self.agregar_matriz()
                    option = self.menu_matrices()
                    continue
                case 2:
                    from sistemas_ecuaciones import SistemaEcuaciones
                    M = self.mats_ingresadas[self.seleccionar_matriz(es_sistema=True)][0]
                    M = SistemaEcuaciones().resolver_sistema(M)
                    match input("\n¿Desea resolver otra matriz? (s/n) ").strip().lower():
                        case 's': continue
                        case 'n':
                            input("De acuerdo! Regresando al menú de matrices...")
                            option = self.menu_matrices()
                            continue
                        case _:
                            input("Opción inválida! Regresando al menú de matrices...")
                            option = self.menu_matrices()
                            continue
                case 3:
                    limpiar_pantalla()
                    M = self.suma_resta_matrices()
                    option = self.menu_matrices()
                    continue
                case 4:
                    limpiar_pantalla()
                    M = self.mult_matrices()
                    option = self.menu_matrices()
                    continue
                case 5: break
                case 6: break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue

        input("Regresando al menú principal...")
        return None

    def agregar_matriz(self) -> DictMatrices:
        try:
            limpiar_pantalla()
            nombre = input("Ingrese el nombre de la matriz (una letra mayúscula): ").strip().upper()
            if not nombre.isalpha() or len(nombre) != 1: raise NameError
            if nombre in self.mats_ingresadas: raise KeyError
            match input("¿Se ingresará una matriz aumentada? (s/n) ").strip().lower():
                case 's': es_aumentada = True
                case 'n': es_aumentada = False
                case _: raise ValueError
        except NameError:
            input("Error: Ingrese solamente una letra mayúscula!")
            return self.agregar_matriz()
        except KeyError:
            input(f"Error: Ya hay un vector con el nombre {nombre}!")
            return self.agregar_matriz()
        except ValueError:
            input("Error: Ingrese una opción válida!")
            return self.agregar_matriz()

        self.mats_ingresadas[nombre] = (self.pedir_matriz(es_aumentada, nombre), es_aumentada)
        print(f"\nMatriz agregada exitosamente!")
        
        match input("¿Desea agregar otra matriz? (s/n) ").strip().lower():
            case 's': return self.agregar_matriz()
            case 'n': input("Regresando al menú de matrices...")
            case _: input("Opción inválida! Regresando al menú de matrices...")
        return self.mats_ingresadas

    def pedir_matriz(self, es_aumentada=True, nombre='M') -> Mat:
        M = []
        mensaje = ["ecuaciones", "variables"] if es_aumentada else ["filas", "columnas"]
        print(f"\nDatos de la matriz {nombre}:")
        print("----------------------------")

        try:
            filas = int(input(f"Ingrese el número de {mensaje[0]}: "))
            if filas <= 0: raise ValueError
            columnas = int(input(f"Ingrese el número de {mensaje[1]}: "))
            if columnas <= 0: raise ValueError
        except ValueError:
            input("Error: Ingrese un número entero positivo!")
            return self.pedir_matriz(es_aumentada, nombre)
        
        fila_actual = 0
        if es_aumentada: columnas += 1

        while fila_actual < filas:
            columna_actual = 0
            fila = []
            print(f"\nFila {fila_actual+1}:")
            while columna_actual < columnas: 
                try:
                    if not es_aumentada or columna_actual != columnas-1: mensaje = f"-> X{columna_actual+1} = "
                    else: mensaje = "-> b = "
                    elemento = Fraction(input(mensaje).strip()).limit_denominator(100)
                    fila.append(elemento)
                    columna_actual += 1
                except ValueError: input("\nError: Ingrese un número real!\n")
                except ZeroDivisionError: input("\nError: El denominador no puede ser cero!\n")
            fila_actual += 1
            M.append(fila)

        return M

    def seleccionar_matriz(self, es_sistema=False) -> List[str] | None:
        if not self.vals.validar_mats(self.mats_ingresadas): return None
        if es_sistema: mensaje = "\n¿Cuál matriz desea resolver? "
        else: mensaje = "\n¿Cuáles matrices desea seleccionar? (nombres separados por comas) "

        try:
            limpiar_pantalla()
            self.imprimir_matrices()
            input_mats = input(mensaje).strip().split(',')
            for mat in input_mats:
                if mat not in self.mats_ingresadas: raise KeyError(mat)
            
            if not es_sistema and len(input_mats) != 2: raise ValueError("Error: Debe seleccionar dos matrices!")
            elif es_sistema and len(input_mats) != 1: raise ValueError("Error: Solo debe seleccionar una matriz!")
            elif es_sistema and not self.mats_ingresadas[input_mats[0]][1]: raise ValueError("Error: La matriz seleccionada no es aumentada!")
            elif not es_sistema and self.mats_ingresadas[input_mats[0][1]] or self.mats_ingresadas[input_mats[1][1]]:
                raise ValueError("Error: Las matrices seleccionadas no pueden ser aumentadas!")
        except KeyError as k:
            input(f"Error: La matriz '{k}' no existe!")
            return self.seleccionar_matriz(es_sistema)
        except ValueError as v:
            input(v)
            return self.seleccionar_matriz(es_sistema)
        if es_sistema: return input_mats[0]
        else: return input_mats

    def suma_resta_matrices(self) -> Mat:
        A, B = self.seleccionar_matriz()
        filas_A = len(A)
        filas_B = len(B)
        columnas_A = len(A[0])
        columnas_B = len(B[0])

        if filas_A != filas_B or columnas_A != columnas_B:
            input("\nError: Las matrices deben tener las mismas dimensiones!")
            return None
        
        option = input("\n¿Desea sumar o restar las matrices? (+/-) ").strip()
        if option not in ('+', '-'):
            input("Error: Ingrese un operador válido!")
            return None
        
        limpiar_pantalla()
        print("\nMatriz A:")
        self.imprimir_matriz(A, es_aumentada=False)
        print("\nMatriz B:")
        self.imprimir_matriz(B, es_aumentada=False)

        if option == '+': C = [[A[i][j] + B[i][j] for j in range(len(columnas_A))] for i in range(filas_A)]
        elif option == '-': C = [[A[i][j] - B[i][j] for j in range(len(columnas_A))] for i in range(filas_A)]

        print(f"\nMatriz A {option} B:")
        self.imprimir_matriz(C, es_aumentada=False)
        input("\nPresione cualquier tecla para continuar...")
        return C

    def mult_matrices(self) -> Mat:
        A, B = self.seleccionar_matriz()
        filas_A = len(A)
        filas_B = len(B)
        columnas_A = len(A[0])
        columnas_B = len(B[0])

        if columnas_A != filas_B:
            input("\nError: El número de columnas de A debe ser igual al número de filas de B!")
            return None

        limpiar_pantalla()
        print("\nMatriz A:")
        self.imprimir_matriz(A, es_aumentada=False)
        print("\nMatriz B:")
        self.imprimir_matriz(B, es_aumentada=False)

        C = [[0 for _ in range(len(columnas_B))] for _ in range(filas_A)]
        for i in range(filas_A):
            for j in range(len(columnas_B)):
                for k in range(filas_A):
                    C[i][j] += A[i][k] * B[k][j]

        print("\nA * B:")
        self.imprimir_matriz(C, es_aumentada=False)
        input("\nPresione cualquier tecla para continuar...")
        return C
