from os import path


ASSET_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "assets"
)

THEMES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "themes"
)

CONFIG_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data",
    "config.json",
)

MATRICES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data", "matrices.json"
)

VECTORES_PATH = path.join(
    path.dirname(path.realpath(__file__)),
    "data", "vectores.json"
)
