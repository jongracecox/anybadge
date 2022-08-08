# Set some defaults
from typing import Dict

DEFAULT_FONT: str = "DejaVu Sans,Verdana,Geneva,sans-serif"
DEFAULT_FONT_SIZE: int = 11
NUM_PADDING_CHARS: float = 0.5
DEFAULT_COLOR: str = "#4c1"
DEFAULT_TEXT_COLOR: str = "#fff"
MASK_ID_PREFIX: str = "anybadge_"

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
