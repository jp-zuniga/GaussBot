# Acknowledgements

## Personalized Widgets

The files in [`src/gui/custom/adapted`](https://github.com/jp-zuniga/GaussBot/tree/main/src/gui/custom/adapted)
contain implementations of custom widgets used in GaussBot.

All of them are based on the work of [Akash Bora](https://github.com/akascape).

| Personalized Implementation |                                   Source                                    |  Licensed Under   |
| :-------------------------: | :-------------------------------------------------------------------------: | :---------------: |
|     `CustomMessageBox`      |    [`Akascape/CTkMessagebox`](https://github.com/Akascape/CTkMessagebox)    | CC0 1.0 Universal |
|       `CustomNumpad`        | [`Akascape/CTkPopupKeyboard`](https://github.com/Akascape/CTkPopupKeyboard) |    MIT License    |
|     `CustomScrollFrame`     |       [`Akascape/CTkXYFrame`](https://github.com/Akascape/CTkXYFrame)       |    MIT License    |
|        `CustomTable`        |         [`Akascape/CTkTable`](https://github.com/Akascape/CTkTable)         |    MIT License    |
|          `Tooltip`          |       [`Akascape/CTkToolTip`](https://github.com/Akascape/CTkToolTip)       | CC0 1.0 Universal |

Generally speaking, the original code was heavily formatted and refactored.
A lot of the functionality aimed at general-purpose use was removed in the interest of simplicity.
Additionally, the widget designs were modified in order to better match the simple and modern look of GaussBot.

## Icons

Most of the [icons](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/icons)
used in GaussBot's GUI were sourced from [The Noun Project](https://thenounproject.com),
which offers free, attribution-based licenses for non-commercial uses.
For compatibility with GaussBot's themes, the original black icons were inverted to white using
[GIMP](https://www.gimp.org/) for use in both light and dark modes.

Additionally, two of the icons were slightly modified:

* [M. Oki Orlando's](https://thenounproject.com/creator/orvipixel/)
["Linear Algebra"](https://thenounproject.com/icon/linear-algebra-4998468/) icon
was converted to the `.ico` file format for use as the application's icon on Windows machines.
* [Sophia's](https://thenounproject.com/creator/sophiabai/)
["Dropdown Arrow"](https://thenounproject.com/icon/dropdown-arrow-1590826/) icon
was rotated to obtain up, left, and right-pointing versions.

|                                           File Name                                           |   Icon Name    |   Artist Name   |                                 Source                                  | Licensed Under |
| :-------------------------------------------------------------------------------------------: | :------------: | :-------------: | :---------------------------------------------------------------------: | :------------: |
|                                      `aceptar_icon.png`                                       |   Check Mark   |      Aini       |   [Noun Project](https://thenounproject.com/icon/check-mark-470987/)    |   CC BY 3.0    |
|                                      `analisis_icon.png`                                      |    Function    | Yeong Rong Kim  |    [Noun Project](https://thenounproject.com/icon/function-4866495/)    |   CC BY 3.0    |
|                                       `config_icon.png`                                       |    Settings    |     raptor      |    [Noun Project](https://thenounproject.com/icon/settings-7294076/)    |   CC BY 3.0    |
| `dropdown_icon.png` <br> `dropleft_icon.png` <br> `dropright_icon.png` <br> `dropup_icon.png` | Dropdown Arrow |     Sophia      | [Noun Project](https://thenounproject.com/icon/dropdown-arrow-1590826/) |   CC BY 3.0    |
|                                     `ecuaciones_icon.png`                                     |     Equal      |      Khoir      |     [Noun Project](https://thenounproject.com/icon/equal-7250715/)      |   CC BY 3.0    |
|                                      `eliminar_icon.png`                                      |     Trash      |   maria icon    |     [Noun Project](https://thenounproject.com/icon/trash-5726444/)      |   CC BY 3.0    |
|                                       `enter_icon.png`                                        |     Enter      |      Baiti      |     [Noun Project](https://thenounproject.com/icon/enter-2987854/)      |   CC BY 3.0    |
|                                        `info_icon.png`                                        |      Info      |  Laurène Smith  |       [Noun Project](https://thenounproject.com/icon/info-51140/)       |   CC BY 3.0    |
|                                       `input_icon.png`                                        |     Input      |   Megan Chown   |     [Noun Project](https://thenounproject.com/icon/input-3437016/)      |   CC BY 3.0    |
|                                      `limpiar_icon.png`                                       |     Delete     |  Vicons Design  |      [Noun Project](https://thenounproject.com/icon/delete-78799/)      |   CC BY 3.0    |
|                                  `logo.png` <br> `logo.ico`                                   | Linear Algebra | M. Oki Orlando  | [Noun Project](https://thenounproject.com/icon/linear-algebra-4998468/) |   CC BY 3.0    |
|                                       `matriz_icon.png`                                       |     Matrix     |      Soapi      |     [Noun Project](https://thenounproject.com/icon/matrix-5886353/)     |   CC BY 3.0    |
|                                      `mostrar_icon.png`                                       |      Show      |  erix subyarko  |      [Noun Project](https://thenounproject.com/icon/show-5831666/)      |   CC BY 3.0    |
|                                      `shuffle_icon.png`                                       |     Random     |  Utari Nuraeni  |     [Noun Project](https://thenounproject.com/icon/random-6179921/)     |   CC BY 3.0    |
|                                      `question_icon.png`                                      |    Question    | Gregor Cresnar  |    [Noun Project](https://thenounproject.com/icon/question-670398/)     |   CC BY 3.0    |
|                                        `quit_icon.png`                                        |     Close      | Michael Wallner |      [Noun Project](https://thenounproject.com/icon/close-25798/)       |   CC BY 3.0    |
|                                       `vector_icon.png`                                       |     Vector     |    rendicon     |     [Noun Project](https://thenounproject.com/icon/vector-5819613/)     |   CC BY 3.0    |

> ### Note
>
> * The following icons were made from scratch using [Canva](https://www.canva.com/):
>   * [`check_icon.png`](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/icons/check_icon.png)
>   * [`error_icon.png`](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/icons/error_icon.png)
>   * [`warning_icon.png`](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/icons/warning_icon.png)
>   * [`h_separator.png`](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/icons/light/h_separator.png)
>   * [`v_separator.png`](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/icons/light/v_separator.png)
> * The icons used for the [`CustomNumpad`](https://github.com/jp-zuniga/GaussBot/tree/main/src/gui/custom/adapted/numpad.py)
>   widget were rendered using [LaTeX](https://www.latex-project.org/about/) and [matplotlib](https://github.com/matplotlib/matplotlib).

## Themes

GaussBot's [themes and color palettes](https://github.com/jp-zuniga/GaussBot/tree/main/src/assets/themes)
are based on the work of [a13xe](https://github.com/a13xe), who generously dedicated their CustomTkinter
theme designs to the public domain.

| Personalized Theme |                                   Original Theme                                    | Licensed Under |
| :----------------: | :---------------------------------------------------------------------------------: | :------------: |
|    `Primavera`     |      [`Sky`](https://github.com/a13xe/CTkThemesPack/tree/main/themes/sky.json)      |   Unlicense    |
|      `Verano`      |   [`Cherry`](https://github.com/a13xe/CTkThemesPack/tree/main/themes/cherry.json)   |   Unlicense    |
|      `Otoño`       |   [`Coffee`](https://github.com/a13xe/CTkThemesPack/tree/main/themes/coffee.json)   |   Unlicense    |
|     `Invierno`     | [`Midnight`](https://github.com/a13xe/CTkThemesPack/tree/main/themes/midnight.json) |   Unlicense    |

The `Coffee` theme was used mostly unchanged, while the others were slightly modified to fit the visual aesthetic of GaussBot.
