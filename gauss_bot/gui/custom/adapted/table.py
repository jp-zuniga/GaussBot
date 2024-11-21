"""
Based on:
* https://github.com/Akascape/CTkTable
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/21/2024.
Heavily simplified the original CTkTable
for the purposes of this project.
"""

from typing import Any
from customtkinter import (
    CTkButton as ctkButton,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    ThemeManager,
)


class CustomTable(ctkFrame):
    """
    Table widget to display data as a grid.
    """

    def __init__(
        self,
        master: Any,
        header: str,
        values: list[list],
    ):

        super().__init__(
            master,
            corner_radius=30,
            border_width=3,
            fg_color="transparent",
        )

        self.values = values
        self.rows = len(self.values)
        self.columns = len(self.values[0])

        self.fg = ThemeManager.theme["CTkFrame"]["fg_color"]
        self.top_fg = ThemeManager.theme["CTkFrame"]["top_fg_color"]

        ctkLabel(
            self,
            text=header,
        ).pack(expand=True, fill="both", padx=20, pady=(20, 4))

        self.inside_frame = ctkFrame(
            self,
            border_width=0,
            fg_color="transparent",
        )

        self.inside_frame.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=(4, 20),
        )

        self.cells: list[list[ctkButton]] = [[]]
        self.draw_table()

    def draw_table(self):
        """
        Initialize the table.
        """

        for i in range(self.rows):
            row: list[ctkButton] = []  # type: ignore
            for j in range(self.columns):
                self.inside_frame.rowconfigure(i, weight=1)
                self.inside_frame.columnconfigure(j, weight=1)

                if i == 0:
                    bw = 2
                    pady = (0, 5)
                    font = ("Roboto", 12, "bold")
                else:
                    bw = 1
                    pady = (0, 1)
                    font = ("Roboto", 10)

                if i == 0:
                    fg = "transparent"
                elif i % 2 == 0:
                    fg = self.top_fg
                else:
                    fg = self.fg
                bc = ThemeManager.theme["CTkFrame"]["border_color"]
                tc = ThemeManager.theme["CTkEntry"]["text_color"]

                cell = self.values[i][j]
                row.append(
                    ctkButton(
                        self.inside_frame,
                        text=cell,
                        text_color=tc,
                        border_color=bc,
                        border_width=bw,
                        border_spacing=0,
                        corner_radius=5,
                        fg_color=fg,  # pylint: disable=E0606
                        font=font,
                        hover=False,
                    )
                )

                row[j]._text_label.configure(justify="center", wraplength=200)  # pylint: disable=W0212
                row[j].grid(
                    row=i,
                    column=j,
                    padx=1 if j == 0 else (0, 1),
                    pady=pady,
                    sticky="nsew",
                )
            self.cells.append(row)
