# Create a dictionary of colors to make selections
# easier.
from enum import Enum


class Color(Enum):
    WHITE = "#FFFFFF"
    SILVER = "#C0C0C0"
    GRAY = "#808080"
    BLACK = "#000000"
    RED = "#E05D44"
    BRIGHT_RED = "#FF0000"
    MAROON = "#800000"
    OLIVE = "#808000"
    LIME = "#00FF00"
    BRIGHT_YELLOW = "#FFFF00"
    YELLOW = "#DFB317"
    GREEN = "#4C1"
    YELLOW_GREEN = "#A4A61D"
    AQUA = "#00FFFF"
    TEAL = "#008080"
    BLUE = "#0000FF"
    NAVY = "#000080"
    FUCHSIA = "#FF00FF"
    PURPLE = "#800080"
    ORANGE = "#FE7D37"
    LIGHT_GREY = "#9F9F9F"

    def __lt__(self, other):
        return self.name < other.name
