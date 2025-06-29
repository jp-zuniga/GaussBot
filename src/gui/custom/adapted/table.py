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

from .scrollframe import CustomScrollFrame


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
        self.rowconfigure(1, weight=1)

        self.top_fg = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        self.fg = ThemeManager.theme["CTkFrame"]["fg_color"]

        ctkLabel(self, text=header, font=ctkFont(size=16, weight="bold")).grid(
            row=0, column=0, padx=20, pady=20, sticky="nsew"
        )

        self.dummy_frame = CustomScrollFrame(
            self,
            border_width=0,
            scrollbar_width=14,
            scrollbar_padding=(0, 0),
            fg_color="transparent",
        )

        self.init_table()

    def init_table(self):
        """
        Initialize the table.
        """

        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.dummy_frame.rowconfigure(i, weight=1)
                self.dummy_frame.columnconfigure(j, weight=1)
                cell = ctkButton(
                    self.dummy_frame,
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
                    row=i,
                    column=j,
                    padx=(0, 6) if j == 0 else (1, 0),
                    pady=3 if i == 0 or i == len(self.values) - 1 else (0, 1),
                    sticky="nsew",
                )
        self.dummy_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
