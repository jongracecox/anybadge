# Set some defaults
from typing import Dict

DEFAULT_FONT: str = "DejaVu Sans,Verdana,Geneva,sans-serif"
DEFAULT_FONT_SIZE: int = 11
NUM_PADDING_CHARS: float = 0.5
DEFAULT_COLOR: str = "#4c1"
DEFAULT_TEXT_COLOR: str = "#fff"
MASK_ID_PREFIX: str = "anybadge_"

# Logo defaults.  The logo is rendered in a square LOGO_SIZE box, with
# LOGO_MARGIN pixels of space at the outer badge edge.
LOGO_SIZE: int = 14
LOGO_MARGIN: int = 5
DEFAULT_LOGO_POSITION: str = "left"
VALID_LOGO_POSITIONS = ("left", "right")
# Vertical offset of the logo box within badges, which are 20px tall.
LOGO_Y: int = 3
# Gap in pixels between the logo and the adjacent label/value text.  This
# replaces the text padding character on the side the logo sits on, so
# the logo and text sit close together while text keeps its normal
# padding on the side away from the logo.
LOGO_TEXT_GAP: int = 3

# Dictionary for looking up approx pixel widths of
# supported fonts and font sizes.
FONT_WIDTHS: Dict[str, Dict[int, int]] = {
    "DejaVu Sans,Verdana,Geneva,sans-serif": {
        10: 9,
        11: 10,
        12: 11,
    },
    "Arial, Helvetica, sans-serif": {
        11: 8,
    },
}
