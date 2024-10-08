from fractions import Fraction
from typing import List

from validaciones import validar_vecs
from utils import Vec, DictVectores, limpiar_pantalla


class Vector:
    def __init__(self, componentes: List[Fraction]) -> None:
        self.componentes = componentes

    def __len__(self) -> int:
        return len(self.componentes)

    def __getitem__(self, indice: int) -> Fraction:
        return self.componentes[indice]

    def __setitem__(self, indice: int, value: Fraction) -> None:
        self.componentes[indice] = value

    def __str__(self) -> str:
        return f"[{', '.join(str(c) for c in self.componentes)}]"

    def __add__(self, vec2: 'Vector') -> 'Vector':
        if len(self) != len(vec2):
            raise ValueError("Vectors must be of the same length")
        return Vector([a + b for a, b in zip(self.componentes, vec2.componentes)])

    def __sub__(self, vec2: 'Vector') -> 'Vector':
        if len(self) != len(vec2):
            raise ValueError("Vectors must be of the same length")
        return Vector([a - b for a, b in zip(self.componentes, vec2.componentes)])

    def mult_escalar(self, escalar: Fraction) -> 'Vector':
        return Vector([escalar * c for c in self.componentes])

    def prod_punto(self, vec2: 'Vector') -> Fraction:
        if len(self) != len(vec2):
            raise ValueError("Vectors must be of the same length")
        return Fraction(sum(a * b for a, b in zip(self.componentes, vec2.componentes)))


class OperacionesVectores:
    def __init__(self, default_vecs: DictVectores = {}) -> None:
        self.vecs_ingresados = default_vecs


    def imprimir_vectores(self, es_matricial=False) -> None:
        if not validar_vecs(self.vecs_ingresados):
            return None

        mensaje = "seleccionados" if es_matricial else "ingresados"
        print(f"\nVectores {mensaje}:")
        print("---------------------------------------------")
        for nombre, vector in self.vecs_ingresados.items():
            vec = [str(num.limit_denominator(100)) for num in vector]
            print(f"{nombre}: {vec}")
        print("---------------------------------------------")

        return None


    def menu_vectores(self) -> int:
        limpiar_pantalla()
        print("\n###############################")
        print("### Operaciones Vectoriales ###")
        print("###############################")
        self.imprimir_vectores()
        print("\n1. Agregar un vector")
        print("2. Suma y resta de vectores")
        print("3. Multiplicación escalar")
        print("4. Producto punto")
        print("5. Producto matriz-vector")
        print("6. Regresar al menú principal")

        try:
            option = int(input("\nSeleccione una opción: "))
            if option < 1 or option > 6:
                raise ValueError
        except ValueError:
            input("\nError: Ingrese una opción válida!")
            return self.menu_vectores()

        return option


    def main_vectores(self) -> None:
        option = self.menu_vectores()
        while option != 7:
            match option:
                case 1:
                    limpiar_pantalla()
                    self.agregar_vector()
                    option = self.menu_vectores()
                    continue
                case 2:
                    limpiar_pantalla()
                    self.suma_resta_vectores()
                    option = self.menu_vectores()
                    continue
                case 3:
                    limpiar_pantalla()
                    self.mult_escalar()
                    option = self.menu_vectores()
                    continue
                case 4:
                    limpiar_pantalla()
                    self.mult_vectorial()
                    option = self.menu_vectores()
                    continue
                case 5:
                    limpiar_pantalla()
                    self.mult_matriz_vector()
                    option = self.menu_vectores()
                    continue
                case 6:
                    input("Regresando al menú principal...")
                    break
                case _:
                    input("Opción inválida! Por favor, intente de nuevo...")
                    continue

        return None


    def agregar_vector(self) -> None:
        try:
            limpiar_pantalla()
            nombre = input("\nIngrese el nombre del vector (una letra minúscula): ").strip().lower()
            if not nombre.isalpha() or len(nombre) != 1:
                raise NameError("Error: Ingrese solamente una letra minúscula!")
            if nombre in self.vecs_ingresados:
                raise KeyError(f"Error: Ya hay un vector con el nombre {nombre}!")

            longitud = int(input("¿Cuántas dimensiones tendrá el vector? ").strip())

        except NameError as n:
            input(n)
            return self.agregar_vector()
        except KeyError as k:
            input(k)
            return self.agregar_vector()
        except ValueError:
            input("Error: Ingrese un número entero!")
            return self.agregar_vector()

        self.vecs_ingresados[nombre] = self.ingresar_vector(longitud)
        print("\nVector agregado exitosamente!")

        match input("¿Desea agregar otro vector? (s/n) ").strip().lower():
            case "s":
                return self.agregar_vector()
            case "n":
                input("Regresando al menú de vectores...")
            case _:
                input("Opción inválida! Regresando al menú de vectores...")

        return None


    def ingresar_vector(self, longitud: int) -> Vec:
        try:
            vec = [
                Fraction(x).limit_denominator(100)
                for x in input("Ingrese los componentes (separados por comas): ")
                .strip()
                .split(",")
            ]

            if len(vec) != longitud:
                raise TypeError("Error: El vector no tiene las dimensiones correctas!")

        except TypeError as t:
            input(t)
            return self.ingresar_vector(longitud)
        except ValueError:
            input("Error: Ingrese un número real!")
            return self.ingresar_vector(longitud)

        return vec


    def seleccionar_vector(self, operacion: str) -> str:
        if operacion not in ("e", "mv"):
            return ""
        if not validar_vecs(self.vecs_ingresados):
            return ""

        match operacion:
            case "e":
                mensaje = "multiplicar escalarmente"
            case "mv":
                mensaje = "multiplicar por la matriz"

        mensaje = f"\n¿Cuál vector desea {mensaje}? "
        try:
            limpiar_pantalla()
            self.imprimir_vectores()
            input_vec = input(mensaje).strip()
            if input_vec not in self.vecs_ingresados:
                raise KeyError(f"Error: El vector '{input_vec}' no existe!")

        except KeyError as k:
            input(k)
            return self.seleccionar_vector(operacion)

        return input_vec


    def seleccionar_vectores(self) -> List[str]:
        if not validar_vecs(self.vecs_ingresados):
            return []

        mensaje = "\n¿Cuáles vectores desea seleccionar? (separados por comas)"
        try:
            limpiar_pantalla()
            self.imprimir_vectores()
            input_vecs = input(mensaje).strip().split(",")
            vec_existe = next((vec for vec in input_vecs if vec not in self.vecs_ingresados), None)

            if vec_existe is not None:
                raise KeyError(f"Error: El vector '{vec_existe}' no existe!")
            if len(input_vecs) != 2:
                raise ValueError("Error: Solamente debe ingresar dos vectores!")

        except KeyError as k:
            input(k)
            return self.seleccionar_vectores()
        except ValueError as v:
            input(v)
            return self.seleccionar_vectores()

        return input_vecs


    def mult_escalar(self) -> None:
        if not validar_vecs(self.vecs_ingresados):
            return None

        vec_nombre = self.seleccionar_vector("e")
        try:
            escalar = Fraction(input("Ingrese el escalar: ").strip())
        except ValueError:
            input("Error: Ingrese un número real!")
            return self.mult_escalar()
        except ZeroDivisionError:
            input("Error: El denominador no puede ser cero!")
            return self.mult_escalar()

        self.vecs_ingresados[vec_nombre] = [
            x * escalar for x in self.vecs_ingresados[vec_nombre]
        ]

        imprimir_escalar = (
            escalar if escalar.is_integer() else f"({str(Fraction(escalar).limit_denominator(100))}) * "
        )

        input(
            f"\n{imprimir_escalar}{vec_nombre} = " +
            f"{[str(x.limit_denominator(100)) for x in self.vecs_ingresados[vec_nombre]]}"
        )

        return None


    def mult_vectorial(self) -> None:
        if not validar_vecs(self.vecs_ingresados):
            return None

        vec1, vec2 = self.seleccionar_vectores()
        if len(self.vecs_ingresados[vec1]) != len(self.vecs_ingresados[vec2]):
            input("Error: Los vectores deben tener la misma longitud!")
            return self.mult_vectorial()

        producto_punto = sum(
            i * j
            for i in self.vecs_ingresados[vec1]
            for j in self.vecs_ingresados[vec2]
        )

        input(f"\n{vec1}.{vec2} = {str(producto_punto)}")
        return None


    def suma_resta_vectores(self) -> Vec:
        if not validar_vecs(self.vecs_ingresados):
            return []

        vec1, vec2 = self.seleccionar_vectores()
        if len(self.vecs_ingresados[vec1]) != len(self.vecs_ingresados[vec2]):
            input("Error: Los vectores deben tener la misma longitud!")
            return self.suma_resta_vectores()

        operacion = input("\n¿Desea sumar o restar los vectores? (+/-) ").strip()
        if operacion not in ("+", "-"):
            input("Error: Ingrese un operador válido!")
            return self.suma_resta_vectores()

        if operacion == "+":
            resultado = [
                self.vecs_ingresados[vec1][x] + self.vecs_ingresados[vec2][x]
                for x in range(len(self.vecs_ingresados[vec1]))
            ]
        elif operacion == "-":
            resultado = [
                self.vecs_ingresados[vec1][x] - self.vecs_ingresados[vec2][x]
                for x in range(len(self.vecs_ingresados[vec1]))
            ]

        input(f"\n{vec1} {operacion} {vec2} = {[str(x.limit_denominator(100)) for x in resultado]}")
        return resultado


    def mult_matriz_vector(self) -> None:
        from matrices import OperacionesMatrices
        mat = OperacionesMatrices()

        if not validar_vecs(self.vecs_ingresados):
            return None

        limpiar_pantalla()
        A = mat.pedir_matriz(es_aumentada=False, nombre="A")
        nombre_x = self.seleccionar_vector("mv")
        x = self.vecs_ingresados[nombre_x]

        if len(A[0]) != len(x):  # validar las dimensiones
            input(f"\nError: Las dimensiones de A y {nombre_x} no son compatibles!")
            return None

        # calcular Ax
        resultado = [[Fraction(0) for _ in range(len(x))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(x)):
                resultado[i][j] += A[i][j] * x[j]

        print("\nA:")
        mat.imprimir_matriz(A, es_aumentada=False)
        print(f"\n{nombre_x} = {[str(num.limit_denominator(100)) for num in x]}")
        print(f"\nA{nombre_x}:")
        mat.imprimir_matriz(resultado, es_aumentada=False)

        input("\nPresione cualquier tecla para continuar...")
        return None
