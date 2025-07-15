"""
Based on CTkTable by Akash Bora (https://github.com/Akascape/CTkTable).
"""

from __future__ import annotations

from csv import writer
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from customtkinter import CTkButton, CTkFont, ThemeManager
from tzlocal import get_localzone

from .scrollframe import CustomScrollFrame

if TYPE_CHECKING:
    from customtkinter import CTk, CTkFrame, CTkToplevel

    from src.gui import GaussUI
    from src.gui.custom.adapted import CustomMessageBox


class CustomTable(CustomScrollFrame):
    """
    Table widget to display data as a grid.
    """

    def __init__(
        self,
        app: GaussUI,
        master: CTk | CTkFrame | CTkToplevel | CustomScrollFrame | GaussUI,
        values: list[list[str]],
        header: str = "Registro de Iteraciones:",
    ) -> None:
        """
        Initialize cells of table.

        Args:
            app:    Root application instance.
            master: Window within which this widget is in.
            values: Values of table.
            header: Table header.

        """

        from src.gui.custom import IconButton

        super().__init__(master, border_width=3, fg_color="transparent")

        self.rowconfigure(1, weight=1)
        self.app = app
        self.parent = master

        self.values = values
        self.msg_box: CustomMessageBox | None = None

        CTkButton(
            self,
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=ThemeManager.theme["CTkFrame"]["border_color"],
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            text=header,
            font=CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover=False,
        ).grid(
            row=0,
            column=0,
            columnspan=len(self.values[0]) - 2,
            ipadx=5,
            padx=10,
            pady=10,
            sticky="nw",
        )

        self.init_table()
        IconButton(
            self,
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=ThemeManager.theme["CTkFrame"]["border_color"],
            text_color=ThemeManager.theme["CTkLabel"]["text_color"],
            text="Exportar tabla",
            font=CTkFont(size=12, slant="italic"),
            command=self.export_to_csv,
        ).grid(row=0, column=len(self.values[0]) - 1, padx=10, pady=10, sticky="ne")

    def init_table(self) -> None:
        """
        Initialize the table.
        """

        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.rowconfigure(i + 1, weight=1)
                cell = CTkButton(
                    self,
                    text=value,
                    text_color=ThemeManager.theme["CTkLabel"]["text_color"],
                    fg_color=(
                        ThemeManager.theme["CTkButton"]["fg_color"]
                        if i == len(self.values) - 1
                        else ThemeManager.theme["CTkFrame"]["top_fg_color"]
                        if i % 2 == 0
                        else ThemeManager.theme["CTkFrame"]["fg_color"]
                        if i != 0
                        else "transparent"
                    ),
                    border_color=ThemeManager.theme["CTkFrame"]["border_color"],
                    border_width=2 if i in (0, len(self.values) - 1) else 1,
                    border_spacing=1,
                    corner_radius=10,
                    font=CTkFont(
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

                cell._text_label.configure(  # type: ignore[reportOptionalMemberAccess]  # noqa: SLF001
                    justify="center",
                )
                cell.grid(
                    row=i + 1,
                    column=j,
                    padx=(10, 5)
                    if j == 0
                    else (3, 0)
                    if j != len(self.values[0]) - 1
                    else (3, 10),
                    pady=5
                    if i == 0
                    else (0, 2)
                    if i != len(self.values) - 1
                    else (3, 5),
                    sticky="nsw",
                )

    def export_to_csv(self) -> None:
        """
        Export table data to a CSV file.
        """

        from .messagebox import CustomMessageBox

        if self.msg_box is not None:
            self.msg_box.focus()
            return

        csv_path: Path = (
            Path.home()
            / "Desktop"
            / f"registro_iteraciones_{
                datetime.now(tz=get_localzone()).strftime('%Y-%m-%d_%H:%M:%S')
            }.csv"
        )

        with csv_path.open(mode="w") as file:
            writer(file).writerows(self.values)

        self.msg_box = CustomMessageBox(
            self.app,
            width=480,
            name="¡Exportación exitosa!",
            msg=f"La tabla ha sido exportada exitosamente al archivo\n'{csv_path}'.",
            button_options=("Ok", None, None),
            icon="check",
            bg_color=ThemeManager.theme["CTk"]["fg_color"],
            fg_color=ThemeManager.theme["CTkFrame"]["fg_color"],
        )

        self.msg_box.get()
        self.msg_box.destroy()
        self.msg_box = None
