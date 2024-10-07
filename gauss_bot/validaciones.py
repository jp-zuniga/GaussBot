from typing import List

from utils import Mat, DictMatrices, DictVectores, Validacion


def validar_vecs(vecs_ingresados: DictVectores) -> bool:
    if not vecs_ingresados:
        input("\nNo hay vectores ingresados!")
        return False
    return True


def validar_mats(mats_ingresadas: DictMatrices) -> bool:
    if not mats_ingresadas:
        input("\nNo hay matrices ingresadas!")
        return False
    return True


def validar_matriz(M: Mat) -> int:
    consistente = validar_consistencia(M)
    if not consistente[0]:
        return consistente[1]
    else:
        return -1


def validar_consistencia(M: Mat) -> Validacion:
    filas = len(M)
    for i in range(filas):
        # validar forma de 0 = b (donde b != 0)
        if [0 for _ in range(len(M[0]) - 1)] == M[i][:-1] and M[i][-1] != 0:
            return (False, i)

    return (True, -1)


def validar_escalonada(M: Mat) -> bool:
    filas = len(M)
    columnas = len(M[0])
    fila_cero = [0 for _ in range(columnas)]
    matriz_cero = [[0 for _ in range(columnas)] for _ in range(filas)]
    entrada_anterior = -1

    if M == matriz_cero:
        return False

    # buscar filas no-cero despues de una fila cero, significa que no es escalonada
    for i in range(filas):
        if M[i] != fila_cero:
            continue
        if any(M[j] != fila_cero for j in range(i + 1, filas)):
            return False

    # validar entradas principales
    for i in range(filas):
        try:
            entrada_actual = next(j for j in range(columnas - 1) if M[i][j] != 0)
        except StopIteration:
            continue
        if entrada_actual <= entrada_anterior:
            return False
        if any(M[k][entrada_actual] != 0 for k in range(i + 1, filas)):
            return False

        entrada_anterior = entrada_actual

    return True


def validar_escalonada_reducida(M: Mat) -> bool:
    filas = len(M)
    columnas = len(M[0])

    if not validar_escalonada(M):  # si no es escalonada, no puede ser escalonada reducida
        return False

    # validar entradas principales
    for i in range(filas):
        try:
            entrada_principal = next(j for j in range(columnas - 1) if M[i][j] == 1)
        except StopIteration:
            continue
        if any(M[k][entrada_principal] != 0 and k != i for k in range(filas)):
            return False

    return True


def encontrar_variables_libres(M: Mat) -> List[int]:
    filas = len(M)
    columnas = len(M[0])
    entradas = []

    # encontrar entradas principales
    for i in range(filas):
        try:
            entradas.append(next(j for j in range(columnas - 1) if M[i][j] != 0))
        except StopIteration:
            continue

    # si no son entradas principales, son variables libres
    return [x for x in range(columnas - 1) if x not in entradas]
