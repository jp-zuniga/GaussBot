"""
Implementación de KeyBindingManager, encargado de crear
bindings a las teclas de flecha para navegar entre entries.
"""

from typing import (
    Optional,
    Union,
)

from ..gui.custom import CustomEntry


class KeyBindingManager:
    """
    Se encarga de crear todos los bindings a las teclas de flecha
    para que se puedan navegar los entries en los módulos
    de agregar sistemas, matrices o vectores.
    """

    def __init__(
        self,
        es_matriz: bool,
        entry_list: Optional[Union[list[CustomEntry], list[list[CustomEntry]]]] = None,
        extra_entries: Optional[tuple[CustomEntry, CustomEntry]] = None,
    ) -> None:

        """
        Argumentos:
        - es_matriz: True si las entries son para una matriz,
                     False si son para un vector

        - entry_list: la lista de entries a la que se le crearán bindings
        - extra_entries: las entries adicionales que se deben tener en cuenta
                         (nombre, filas, columnas, dimensiones)

        Errores:
        - ValueError:
            - si 'entry_list' o 'extra_entries' es None a la hora de crear bindings
            - si 'entry_list' no es una lista 2D y 'es_matriz' == True
            - si 'es_matriz' == False y 'entry_list' no es una lista 1D.
        """

        self.es_matriz = es_matriz
        self.entry_list = entry_list
        self.extra_entries = extra_entries

        try:
            if self.es_matriz and not isinstance(self.entry_list[0], list):  # type: ignore
                raise ValueError(
                    "Para una matriz, 'entry_list' debe ser una lista bidimensional!"
                )

            if not self.es_matriz and isinstance(self.entry_list[0], list):  # type: ignore
                raise ValueError(
                    "Para un vector, 'entry_list' debe ser una lista unidimensional!"
                )
        except TypeError:
            pass

    def create_key_bindings(self) -> None:
        """
        Método principal para crear los bindings de teclas de flecha necesarios.
        """

        if self.entry_list is None:
            raise ValueError("'entry_list' no puede ser None!")
        if self.extra_entries is None:
            raise ValueError("'extra_entries' no puede ser None!")

        if self.es_matriz:
            for i, row in enumerate(self.entry_list):
                for j, entry in enumerate(row):  # type: ignore
                    self._bind_mat_entry(i, j, entry)
        else:
            for i, entry in enumerate(self.entry_list):
                self._bind_vec_entry(i, entry)

    def _bind_mat_entry(
        self,
        row: int,
        column: int,
        entry: CustomEntry,
    ) -> None:

        """
        Crea los bindings de teclas de flecha
        para un entry de una matriz.
        """

        nombre_entry, filas_entry = self.extra_entries  # type: ignore
        entry.bind("<Up>", lambda _: self._entry_move_up(row, column, filas_entry))
        entry.bind("<Down>", lambda _: self._entry_move_down(row, column, nombre_entry))
        entry.bind("<Left>", lambda _: self._entry_move_left(row, column))
        entry.bind("<Right>", lambda _: self._entry_move_right(row, column))
        entry.bind("<Control-Tab>", self.autocomplete_all)

    def _bind_vec_entry(
        self,
        row: int,
        entry: CustomEntry,
    ) -> None:

        """
        Crea los bindings de teclas de flecha
        para un entry de un vector.
        """

        nombre_entry, dimensiones_entry = self.extra_entries  # type: ignore
        entry.bind("<Up>", lambda _: self._entry_move_up(row, -1, dimensiones_entry))
        entry.bind("<Down>", lambda _: self._entry_move_down(row, -1, nombre_entry))
        entry.bind("<Control-Tab>", self.autocomplete_all)

    def _entry_move_up(self, row: int, column: int, data_entry: CustomEntry) -> None:
        """
        Cambia el foco a la entry por encima de la actual,
        o al entry de filas/dimensiones si ya se llegó al inicio.
        """

        if row > 0:
            if self.es_matriz:
                self.entry_list[row - 1][column].focus_set()  # type: ignore
            else:
                self.entry_list[row - 1].focus_set()  # type: ignore
        elif row == 0:
            if self.es_matriz:
                KeyBindingManager.focus_filas(data_entry)
            else:
                KeyBindingManager.focus_dimensiones(data_entry)

    def _entry_move_down(
        self,
        row: int,
        column: int,
        nombre_entry: CustomEntry,
    ) -> None:

        """
        Cambia el foco a la siguiente entry,
        o al entry de nombre si ya se llegó al final.
        """

        if row < len(self.entry_list) - 1:  # type: ignore
            if self.es_matriz:
                self.entry_list[row + 1][column].focus_set()  # type: ignore
            else:
                self.entry_list[row + 1].focus_set()  # type: ignore
        elif row == len(self.entry_list) - 1:  # type: ignore
            nombre_entry.focus_set()

    def _entry_move_left(self, row: int, column: int) -> None:
        """
        Cambia el foco a la entry a la izquierda,
        o a la fila anterior si se llegó al inicio de la fila,
        o al entry de datos iniciales si se llegó al inicio de la lista de entries.
        * row: la fila actual
        * column: la columna actual

        Solamente utilizado para los bindings de matrices.
        """

        if column > 0:
            self.entry_list[row][column - 1].focus_set()  # type: ignore
        elif column == 0:
            if row > 0:
                self.entry_list[row - 1][-1].focus_set()  # type: ignore
            elif row == 0:
                self.focus_last()

    def _entry_move_right(self, row: int, column: int) -> None:
        """
        Cambia el foco a la entry a la derecha,
        o al siguiente fila si ya se llegó al final de la fila,
        o al entry de nombre si ya se llegó al final de la lista de entries.
        * row: la fila actual
        * column: la columna actual

        Solamente utilizado para los bindings de matrices.
        """

        if column < len(self.entry_list[row]) - 1:  # type: ignore
            self.entry_list[row][column + 1].focus_set()  # type: ignore
        elif column == len(self.entry_list[row]) - 1:  # type: ignore
            if row < len(self.entry_list) - 1:  # type: ignore
                self.entry_list[row + 1][0].focus_set()  # type: ignore
            elif row == len(self.entry_list) - 1:  # type: ignore
                self.focus_first()

    def focus_first(self) -> None:
        """
        Cambia el foco a la primera entry de la lista.
        """

        try:
            if self.es_matriz:
                self.entry_list[0][0].focus_set()  # type: ignore
            else:
                self.entry_list[0].focus_set()  # type: ignore
        except IndexError:
            pass

    def focus_last(self) -> None:
        """
        Cambia el foco a la última entry de la lista.
        """

        try:
            if self.es_matriz:
                self.entry_list[-1][-1].focus_set()  # type: ignore
            else:
                self.entry_list[-1].focus_set()  # type: ignore
        except IndexError:
            pass

    def autocomplete_all(self, event) -> str:
        """
        Llama autocomplete_placeholder() para todos los entries.
        """

        del event
        if self.es_matriz:
            for row in self.entry_list:  # type: ignore
                for entry in row:  # type: ignore
                    entry.autocomplete_placeholder(event=None)  # type: ignore
        else:
            for entry in self.entry_list:  # type: ignore
                entry.autocomplete_placeholder(event=None)  # type: ignore
        return "break"

    @staticmethod
    def focus_dimensiones(dimensiones_entry: CustomEntry) -> None:
        """
        Cambia el foco al entry de ingresar dimensiones.
        """

        dimensiones_entry.focus_set()

    @staticmethod
    def focus_filas(filas_entry: CustomEntry) -> None:
        """
        Cambia el foco al entry de ingresar filas.
        """

        filas_entry.focus_set()

    @staticmethod
    def focus_columnas(columnas_entry: CustomEntry) -> None:
        """
        Cambia el foco al entry de ingresar columnas.
        """

        columnas_entry.focus_set()
