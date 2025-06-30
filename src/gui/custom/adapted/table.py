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
    # CTkLabel as ctkLabel,
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
            text=header,
            font=ctkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover=False,
        ).grid(
            row=0,
            column=0,
            columnspan=len(self.values[0]) - 1,
            padx=20,
            pady=20,
            sticky="nw",
        )

        self.init_table()
        IconButton(
            self,
            self.app,
            height=30,
            text="Exportar tabla a CSV",
            tooltip_text="Exportar los valores de la tabla a\n "
            + "un archivo .csv en su escritorio.",
            font=ctkFont(weight="bold"),
            fg_color=ThemeManager.theme["CTkButton"]["fg_color"],
            command=self.export_to_csv,
            swap_tooltip_colors=True,
        ).grid(
            row=len(self.values) + 2,
            column=0,
            columnspan=len(self.values[0]) - 1,
            padx=20,
            pady=20,
            sticky="nw",
        )

    def init_table(self):
        """
        Initialize the table.
        """

        top_fg: str = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        fg: str = ThemeManager.theme["CTkFrame"]["fg_color"]

        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.rowconfigure(i + 1, weight=1)
                # self.columnconfigure(j, weight=1)
                cell = ctkButton(
                    self,
                    text=value,
                    fg_color=(
                        ThemeManager.theme["CTkButton"]["fg_color"]
                        if i == len(self.values) - 1
                        else top_fg
                        if i % 2 == 0
                        else fg
                        if i != 0
                        else "transparent"
                    ),
                    text_color=ThemeManager.theme["CTkEntry"]["text_color"],
                    border_color=ThemeManager.theme["CTkFrame"]["border_color"],
                    border_width=2 if i == 0 or i == len(self.values) - 1 else 1,
                    border_spacing=0,
                    corner_radius=8,
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
                    padx=(20, 3)
                    if j == 0
                    else (2, 0)
                    if j != len(self.values[0]) - 1
                    else (2, 20),
                    pady=3 if i == 0 or i == len(self.values) - 1 else (0, 2),
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
