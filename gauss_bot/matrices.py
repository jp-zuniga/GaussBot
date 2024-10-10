from fractions import Fraction
from typing import Tuple, List, Dict, overload
from copy import deepcopy

from utils import limpiar_pantalla

# type annotations:
DictMatrices = Dict[str, "Matriz"]
Validacion = Tuple[bool, int]


class Matriz:
    def __init__(self, aumentada: bool, filas: int, columnas: int, valores: List[List[Fraction]] = []):
        self.aumentada = aumentada
        self.filas = filas
        self.columnas = columnas

        if valores == []:
            self.valores = [[Fraction(0) for _ in range(columnas)] for _ in range(filas)]
        else:
            self.valores = valores

    @overload
    def __getitem__(self, indice_fila: int) -> List[Fraction]: ...

    @overload
    def __getitem__(self, indices: Tuple[int, int]) -> Fraction: ...

    def __getitem__(self, indice):
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


class SistemaEcuaciones:
    def __init__(self, matriz: Matriz) -> None:
        self.matriz = matriz
        self.filas = matriz.filas
        self.columnas = matriz.columnas

        self.respuesta: List[str] = []
        self.procedimiento: List[str] = []

    def resolver_sistema(self) -> None:
        self.reducir_matriz()
        if self.matriz.es_matriz_cero():
            return None

        libres = self.encontrar_variables_libres()
        if self.matriz.validar_escalonada_reducida() and not libres:  # solucion unica:
            self.imprimir_soluciones(unica=True, libres=[], validacion=(True, -1))
            return None

        # solucion general:
        self.imprimir_soluciones(unica=False, libres=libres, validacion=(True, -1))
        return None

    def reducir_matriz(self) -> None:
        test_inicial = self.matriz.validar_consistencia()
        if not test_inicial[0]:
            self.imprimir_soluciones(unica=False, libres=[], validacion=test_inicial)
            return None
        elif self.matriz.validar_escalonada_reducida():
            self.procedimiento.append("\nMatriz ya esta en su forma escalonada reducida!\n")
            return None

        self.procedimiento.append("\nMatriz inicial:\n")
        self.procedimiento.append(self.matriz.get_mat_str())
        self.procedimiento.append("\nReduciendo la matriz a su forma escalonada:\n")

        fila_actual = 0
        for j in range(self.columnas - 1):  # encontrar pivotes y eliminar elementos debajo
            fila_pivote = None
            maximo = Fraction(0)

            # buscar la entrada con el valor mas grande para usarla como pivote
            for i in range(fila_actual, self.filas):
                if abs(self.matriz[i, j]) > maximo:
                    maximo = abs(self.matriz[i, j])
                    fila_pivote = i

            # si las variables siguen iguales, no hay pivote y se pasa a la siguiente columna
            if fila_pivote is None or maximo == 0:
                continue

            # siempre trabajar con la fila pivote
            if fila_pivote != fila_actual:
                self.matriz.valores[fila_actual], self.matriz.valores[fila_pivote] = self.matriz.valores[fila_pivote], self.matriz.valores[fila_actual]
                self.procedimiento.append(f"\nF{fila_actual+1} <==> F{fila_pivote+1}\n")
                self.procedimiento.append(self.matriz.get_mat_str())

            pivote = self.matriz[fila_actual][j]
            if pivote != 1 and pivote != 0:  # hacer el pivote igual a 1
                for k in range(self.columnas):
                    self.matriz[fila_actual][k] /= pivote
                if pivote == -1:
                    self.procedimiento.append(f"\nF{fila_actual+1} => -F{fila_actual+1}\n")
                else:
                    self.procedimiento.append(f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote.limit_denominator(100))}\n")

                self.procedimiento.append(self.matriz.get_mat_str())

            # eliminar los elementos debajo del pivote
            for f in range(fila_actual + 1, self.filas):
                factor = self.matriz[f][j]
                if factor == 0:
                    continue
                for k in range(self.columnas):
                    self.matriz[f][k] -= factor * self.matriz[fila_actual][k]

                self.procedimiento.append(f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor.limit_denominator(100))} * F{fila_pivote+1})\n")
                self.procedimiento.append(self.matriz.get_mat_str())

            fila_actual += 1

        for i in reversed(range(self.filas)):  # eliminar elementos arriba de pivotes
            try:
                columna_pivote = self.matriz[i].index(next(filter(lambda x: x != 0, self.matriz[i])))
            except StopIteration:
                columna_pivote = None
            if columna_pivote is None:  # no hay entrada principal
                continue

            # eliminar los elementos encima del pivote
            for f in reversed(range(i)):
                factor = self.matriz[f][columna_pivote]
                if factor == 0:
                    continue
                for k in range(self.columnas):
                    self.matriz[f][k] -= factor * self.matriz[i][k]

                self.procedimiento.append(f"\nF{f+1} => F{f+1} - ({str(factor.limit_denominator(100))} * F{i+1})\n")
                self.procedimiento.append(self.matriz.get_mat_str())

        test_final = self.matriz.validar_consistencia()
        if not test_final[0]:
            self.imprimir_soluciones(unica=False, libres=[], validacion=test_final)
            return None
        return None

    def encontrar_variables_libres(self) -> List[int]:
        entradas = []

        # encontrar entradas principales
        for i in range(self.matriz.filas):
            try:
                entradas.append(next(j for j in range(self.matriz.columnas - 1) if self.matriz[i][j] != 0))
            except StopIteration:
                continue

        # si no son entradas principales, son variables libres
        return [x for x in range(self.matriz.columnas - 1) if x not in entradas]

    def despejar_variables(self, libres: List[int]) -> List[str]:
        ecuaciones = []
        for x in libres:
            ecuaciones.append(f"| X{x+1} es libre\n")

        for i in range(self.filas):
            for j in range(self.columnas - 1):
                if self.matriz[i, j] == 0:
                    continue

                constante = self.matriz[i, -1].limit_denominator(100)
                expresion = str(constante) if constante != 0 else ""
                for k in range(j + 1, self.columnas - 1):
                    if self.matriz[i, k] == 0:
                        continue

                    coeficiente = -self.matriz[i, k].limit_denominator(100)
                    signo = "+" if coeficiente >= 0 else "-"
                    if expresion:
                        signo = f" {signo} "
                    else:
                        signo = "" if signo == "+" else "-"

                    variable = (
                        f"{abs(coeficiente)}*X{k+1}"
                        if abs(coeficiente) != 1
                        else f"X{k+1}"
                    )

                    expresion += f"{signo}{variable}"

                if expresion == "":
                    expresion = "0"

                ecuaciones.append(f"| X{j+1} = {expresion}\n")
                break

        ecuaciones.sort(key=lambda x: x[3])
        return ecuaciones

    def imprimir_soluciones(self, unica: bool, libres: List[int], validacion: Validacion) -> None:
        solucion, fila_inconsistente = validacion
        if not solucion and fila_inconsistente != -1:
            self.respuesta.append(f"\n| En F{fila_inconsistente+1}: 0 != {str(self.matriz[fila_inconsistente, -1].limit_denominator(100))}\n")
            self.respuesta.append("| Sistema es inconsistente!\n")
            return None

        elif unica:
            solucion_trivial = all(self.matriz[i, -1] == 0 for i in range(self.filas))
            mensaje_solucion = "trivial" if solucion_trivial else "no trivial"

            self.respuesta.append(f"\n| Solución {mensaje_solucion} encontrada:\n")
            for i in range(self.filas):
                if all(x == 0 for x in self.matriz[i]):
                    continue
                self.respuesta.append(f"| X{i+1} = {str(self.matriz[i, -1].limit_denominator(100))}\n")
            return None

        ecuaciones = self.despejar_variables(libres)
        self.respuesta.append("\n| Sistema no tiene solución única!\n")
        self.respuesta.append("| Solución general encontrada:\n")
        for linea in ecuaciones:
            self.respuesta.append(linea)

        return None


class OperacionesMatrices:
    def __init__(self, default_mats: DictMatrices = {}) -> None:
        self.mats_ingresadas = default_mats

    def main_matrices(self) -> None:
        option = self.menu_matrices()
        while option != 7:
            match option:
                case 1:  # agregar
                    self.agregar_matriz()
                    option = self.menu_matrices()
                    continue
                case 2:  # resolver sistema de ecuaciones
                    respuesta, procedimiento, mat_resultante = self.procesar_operacion("se")
                    print("\n---------------------------------------------")
                    print("\nSistema de ecuaciones resuelto:")
                    for linea in mat_resultante.get_mat_str():
                        print(linea, end="")
                    for linea in respuesta:
                        print(linea, end="")

                    print("\n---------------------------------------------")
                    mostrar_procedimiento = self._match_input("\n¿Desea ver el procedimiento? (s/n) ")
                    if mostrar_procedimiento:
                        limpiar_pantalla()
                        for linea in procedimiento:
                            print(linea, end="")
                        for linea in respuesta:
                            print(linea, end="")
                    elif not mostrar_procedimiento:
                        print("\nDe acuerdo!")
                    else:
                        print("\nOpción inválida!")

                    resolver_otra = self._match_input("¿Desea resolver otra matriz? (s/n) ")
                    if resolver_otra:
                        continue
                    elif not resolver_otra:
                        input("De acuerdo! Regresando al menú de matrices...")
                    else:
                        input("Opción inválida! Regresando al menú de matrices...")

                    option = self.menu_matrices()
                    continue
                case 3:  # sumar matrices
                    mats_seleccionadas, resultado = self.procesar_operacion("s")
                    mat1, mat2 = self.mats_ingresadas[mats_seleccionadas[0]], self.mats_ingresadas[mats_seleccionadas[1]]
                    
                    limpiar_pantalla()
                    print(f"\n{mats_seleccionadas[0]}:")
                    for linea in mat1.get_mat_str():
                        print(linea, end="")
                    
                    print(f"\n{mats_seleccionadas[1]}:")
                    for linea in mat2.get_mat_str():
                        print(linea, end="")

                    print(f"\n{mats_seleccionadas[0]} + {mats_seleccionadas[1]}:")
                    for linea in resultado.get_mat_str():
                        print(linea, end="")

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_matrices()
                    continue
                case 4:  # restar matrices
                    mats_seleccionadas, resultado = self.procesar_operacion("r")
                    mat1, mat2 = self.mats_ingresadas[mats_seleccionadas[0]], self.mats_ingresadas[mats_seleccionadas[1]]
                    
                    limpiar_pantalla()
                    print(f"\n{mats_seleccionadas[0]}:")
                    for linea in mat1.get_mat_str():
                        print(linea, end="")
                    
                    print(f"\n{mats_seleccionadas[1]}:")
                    for linea in mat2.get_mat_str():
                        print(linea, end="")

                    print(f"\n{mats_seleccionadas[0]} - {mats_seleccionadas[1]}:")
                    for linea in resultado.get_mat_str():
                        print(linea, end="")

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_matrices()
                    continue
                case 5:  # multiplicar matrices
                    mats_seleccionadas, resultado = self.procesar_operacion("m")
                    mat1, mat2 = self.mats_ingresadas[mats_seleccionadas[0]], self.mats_ingresadas[mats_seleccionadas[1]]
                    
                    limpiar_pantalla()
                    print(f"\n{mats_seleccionadas[0]}:")
                    for linea in mat1.get_mat_str():
                        print(linea, end="")
                    
                    print(f"\n{mats_seleccionadas[1]}:")
                    for linea in mat2.get_mat_str():
                        print(linea, end="")

                    print(f"\n{mats_seleccionadas[0]} * {mats_seleccionadas[1]}:")
                    for linea in resultado.get_mat_str():
                        print(linea, end="")

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_matrices()
                    continue
                case 6:  # transponer matriz
                    mat_seleccionada, resultado = self.procesar_operacion("t")
                    mat_original = self.mats_ingresadas[mat_seleccionada]
                    
                    limpiar_pantalla()
                    print(f"\n{mat_seleccionada}:")
                    for linea in mat_original.get_mat_str():
                        print(linea, end="")

                    print(f"\n{mat_seleccionada}_t:")
                    for linea in resultado.get_mat_str():
                        print(linea, end="")

                    input("\nPresione cualquier tecla para continuar...")
                    option = self.menu_matrices()
                    continue
                case 7:
                    input("Regresando al menú principal...")
                    break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue
        return None

    def menu_matrices(self) -> int:
        limpiar_pantalla()
        print("\n###############################")
        print("### Operaciones Matriciales ###")
        print("###############################")
        self._imprimir_matrices()
        print("\n1. Agregar una matriz")
        print("2. Resolver sistema de ecuaciones")
        print("3. Suma de matrices")
        print("4. Resta de matrices")
        print("5. Multiplicación de matrices")
        print("6. Transposición de una matriz")
        print("7. Regresar al menú principal")

        try:
            option = int(input("\nSeleccione una opción: ").strip())
            if option < 1 or option > 7:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_matrices()

        return option

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

        self.mats_ingresadas[nombre] = self.pedir_matriz(nombre, es_aumentada)
        print("\nMatriz agregada exitosamente!")

        match input("¿Desea agregar otra matriz? (s/n) ").strip().lower():
            case "s":
                return self.agregar_matriz()
            case "n":
                input("Regresando al menú de matrices...")
            case _:
                input("Opción inválida! Regresando al menú de matrices...")

        return None

    def pedir_matriz(self, nombre="M", es_aumentada=True) -> Matriz:
        valores = []
        filas, columnas = self.pedir_dimensiones(nombre, es_aumentada)

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
                        dato_a_pedir = f"-> X{columna_actual+1} = "
                    else:
                        dato_a_pedir = "-> b = "
                    elemento = Fraction(input(dato_a_pedir).strip()).limit_denominator(100)
                    fila.append(elemento)
                    columna_actual += 1

                except ValueError:
                    input("\nError: Ingrese un número real!")
                    print()
                except ZeroDivisionError:
                    input("\nError: El denominador no puede ser cero!")
                    print()

            fila_actual += 1
            valores.append(fila)

        mat = Matriz(es_aumentada, filas, columnas, valores)
        return mat

    def pedir_dimensiones(self, nombre: str, es_aumentada: bool) -> Tuple[int, int]:
            palabras = ["ecuaciones", "variables"] if es_aumentada else ["filas", "columnas"]

            try:
                print(f"\nDatos de matriz {nombre}:")
                print("----------------------------")
                filas = int(input(f"Ingrese el número de {palabras[0]}: "))
                if filas <= 0:
                    raise ValueError("Error: Ingrese un número entero positivo!")
                columnas = int(input(f"Ingrese el número de {palabras[1]}: "))
                if columnas <= 0:
                    raise ValueError("Error: Ingrese un número entero positivo!")

            except ValueError as v:
                input(v)
                return self.pedir_dimensiones(nombre, es_aumentada)
            return (filas, columnas)

    # TODO: mejorar esta mierda
    def procesar_operacion(self, operacion: str):
        """
        "m": multiplicar matrices
        "s": sumar matrices
        "r": restar matrices
        "t": transponer matriz
        "se": resolver sistema de ecuaciones
        """

        if operacion not in ("m", "s", "r", "t", "se"):
            return None

        if operacion == "m" or operacion == "s" or operacion == "r":
            nombres_mats = self.seleccionar(None)
            mat1, mat2 = self.mats_ingresadas[nombres_mats[0]], self.mats_ingresadas[nombres_mats[1]]
            match operacion:
                case "m":
                    mat_resultante = mat1.mult_matrices(mat2)
                case "s":
                    mat_resultante = mat1.sumar_mats(mat2)
                case "r":
                    mat_resultante = mat1.restar_mats(mat2)
            return (nombres_mats, mat_resultante)

        elif operacion == "t" or operacion == "se":
            nombre_mat = self.seleccionar(operacion)
            mat_copia = deepcopy(self.mats_ingresadas[nombre_mat])
            match operacion:
                case "t":
                    nombre_mat_modded = f"{nombre_mat}_t"
                    mat_copia_modded = mat_copia.transponer()

                    if nombre_mat_modded not in self.mats_ingresadas.keys():
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded
                    return (nombre_mat, mat_copia_modded)
                case "se":
                    nombre_mat_modded = f"{nombre_mat}_r"
                    resolver = SistemaEcuaciones(mat_copia)
                    resolver.resolver_sistema()
                    respuesta = resolver.respuesta
                    procedimiento = resolver.procedimiento
                    mat_copia_modded = resolver.matriz

                    if nombre_mat_modded not in self.mats_ingresadas.keys():
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded
                    return (respuesta, procedimiento, mat_copia_modded)

    @overload
    def seleccionar(self, operacion: str) -> str: ...

    @overload
    def seleccionar(self, operacion: None) -> List[str]: ...

    def seleccionar(self, operacion: str | None) -> str | List[str]:
        if operacion not in ("t", "se", None):
            return "" if operacion else []

        if not self._validar_mats_ingresadas():
            return "" if operacion else []

        if operacion:
            mensaje = self._get_mensaje(operacion)
            input_mat = self._get_input(mensaje)
            try:
                self._validate_input_mat(input_mat, operacion)
            except (KeyError, TypeError) as e:
                input(e)
                return self.seleccionar(operacion)
            return input_mat

        else:
            mensaje = "\n¿Cuáles matrices desea seleccionar? (separadas por comas) "
            input_mats = self._get_input(mensaje).split(",")
            try:
                self._validate_input_mats(input_mats)
            except (KeyError, ArithmeticError) as e:
                input(e)
                return self.seleccionar(None)
            return input_mats

    def _get_mensaje(self, operacion: str) -> str:
        match operacion:
            case "se":
                return "\n¿Cuál matriz desea resolver? "
            case "t":
                return "\n¿Cuál matriz desea transponer? "
            case _:
                return ""

    def _get_input(self, mensaje: str) -> str:
        limpiar_pantalla()
        self._imprimir_matrices()
        return input(mensaje).strip()

    def _validate_input_mat(self, input_mat: str, operacion: str) -> None:
        if input_mat not in self.mats_ingresadas:
            raise KeyError(f"Error: La matriz {input_mat} no existe!")
        elif operacion == "se" and not self.mats_ingresadas[input_mat][1]:
            raise TypeError("Error: La matriz seleccionada no es aumentada!")

    def _validate_input_mats(self, input_mats: List[str]) -> None:
        mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)
        if mat is not None:
            raise KeyError(f"Error: La matriz {mat} no existe!")
        elif len(input_mats) != 2:
            raise ArithmeticError("Error: Debe seleccionar dos matrices!")

    def _validar_mats_ingresadas(self) -> bool:
        if self.mats_ingresadas == {}:
            input("\nNo hay matrices ingresadas!")
            return False
        return True

    def _imprimir_matrices(self) -> None:
        if not self._validar_mats_ingresadas():
            return None

        print("\nMatrices guardadas:")
        print("---------------------------------------------", end="")
        for nombre, mat in self.mats_ingresadas.items():
            print(f"\n{nombre}:")
            for linea in mat.get_mat_str():
                print(linea, end="")
        print("---------------------------------------------")

        return None
    
    @staticmethod
    def _match_input(pregunta: str) -> int:
        opciones = ("s", "n")
        input_usuario = input(pregunta).strip().lower()
        if input_usuario not in opciones:
            return -1
        return 1 if input_usuario == "s" else 0
