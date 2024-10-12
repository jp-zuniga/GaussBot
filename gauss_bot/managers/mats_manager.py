from copy import deepcopy
from fractions import Fraction

from gauss_bot.clases.matriz import Matriz
from gauss_bot.clases.sistema_ecuaciones import SistemaEcuaciones
from gauss_bot.utils import limpiar_pantalla, match_input


class MatricesManager:
    def __init__(self, parent=None, mats_ingresadas: dict[str, Matriz] = {}) -> None:
        self.parent = parent
        self.mats_ingresadas = mats_ingresadas

    def menu_matrices(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n###############################")
            print("### Operaciones de Matrices ###")
            print("###############################")
            print("\n1. Agregar una matriz")
            print("2. Mostrar matrices\n")
            print("3. Resolver sistema de ecuaciones")
            print("4. Sumar matrices")
            print("5. Restar matrices")
            print("6. Multiplicar matriz por escalar")
            print("7. Multiplicar matrices")
            print("8. Multiplicar matriz por vector")
            print("9. Transponer matriz")
            print("10. Calcular determinante de una matriz\n")
            print("11. Regresar al menú principal")
            try:
                option = int(input("\n=> Seleccione una opción: ").strip())
                if option < 1 or option > 11:
                    raise ValueError
            except ValueError:
                input("=> Error: Ingrese una opción válida!")
                continue
            if option == 11:
                input("=> Regresando a menú principal...")
                break
            self.procesar_menu(option)
        return None

    def procesar_menu(self, opcion: int) -> None:
        match opcion:
            case 1:
                self.agregar_matriz()
                return None
            case 2:
                self._mostrar_matrices(necesita_aumentada=-1)
            case 3:
                resultado = self.procesar_operacion("se")
                if resultado is not None:
                    self.mostrar_resultado("se", resultado)
                    return None
            case 4:
                resultado = self.procesar_operacion("s")
                if resultado is not None:
                    self.mostrar_resultado("s", resultado)
                    return None
            case 5:
                resultado = self.procesar_operacion("r")
                if resultado is not None:
                    self.mostrar_resultado("r", resultado)
                    return None
            case 6:
                resultado = self.procesar_operacion("me")
                if resultado is not None:
                    self.mostrar_resultado("me", resultado)
                    return None
            case 7:
                resultado = self.procesar_operacion("m")
                if resultado is not None:
                    self.mostrar_resultado("m", resultado)
                    return None
            case 8:
                self.parent.producto_matriz_vector()
            case 9:
                resultado = self.procesar_operacion("t")
                if resultado is not None:
                    self.mostrar_resultado("t", resultado)
                    return None
            case 10:
                resultado = self.procesar_operacion("d")
                if resultado is not None:
                    self.mostrar_resultado("d", resultado)
                    return None
        input("Presione cualquier tecla para regresar al menú de matrices...")
        return None

    def agregar_matriz(self) -> None:
        try:
            limpiar_pantalla()
            nombre = (
                input("\nIngrese el nombre de la matriz (una letra mayúscula): ")
                .strip()
                .upper()
            )

            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError
            if nombre in self.mats_ingresadas:
                raise KeyError

            ingresar_aumentada = match_input(
                "¿Se ingresará una matriz aumentada? (s/n) "
            )

            if ingresar_aumentada == 1:
                es_aumentada = True
            elif ingresar_aumentada == 0:
                es_aumentada = False
            else:
                raise ValueError

        except NameError:
            input("Error: Ingrese solamente una letra mayúscula!")
            return self.agregar_matriz()
        except KeyError:
            input(f"Error: Ya hay una matriz con el nombre '{nombre}'!")
            return self.agregar_matriz()
        except ValueError:
            input("Error: Ingrese una opción válida!")
            return self.agregar_matriz()

        self.mats_ingresadas[nombre] = self.pedir_matriz(nombre, es_aumentada)
        print("\nMatriz agregada exitosamente!")
        ingresar_otra = match_input("¿Desea ingresar otra matriz? (s/n) ")
        if ingresar_otra == 1:
            return self.agregar_matriz()
        elif ingresar_otra == 0:
            input("\nPresione cualquier tecla para regresar al menú de matrices...")
        else:
            input("\nOpción inválida!\nPresione cualquier tecla para regresar al menú de matrices...")
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

    def pedir_dimensiones(self, nombre: str, es_aumentada: bool) -> tuple[int, int]:
        palabras = ["ecuaciones", "variables"] if es_aumentada else ["filas", "columnas"]
        try:
            limpiar_pantalla()
            print(f"\nDatos de matriz {nombre}:")
            print("----------------------------")
            filas = int(input(f"Ingrese el número de {palabras[0]}: "))
            if filas <= 0:
                raise ValueError
            columnas = int(input(f"Ingrese el número de {palabras[1]}: "))
            if columnas <= 0:
                raise ValueError
        except ValueError:
            input("Error: Ingrese un número entero positivo!")
            return self.pedir_dimensiones(nombre, es_aumentada)
        return (filas, columnas)

    def procesar_operacion(self, operacion: str) -> tuple:
        """
        * toma un codigo de operacion
        * selecciona las matrices necesarias
        * retorna una tupla con lo que selecciono el usuario y los resultados de la operacion

        codigos validos de operacion:
        * "se": resolver sistema de ecuaciones
        * "s": sumar matrices
        * "r": restar matrices
        * "me": multiplicar matriz por escalar
        * "m": multiplicar matrices
        * "t": transponer matriz
        * "d": calcular determinante
        """

        limpiar_pantalla()
        if operacion not in ("se", "s", "r", "me", "m", "t", "d") or not self._validar_mats_ingresadas():
            return ()

        if operacion in ("s", "r", "m"):
            nombres_mats = self.seleccionar_mats(operacion)
            if nombres_mats == []:
                return ()

            mat1, mat2 = (
                self.mats_ingresadas[nombres_mats[0]],
                self.mats_ingresadas[nombres_mats[1]],
            )

            match operacion:
                case "s":
                    return (nombres_mats, mat1 + mat2)
                case "r":
                    return (nombres_mats, mat1 - mat2)
                case "m":
                    return (nombres_mats, mat1 * mat2)

        elif operacion in ("se", "me", "t", "d"):
            nombre_mat = self.seleccionar_mat(operacion)
            if nombre_mat == "":
                return ()

            mat_copia = deepcopy(self.mats_ingresadas[nombre_mat])
            match operacion:
                case "se":
                    nombre_mat_modded = f"{nombre_mat}_r"
                    sistema = SistemaEcuaciones(mat_copia)
                    sistema.resolver_sistema()

                    respuesta = sistema.respuesta
                    procedimiento = sistema.procedimiento
                    mat_copia_modded = sistema.matriz
                    if not any(mat_copia_modded == mat for mat in self.mats_ingresadas.values()):
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded

                    return (nombre_mat, respuesta, procedimiento, mat_copia_modded)
                case "me":
                    try:
                        escalar = Fraction(
                            input("Ingrese el escalar: ").strip()
                        ).limit_denominator(100)
                    except ValueError:
                        input("Error: Ingrese un número real!")
                        return ()
                    except ZeroDivisionError:
                        input("Error: El denominador no puede ser cero!")
                        return ()
                    return (nombre_mat, escalar, mat_copia * escalar)
                case "t":
                    nombre_mat_modded = f"{nombre_mat}_t"
                    mat_copia_modded = mat_copia.transponer()
                    if not any(mat_copia_modded == mat for mat in self.mats_ingresadas.values()):
                        self.mats_ingresadas[nombre_mat_modded] = mat_copia_modded

                    return (nombre_mat, mat_copia_modded)
                case "d":
                    mat_triangular, intercambio = mat_copia.hacer_triangular_superior()
                    determinante = Fraction(1)
                    for i in range(mat_triangular.filas):
                        determinante *= mat_triangular[i, i]

                    return (nombre_mat, mat_triangular, determinante, intercambio)
        return ()

    def mostrar_resultado(self, operacion: str, resultado: tuple) -> None:
        """
        * operacion: el codigo de operacion usada en .procesar_operacion()
        * resultado: la tupla retornada por .procesar_operacion()

        codigos validos de operacion:
        * "se": resolver sistema de ecuaciones
        * "s": sumar matrices
        * "r": restar matrices
        * "me": multiplicar matriz por escalar
        * "m": multiplicar matrices
        * "t": transponer matriz
        * "d": calcular determinante
        """

        limpiar_pantalla()
        if operacion not in ("se", "s", "r", "me", "m", "t", "d") or resultado == ():
            return None

        match operacion:
            case "se":  # ? resolver sistema de ecuaciones
                mat_seleccionada, respuesta, procedimiento, mat_resuelta = resultado
                print("\nMatriz seleccionada:")
                print(self.mats_ingresadas[mat_seleccionada])
                print("---------------------------------------------")
                print("\nSistema de ecuaciones resuelto:")
                print(mat_resuelta, end="")
                print(respuesta)
                print("---------------------------------------------")

                mostrar_procedimiento = match_input(
                    "\n¿Desea ver el procedimiento? (s/n) "
                )

                if mostrar_procedimiento == 1:
                    limpiar_pantalla()
                    print(procedimiento, end="")
                    print(respuesta, end="")
                elif mostrar_procedimiento == 0:
                    print("De acuerdo!")
                else:
                    print("Opción inválida!")

                resolver_otra = match_input("\n¿Desea resolver otra matriz? (s/n) ")
                if resolver_otra == 1:
                    return self.mostrar_resultado("se", self.procesar_operacion("se"))
                elif resolver_otra == 0:
                    input("De acuerdo! Regresando al menú de matrices...")
                else:
                    input("Opción inválida! Regresando al menú de matrices...")
                return None

            case "s":   # ? sumar matrices
                mats_seleccionadas, mat_sumada = resultado
                mat1, mat2 = (
                    self.mats_ingresadas[mats_seleccionadas[0]],
                    self.mats_ingresadas[mats_seleccionadas[1]],
                )

                limpiar_pantalla()
                print("\nMatriz seleccionadas:")
                print("---------------------------------------------")
                print(f"\n{mats_seleccionadas[0]}:")
                print(mat1)
                print(f"\{mats_seleccionadas[1]}:")
                print(mat2, end="")
                print("---------------------------------------------")
                print(f"\n{mats_seleccionadas[0]} + {mats_seleccionadas[1]}:")
                print(mat_sumada, end="")

            case "r":   # ? restar matrices
                mats_seleccionadas, mat_restada = resultado
                mat1, mat2 = (
                    self.mats_ingresadas[mats_seleccionadas[0]],
                    self.mats_ingresadas[mats_seleccionadas[1]],
                )

                limpiar_pantalla()
                print("\nMatriz seleccionadas:")
                print("---------------------------------------------")
                print(f"{mats_seleccionadas[0]}:")
                print(mat1)
                print(f"\{mats_seleccionadas[1]}:")
                print(mat2, end="")
                print("---------------------------------------------")
                print(f"\n{mats_seleccionadas[0]} - {mats_seleccionadas[1]}:")
                print(mat_restada, end="")

            case "me":  # ? multiplicar matriz por escalar
                mat_seleccionada, escalar, mat_multiplicada = resultado
                mat = self.mats_ingresadas[mat_seleccionada]
                if escalar in (1, -1):
                    imprimir_escalar = ""
                elif Fraction(escalar).is_integer():
                    imprimir_escalar = str(escalar)
                else:
                    imprimir_escalar = f"({escalar}) * "

                limpiar_pantalla()
                print(f"\n{mat_seleccionada}:")
                print(mat)
                print(f"{imprimir_escalar}{mat_seleccionada}:")
                print(mat_multiplicada, end="")

            case "m":   # ? multiplicar matrices
                mats_seleccionadas, mat_multiplicada = resultado
                mat1, mat2 = (
                    self.mats_ingresadas[mats_seleccionadas[0]],
                    self.mats_ingresadas[mats_seleccionadas[1]],
                )

                limpiar_pantalla()
                print("\nMatriz seleccionadas:")
                print("---------------------------------------------")
                print(f"\n{mats_seleccionadas[0]}:")
                print(mat1)
                print(f"{mats_seleccionadas[1]}:")
                print(mat2, end="")
                print("---------------------------------------------")
                print(f"\n{mats_seleccionadas[0]} * {mats_seleccionadas[1]}:")
                print(mat_multiplicada, end="")

            case "t":   # ? transponer matriz
                mat_seleccionada, mat_transpuesta = resultado
                mat_original = self.mats_ingresadas[mat_seleccionada]

                limpiar_pantalla()
                print(f"\n{mat_seleccionada}:")
                print(mat_original)
                print(f"Transposición de {mat_seleccionada}:")
                print(mat_transpuesta, end="")

            case "d":   # ? calcular determinante
                mat_seleccionada, mat_triangular, determinante, intercambio = resultado
                mat_original = self.mats_ingresadas[mat_seleccionada]

                limpiar_pantalla()
                print("\n---------------------------------------------")
                print(f"{mat_seleccionada}:")
                print(mat_original)
                print(f"Matriz triangular superior a partir de {mat_seleccionada}:")
                print(mat_triangular, end="")
                print("---------------------------------------------\n")
                diagonales = [mat_triangular[i, i] for i in range(mat_triangular.filas)]
                print(f"| {mat_seleccionada} | = {" * ".join(str(d) for d in diagonales)}")
                print(f"| {mat_seleccionada} | = {determinante}")

                cambiar_signo = intercambio is True and determinante != 0
                if cambiar_signo:
                    print("\nComo hubo un número impar de intercambios de filas al crear la matriz triangular superior, el signo del determinante se invierte:")
                    print(f"-| {mat_seleccionada} | = {determinante}")

        input("\nPresione cualquier tecla para regresar al menú de matrices...")
        return None

    def seleccionar_mat(self, operacion: str) -> str:
        if operacion in ("se", "me", "mv", "t", "d") and self._validar_mats_ingresadas():
            mensaje = self._get_mensaje(operacion)
            input_mat = self._get_input(mensaje, operacion)
            try:
                self._validar_input_mat(input_mat, operacion)
            except (KeyError, TypeError, ArithmeticError) as e:
                print(e)
                input("Presione cualquier tecla para regresar al menú de matrices...")
                return ""
            return input_mat
        else:
            return ""

    def seleccionar_mats(self, operacion: str) -> list[str]:
        if operacion in ("s", "r", "m") and self._validar_mats_ingresadas():
            mensaje = "\n¿Cuáles matrices desea seleccionar? (separadas por comas) "
            input_mats = self._get_input(mensaje, operacion).split(",")
            try:
                self._validar_input_mats(input_mats, operacion)
            except (KeyError, ArithmeticError) as e:
                print(e)
                input("Presione cualquier tecla para regresar al menú de matrices...")
                return []
            return input_mats
        else:
            return []

    def _get_mensaje(self, operacion: str) -> str:
        match operacion:
            case "se":
                return "\n¿Cuál matriz desea resolver? "
            case "me":
                return "\n¿Cuál matriz desea multiplicar por un escalar? "
            case "mv":
                return "\n¿Cuál matriz desea multiplicar por un vector? "
            case "t":
                return "\n¿Cuál matriz desea transponer? "
            case "d":
                return "\n¿Para cuál matriz desea calcular su determinante? "
            case _:
                return ""

    def _get_input(self, mensaje: str, operacion: str) -> str:
        limpiar_pantalla()
        necesita_aumentada = operacion == "se"
        self._mostrar_matrices(necesita_aumentada)
        return input(mensaje).strip()

    def _validar_input_mat(self, input_mat: str, operacion: str) -> None:
        if input_mat not in self.mats_ingresadas:
            raise KeyError(f"Error: La matriz '{input_mat}' no existe!")
        elif operacion == "se" and not self.mats_ingresadas[input_mat].aumentada:
            raise TypeError(f"Error: La matriz '{input_mat}' no es aumentada!")
        elif operacion == "d" and not self.mats_ingresadas[input_mat].es_cuadrada():
            raise ArithmeticError(f"Error: La matriz '{input_mat}' no es cuadrada!")
        return None

    def _validar_input_mats(self, input_mats: list[str], operacion: str) -> None:
        mat = next((mat for mat in input_mats if mat not in self.mats_ingresadas), None)
        if mat is not None:
            raise KeyError(f"Error: La matriz '{mat}' no existe!")
        elif len(input_mats) != 2:
            raise ArithmeticError("Error: Debe seleccionar dos matrices!")

        elif operacion in ("s", "r"):
            mat1, mat2 = (
                self.mats_ingresadas[input_mats[0]],
                self.mats_ingresadas[input_mats[1]],
            )

            dimensiones_validas = mat1.filas == mat2.filas and mat1.columnas == mat2.columnas
            if not dimensiones_validas:
                raise ArithmeticError("Error: Las matrices deben tener las mismas dimensiones!")

        elif operacion == "m":
            mat1, mat2 = (
                self.mats_ingresadas[input_mats[0]],
                self.mats_ingresadas[input_mats[1]],
            )

            dimensiones_validas = mat1.columnas == mat2.filas
            if not dimensiones_validas:
                raise ArithmeticError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz")

        return None

    def _validar_mats_ingresadas(self) -> bool:
        if self.mats_ingresadas == {}:
            print("\nNo hay matrices ingresadas!")
            return False
        return True

    def _mostrar_matrices(self, necesita_aumentada: int) -> None:
        """
        necesita_aumentada:
        *  1: solo mostrar matrices aumentadas
        *  0: solo mostrar matrices no aumentadas
        * -1: mostrar todas las matrices ingresadas
        """

        limpiar_pantalla()
        if not self._validar_mats_ingresadas() or necesita_aumentada not in (1, 0, -1):
            return None

        solo_aumentadas = all(mat.aumentada for mat in self.mats_ingresadas.values())
        solo_no_aumentadas = all(not mat.aumentada for mat in self.mats_ingresadas.values())
        if necesita_aumentada == 1 and solo_no_aumentadas:
            print("\nNo hay matrices aumentadas ingresadas!")
            return None
        elif necesita_aumentada == 0 and solo_aumentadas:
            print("\nNo hay matrices no aumentadas ingresadas!")
            return None

        adj = "aumentadas " if necesita_aumentada == 1 else "no aumentadas "
        print(f"\nMatrices {adj if necesita_aumentada != -1 else " "}guardadas:")
        print("---------------------------------------------", end="")
        for nombre, mat in self.mats_ingresadas.items():
            if (necesita_aumentada == 1 and not mat.aumentada) or (
                necesita_aumentada == 0 and mat.aumentada):
                continue
            print(f"\n{nombre}:")
            print(mat, end="")
        print("---------------------------------------------")
        return None
