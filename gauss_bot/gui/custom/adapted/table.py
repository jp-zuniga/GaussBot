"""
Based on:
* https://github.com/Akascape/CTkTable
* By: Akash Bora

Modified by: Joaquín Zúñiga, on 11/21/2024.
Heavily modified and simplified the original
for the purposes of this project.
"""

from customtkinter import (
    CTkButton as ctkButton,
    CTkFont as ctkFont,
    CTkFrame as ctkFrame,
    CTkLabel as ctkLabel,
    CTkToplevel as ctkTop,
    ThemeManager,
)

from ..custom_frames import CustomScrollFrame


class CustomTable(ctkFrame):
    """
    Table widget to display data as a grid.
    """

    def __init__(
        self,
        master: ctkTop,
        values: list[list[str]],
        header: str = "Registro de Iteraciones:",
    ):
        super().__init__(
            master, corner_radius=20, border_width=3, fg_color="transparent"
        )

        self.parent = master
        self.values = values
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.top_fg = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        self.fg = ThemeManager.theme["CTkFrame"]["fg_color"]

        ctkLabel(
            self, text=header, font=ctkFont(size=14, weight="bold", underline=True)
        ).grid(row=0, column=0, padx=20, pady=20, sticky="new")

        self.header_frame = ctkFrame(self, fg_color="transparent", border_width=0)

        self.header_frame.rowconfigure(0, weight=1)
        for j, value in enumerate(self.values[0]):
            self.header_frame.columnconfigure(j, weight=1)
            cell = ctkButton(
                self.header_frame,
                text=value,
                fg_color="transparent",
                text_color=ThemeManager.theme["CTkEntry"]["text_color"],
                border_color=ThemeManager.theme["CTkFrame"]["border_color"],
                border_width=2,
                border_spacing=0,
                corner_radius=6,
                font=ctkFont(size=12, weight="bold"),
                hover=False,
            )

            cell._text_label.configure(justify="center")  # type: ignore
            cell.grid(row=0, column=j, padx=6 if j == 0 else (1, 0), sticky="nsew")

        self.cells_frame = CustomScrollFrame(
            self, border_width=0, fg_color="transparent"
        )

        self.header_frame.grid(row=1, column=0, padx=20, sticky="nsew")
        self.cells_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")

        self.cells: list[list[ctkButton]] = [[]]
        self.init_table()

    def init_table(self):
        """
        Initialize the table.
        """

        for i, row in enumerate(self.values[1:]):
            for j, value in enumerate(row):
                self.cells_frame.rowconfigure(i, weight=1)
                self.cells_frame.columnconfigure(j, weight=1)

                cell = ctkButton(
                    self.cells_frame,
                    text=value,
                    fg_color=(
                        ThemeManager.theme["CTkButton"]["fg_color"]
                        if i == len(self.values) - 2
                        else self.top_fg
                        if i % 2 == 0
                        else self.fg
                    ),
                    text_color=ThemeManager.theme["CTkEntry"]["text_color"],
                    border_color=ThemeManager.theme["CTkFrame"]["border_color"],
                    border_width=2 if i == len(self.values) - 2 else 1,
                    border_spacing=0,
                    corner_radius=6,
                    font=ctkFont(
                        size=(12 if j == 0 or i == len(self.values) - 2 else 10),
                        weight=(
                            "bold" if j == 0 or i == len(self.values) - 2 else "normal"
                        ),
                    ),
                    hover=False,
                )

                cell._text_label.configure(justify="center")  # type: ignore
                cell.grid(
                    row=i,
                    column=j,
                    padx=(0, 6) if j == 0 else (1, 0),
                    pady=3 if i == len(self.values) - 2 else (0, 1),
                    sticky="nsew",
                )
