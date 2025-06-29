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
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
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
        super().__init__(
            master, corner_radius=20, border_width=3, fg_color="transparent"
        )

        self.parent = master
        self.values = values
        self.rowconfigure(1, weight=1)

        self.top_fg = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        self.fg = ThemeManager.theme["CTkFrame"]["fg_color"]

        self.header_frame = ctkFrame(self)

        ctkLabel(
            self.header_frame, text=header, font=ctkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctkButton(
            self.header_frame,
            text="Exportar a CSV",
            font=ctkFont(size=12, weight="bold"),
            command=self.export_to_csv,
        ).grid(row=0, column=1, padx=20, pady=20, sticky="ne")

        self.header_frame.grid(row=0, column=0, columnspan=len(self.values[0]))
        self.init_table()

    def init_table(self):
        """
        Initialize the table.
        """

        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.rowconfigure(i + 1, weight=1)
                self.columnconfigure(j, weight=1)
                cell = ctkButton(
                    self,
                    text=value,
                    fg_color=(
                        ThemeManager.theme["CTkButton"]["fg_color"]
                        if i == len(self.values) - 1
                        else self.top_fg
                        if i % 2 == 0
                        else self.fg
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
                    padx=(0, 6) if j == 0 else (1, 0),
                    pady=3 if i == 0 or i == len(self.values) - 1 else (0, 1),
                    sticky="nsew",
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
            width=400,
            height=200,
            name="¡Exportación exitosa!",
            msg=f"La tabla ha sido exportada exitosamente al archivo '{csv_path}'.",
            button_options=("Ok", None, None),
            icon="check",
        )

        self._quit_box.get()
        self._quit_box.destroy()
        del self._quit_box
