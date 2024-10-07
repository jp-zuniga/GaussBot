from fractions import Fraction

from utils import List, Mat, Validacion
from validaciones import (
    validar_matriz,
    validar_escalonada_reducida,
    encontrar_variables_libres,
)


def resolver_sistema(M: Mat) -> Mat | None:
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


def reducir_matriz(M: Mat) -> Mat:
    test_inicial = validar_matriz(M)
    if test_inicial != -1:
        imprimir_soluciones(M, unica=False, libres=[], validacion=(False, test_inicial))
        return []
    elif validar_escalonada_reducida(M):
        print("\nMatriz ya esta en su forma escalonada reducida!")
        return M

    from matrices import Matriz  # para Matriz.imprimir_matriz()
    mat = Matriz()
    filas = len(M)
    columnas = len(M[0])

    print("\nMatriz inicial:")
    mat.imprimir_matriz(M)
    print("\nReduciendo la matriz a su forma escalonada:")

    fila_actual = 0
    for j in range(columnas - 1):  # encontrar pivotes y eliminar elementos debajo
        fila_pivote = None
        maximo = Fraction(0)

        # buscar la entrada con el valor mas grande para usarla como pivote
        for i in range(fila_actual, filas):
            if abs(M[i][j]) > maximo:
                maximo = abs(M[i][j])
                fila_pivote = i

        # si las variables siguen iguales, no hay pivote y se pasa a la siguiente columna
        if fila_pivote is None or maximo == 0:
            continue

        # siempre trabajar con la fila pivote
        if fila_pivote != fila_actual:
            M[fila_actual], M[fila_pivote] = M[fila_pivote], M[fila_actual]
            print(f"\nF{fila_actual+1} <==> F{fila_pivote+1}")
            mat.imprimir_matriz(M)

        pivote = M[fila_actual][j]
        if pivote != 1 and pivote != 0:  # hacer el pivote igual a 1
            for k in range(columnas):
                M[fila_actual][k] /= pivote
            if pivote == -1:
                print(f"\nF{fila_actual+1} => -F{fila_actual+1}")
            else:
                print(f"\nF{fila_actual+1} => F{fila_actual+1} / {str(pivote.limit_denominator(100))}")

            mat.imprimir_matriz(M)

        # eliminar los elementos debajo del pivote
        for f in range(fila_actual + 1, filas):
            factor = M[f][j]
            if factor == 0:
                continue
            for k in range(columnas):
                M[f][k] -= factor * M[fila_actual][k]

            print(f"\nF{fila_actual+1} => F{fila_actual+1} - ({str(factor.limit_denominator(100))} * F{fila_pivote+1})")
            mat.imprimir_matriz(M)

        fila_actual += 1

    for i in reversed(range(filas)):  # eliminar elementos arriba de pivotes
        try:
            columna_pivote = M[i].index(next(filter(lambda x: x != 0, M[i])))
        except StopIteration:
            columna_pivote = None
        if columna_pivote is None:  # no hay entrada principal
            continue

        # eliminar los elementos encima del pivote
        for f in reversed(range(i)):
            factor = M[f][columna_pivote]
            if factor == 0:
                continue
            for k in range(columnas):
                M[f][k] -= factor * M[i][k]

            print(f"\nF{f+1} => F{f+1} - ({str(factor.limit_denominator(100))} * F{i+1})")
            mat.imprimir_matriz(M)

    test_final = validar_matriz(M)
    if test_final != -1:
        imprimir_soluciones(M, unica=False, libres=[], validacion=(False, test_inicial))
        return []
    return M


def despejar_variables(M: Mat, libres: List[int]) -> List[str]:
    filas = len(M)
    columnas = len(M[0])
    ecuaciones = []
    for x in libres:
        ecuaciones.append(f"| X{x+1} es libre")

    for i in range(filas):
        for j in range(columnas - 1):
            if M[i][j] == 0:
                continue

            constante = M[i][-1].limit_denominator(100)
            expresion = str(constante) if constante != 0 else ""
            for k in range(j + 1, columnas - 1):
                if M[i][k] == 0:
                    continue

                coeficiente = -M[i][k].limit_denominator(100)
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

            if not expresion:
                expresion = "0"

            ecuaciones.append(f"| X{j+1} = {expresion}")
            break

    ecuaciones.sort(key=lambda x: x[3])
    return ecuaciones


def imprimir_soluciones(M: Mat, unica: bool,libres: List[int], validacion: Validacion) -> None:
    filas = len(M)
    solucion, fila_inconsistente = validacion
    if not solucion and fila_inconsistente != -1:
        print(f"\n| En F{fila_inconsistente+1}: 0 != {str(M[fila_inconsistente][-1].limit_denominator(100))}")
        input("| Sistema es inconsistente!")
        return None

    elif unica:
        solucion_trivial = all(M[i][-1] == 0 for i in range(filas))
        mensaje_solucion = "trivial" if solucion_trivial else "no trivial"

        print(f"\n| Solución {mensaje_solucion} encontrada:")
        for i in range(filas):
            if all(x == 0 for x in M[i]):
                continue
            print(f"| X{i+1} = {str(M[i][-1].limit_denominator(100))}")
        return None

    # solucion general:
    ecuaciones = despejar_variables(M, libres)
    print("\n| Sistema no tiene solución única!")
    print("| Solución general encontrada:")
    for linea in ecuaciones:
        print(linea)

    return None
