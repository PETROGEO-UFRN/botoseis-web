from typing import Literal
from bokeh.colors import RGB
from bokeh.palettes import linear_palette
from bokeh.palettes import Greys256, BuRd9, RdBu11, Reds256, Blues256

red_black_palette = linear_palette(
    [RGB(r, 0, 0) for r in range(255, -1, -1)],
    256
)

red_blue_palette = linear_palette(
    list(reversed(Blues256)),
    256 // 2
) + linear_palette(
    Reds256,
    256 // 2
)

blue_red_palette = linear_palette(
    list(reversed(Reds256)),
    256 // 2
) + linear_palette(
    Blues256,
    256 // 2
)


def get_plot_pallete(
    selectedPalette: Literal[
        "grey", "red_black", "red_blue", "blue_red", "BuRd", "RdGy"
    ]
):
    if selectedPalette == "grey":
        return Greys256
    if selectedPalette == "red_black":
        return red_black_palette
    if selectedPalette == "red_blue":
        return red_blue_palette
    if selectedPalette == "blue_red":
        return blue_red_palette
    if selectedPalette == "BuRd":
        return BuRd9
    if selectedPalette == "RdGy":
        return RdBu11
