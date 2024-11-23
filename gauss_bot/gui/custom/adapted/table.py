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
            master,
            corner_radius=20,
            border_width=3,
            fg_color="transparent",
        )

        self.parent = master
        self.values = values

        self.top_fg = ThemeManager.theme["CTkFrame"]["top_fg_color"]
        self.fg = ThemeManager.theme["CTkFrame"]["fg_color"]

        ctkLabel(
            self,
            text=header,
            font=ctkFont(
                family="Roboto",
                size=14,
                weight="bold",
                underline=True,
            ),
        ).pack(expand=True, fill="both", padx=20, pady=20)

        self.header_frame = ctkFrame(
            self,
            fg_color="transparent",
            border_width=0,
        )

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
                font=("Roboto", 12, "bold"),
                hover=False,
            )

            cell._text_label.configure(justify="center")  # type: ignore
            cell.grid(
                row=0, column=j,
                padx=0 if j == 0 else (1, 0),
                sticky="nsew",
            )

        self.inside_frame = CustomScrollFrame(
            self,
            border_width=0,
            fg_color="transparent",
        )

        self.header_frame.pack(expand=True, fill="both", padx=20)
        self.inside_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.cells: list[list[ctkButton]] = [[]]
        self.init_table()

    def init_table(self):
        """
        Initialize the table.
        """

        for i, row in enumerate(self.values[1:]):
            for j, value in enumerate(row):
                self.inside_frame.rowconfigure(i, weight=1)
                self.inside_frame.columnconfigure(j, weight=1)

                cell = ctkButton(
                    self.inside_frame,
                    text=value,
                    fg_color=self.top_fg if i % 2 == 0 else self.fg,
                    text_color=ThemeManager.theme["CTkEntry"]["text_color"],
                    border_color=ThemeManager.theme["CTkFrame"]["border_color"],
                    border_width=1,
                    border_spacing=0,
                    corner_radius=6,
                    font=("Roboto", 8),
                    hover=False,
                )

                cell._text_label.configure(justify="center")  # pylint: disable=W0212
                cell.grid(
                    row=i,
                    column=j,
                    padx=0 if j == 0 else (1, 0),
                    pady=(0, 1),
                    sticky="nsew",
                )
