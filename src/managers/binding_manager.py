"""
Implementación de KeyBindingManager, encargado de crear
bindings a las teclas de flecha para navegar entre entries.
"""

from tkinter import Event

from src.gui.custom import CustomEntry


class KeyBindingManager:
    """
    Manager de bindings para los CustomEntry's de la aplicación.
    """

    def __init__(
        self,
        es_matriz: bool,
        entry_list: list[CustomEntry] | list[list[CustomEntry]] | None = None,
        extra_entries: tuple[CustomEntry, CustomEntry] | None = None,
    ) -> None:
        """
        Args:
            es_matriz:     Indica si las entries son para ingresar una matriz.
            entry_list:    La lista de entries que recibirán bindings.
            extra_entries: Las entries adicionales que se deben tomar en cuenta
                          (nombre, filas, columnas, dimensiones).

        Raises:
            ValueError: Si 'entry_list' o 'extra_entries' son listas vacías;
                        si 'es_matriz' es True y 'entry_list' no es una lista 2D;
                        si 'es_matriz' es False y 'entry_list' no es una lista 1D.

        """

        self.es_matriz = es_matriz
        self.entry_list = entry_list
        self.extra_entries = extra_entries

        if entry_list is None:
            # deferir las validaciones hasta que se crean los bindings
            return

        if self.entry_list == []:
            raise ValueError("Argumento 'entry_list' no puede ser una lista vacía.")
        if self.extra_entries == []:
            raise ValueError("Argumento 'extra_entries' no puede ser una lista vacía.")

        if self.es_matriz and not all(
            isinstance(row, list)
            for row in self.entry_list  # type: ignore[reportOptionalIterable]
        ):
            raise ValueError(
                "Para una matriz, 'entry_list' debe ser una lista bidimensional.",
            )
        if not self.es_matriz and any(
            isinstance(item, list)
            for item in self.entry_list  # type: ignore[reportOptionalIterable]
        ):
            raise ValueError(
                "Para un vector, 'entry_list' debe ser una lista unidimensional.",
            )

    def create_key_bindings(self) -> None:
        """
        Crear los keybindings de todos los CustomEntry's especificados.

        Raises:
            ValueError: Si 'entry_list' o 'extra_entries' son None.
        ---

        """

        if self.entry_list is None:
            raise ValueError("Atributo 'entry_list' no puede ser None.")
        if self.extra_entries is None:
            raise ValueError("Atributo 'extra_entries' no puede ser None.")

        if self.es_matriz:
            for i, row in enumerate(self.entry_list):
                for j, entry in enumerate(row):  # type: ignore[reportArgumentType]
                    self._bind_mat_entry(i, j, entry)
        else:
            for i, entry in enumerate(self.entry_list):
                self._bind_vec_entry(i, entry)  # type: ignore[reportArgumentType]

    def _bind_mat_entry(self, row: int, column: int, entry: CustomEntry) -> None:
        """
        Crear bindings para un entry de una matriz.

        Args:
            row:    Fila del entry.
            column: Columna del entry.
            entry:  CustomEntry a configurar.
        ---

        """

        nombre_entry, filas_entry = self.extra_entries  # type: ignore[reportGeneralTypeIssues]
        entry.bind("<Up>", lambda _: self._entry_move_up(row, column, filas_entry))
        entry.bind("<Down>", lambda _: self._entry_move_down(row, column, nombre_entry))
        entry.bind("<Left>", lambda _: self._entry_move_left(row, column))
        entry.bind("<Right>", lambda _: self._entry_move_right(row, column))
        entry.bind("<Control-Tab>", self.autocomplete_all)

    def _bind_vec_entry(self, row: int, entry: CustomEntry) -> None:
        """
        Crear bindings para un entry de un vector.

        Args:
            row:    Fila del entry.
            entry:  CustomEntry a configurar.
        ---

        """

        nombre_entry, dimensiones_entry = self.extra_entries  # type: ignore[reportGeneralTypeIssues]
        entry.bind("<Up>", lambda _: self._entry_move_up(row, -1, dimensiones_entry))
        entry.bind("<Down>", lambda _: self._entry_move_down(row, -1, nombre_entry))
        entry.bind("<Control-Tab>", self.autocomplete_all)

    def _entry_move_up(self, row: int, column: int, data_entry: CustomEntry) -> None:
        """
        Cambiar focus al entry encima del actual,
        o al entry de filas/dimensiones si ya se llegó al inicio.

        Args:
            row:        Fila del entry.
            column:     Columna del entry.
            data_entry: CustomEntry a configurar.
        ---

        """

        if row > 0:
            if self.es_matriz:
                self.entry_list[row - 1][column].focus_set()  # type: ignore[reportOptionalSubscript]
            else:
                self.entry_list[row - 1].focus_set()  # type: ignore[reportOptionalSubscript]
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
        Cambiar focus al entry debajo del actual,
        o al entry de nombre si ya se llegó al final.

        Args:
            row:          Fila del entry.
            column:       Columna del entry.
            nombre_entry: CustomEntry a configurar.
        ---

        """

        if row < len(self.entry_list) - 1:  # type: ignore[reportArgumentType]
            if self.es_matriz:
                self.entry_list[row + 1][column].focus_set()  # type: ignore[reportOptionalSubscript]
            else:
                self.entry_list[row + 1].focus_set()  # type: ignore[reportOptionalSubscript]
        elif row == len(self.entry_list) - 1:  # type: ignore[reportArgumentType]
            nombre_entry.focus_set()

    def _entry_move_left(self, row: int, column: int) -> None:
        """
        Cambiar focus al entry a la izquierda;
        a la fila anterior (si se llegó al inicio de la fila);
        o al entry de datos iniciales (si se llegó al inicio de la lista).
        Solamente utilizado para los bindings de matrices.

        Args:
            row:    Fila del entry.
            column: Columna del entry.
        ---

        """

        if column > 0:
            self.entry_list[row][column - 1].focus_set()  # type: ignore[reportOptionalSubscript]
        elif column == 0:
            if row > 0:
                self.entry_list[row - 1][-1].focus_set()  # type: ignore[reportOptionalSubscript]
            elif row == 0:
                self.focus_last()

    def _entry_move_right(self, row: int, column: int) -> None:
        """
        Cambiar focus al entry a la derecha;
        al siguiente fila (si ya se llegó al final de la fila);
        o al entry de nombre (si ya se llegó al final de la lista).
        Solamente utilizado para los bindings de matrices.

        Args:
            row:    Fila del entry.
            column: Columna del entry.
        ---

        """

        if column < len(self.entry_list[row]) - 1:  # type: ignore[reportOptionalSubscript]
            self.entry_list[row][column + 1].focus_set()  # type: ignore[reportOptionalSubscript]
        elif column == len(self.entry_list[row]) - 1:  # type: ignore[reportOptionalSubscript]
            if row < len(self.entry_list) - 1:  # type: ignore[reportArgumentType]
                self.entry_list[row + 1][0].focus_set()  # type: ignore[reportOptionalSubscript]
            elif row == len(self.entry_list) - 1:  # type: ignore[reportArgumentType]
                self.focus_first()

    def focus_first(self) -> None:
        """
        Cambiar focus a la primera entry de la lista.
        """

        try:
            if self.es_matriz:
                self.entry_list[0][0].focus_set()  # type: ignore[reportOptionalSubscript]
            else:
                self.entry_list[0].focus_set()  # type: ignore[reportOptionalSubscript]
        except IndexError:
            pass

    def focus_last(self) -> None:
        """
        Cambiar focus a la última entry de la lista.
        """

        try:
            if self.es_matriz:
                self.entry_list[-1][-1].focus_set()  # type: ignore[reportOptionalSubscript]
            else:
                self.entry_list[-1].focus_set()  # type: ignore[reportOptionalSubscript]
        except IndexError:
            pass

    def autocomplete_all(self, event: Event | None = None) -> str:
        """
        Llamar autocomplete_placeholder() para todos los entries.

        Args:
            event: Evento de tkinter que desencadenó este método.

        """

        del event
        if self.es_matriz:
            for row in self.entry_list:  # type: ignore[reportOptionalIterable]
                for entry in row:  # type: ignore[reportGeneralTypeIssues]
                    entry.autocomplete_placeholder(event=None)
        else:
            for entry in self.entry_list:  # type: ignore[reportOptionalIterable]
                entry.autocomplete_placeholder(event=None)  # type: ignore[reportAttributeAccessIssue]
        return "break"

    @staticmethod
    def focus_dimensiones(dimensiones_entry: CustomEntry) -> None:
        """
        Cambiar focus al entry de ingresar dimensiones.

        Args:
            dimensiones_entry: Entry a enfocar.
        ---

        """

        dimensiones_entry.focus_set()

    @staticmethod
    def focus_filas(filas_entry: CustomEntry) -> None:
        """
        Cambiar focus al entry de ingresar filas.

        Args:
            filas_entry: Entry a enfocar.
        ---

        """

        filas_entry.focus_set()

    @staticmethod
    def focus_columnas(columnas_entry: CustomEntry) -> None:
        """
        Cambiar focus al entry de ingresar columnas.

        Args:
            columnas_entry: Entry a enfocar.
        ---

        """

        columnas_entry.focus_set()
