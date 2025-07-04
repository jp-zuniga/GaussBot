"""
Based on:
* https://github.com/Akascape/CTkTable
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/21/2024.
Heavily modified and simplified the original
for the purposes of this project.
"""

from csv import writer
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkToplevel as ctkTop,
    ThemeManager,
)

from .scrollframe import CustomScrollFrame

if TYPE_CHECKING:
    from ...gui import GaussUI


class CustomTable(CustomScrollFrame):
    """
    Table widget to display data as a grid.
    """

    def __init__(
        self,
        app: "GaussUI",
        master: ctkTop,
        values: list[list[str]],
        header: str = "Registro de Iteraciones:",
    ):
        from .. import IconButton

        super().__init__(master, border_width=3, fg_color="transparent")
        self.rowconfigure(1, weight=1)
        self.app = app
        self.values = values

        ctkButton(
            self,
            height=30,
            corner_radius=10,
            border_width=2,
            text=header,
            font=ctkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover=False,
        ).grid(
            row=0,
            column=0,
            columnspan=len(self.values[0]) - 2,
            ipadx=5,
            padx=20,
            pady=20,
            sticky="nw",
        )

        self.init_table()
        IconButton(
            self,
            self.app,
            corner_radius=10,
            border_width=2,
            text="Exportar a CSV",
            tooltip_text="Exportar la tabla a un archivo .csv.",
            command=self.export_to_csv,
            swap_tooltip_colors=True,
        ).grid(row=0, column=len(self.values[0]) - 1, padx=20, pady=20, sticky="ne")

    def init_table(self):
        """
        Initialize the table.
        """

        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.rowconfigure(i + 1, weight=1)
                cell = ctkButton(
                    self,
                    text=value,
                    fg_color=(
                        ThemeManager.theme["CTkButton"]["fg_color"]
                        if i == len(self.values) - 1
                        else ThemeManager.theme["CTkFrame"]["top_fg_color"]
                        if i % 2 == 0
                        else ThemeManager.theme["CTkFrame"]["fg_color"]
                        if i != 0
                        else "transparent"
                    ),
                    border_width=2 if i == 0 or i == len(self.values) - 1 else 1,
                    border_spacing=1,
                    corner_radius=10,
                    font=ctkFont(
                        size=(
                            12 if j == 0 or i == 0 or i == len(self.values) - 1 else 10
                        ),
                        weight=(
                            "bold"
                            if j == 0 or i == 0 or i == len(self.values) - 1
                            else "normal"
                        ),
                    ),
                    hover=False,
                )

                cell._text_label.configure(justify="center")  # type: ignore
                cell.grid(
                    row=i + 1,
                    column=j,
                    padx=(20, 5)
                    if j == 0
                    else (3, 0)
                    if j != len(self.values[0]) - 1
                    else (3, 20),
                    pady=5
                    if i == 0
                    else (0, 2)
                    if i != len(self.values) - 1
                    else (3, 5),
                    sticky="nsw",
                )

    def export_to_csv(self):
        """
        Export table data to a CSV file.
        """

        from .messagebox import CustomMessageBox

        if hasattr(self, "_quit_box") and self._quit_box.winfo_exists():
            self._quit_box.focus()
            return

        csv_path: Path = (
            Path.home()
            / "Desktop"
            / f"registro_iteraciones_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
        )

        with open(csv_path, mode="w", encoding="utf-8", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerows(self.values)

        self._quit_box = CustomMessageBox(
            self.app,
            width=480,
            name="¡Exportación exitosa!",
            msg=f"La tabla ha sido exportada exitosamente al archivo\n'{csv_path}'.",
            button_options=("Ok", None, None),
            icon="check",
            bg_color=ThemeManager.theme["CTk"]["fg_color"],
            fg_color=ThemeManager.theme["CTkFrame"]["fg_color"],
        )

        self._quit_box.get()
        self._quit_box.destroy()
        del self._quit_box
