import re
from .badge import Badge
from .colors import Color
from .styles import Style

# Package information
version = __version__ = "0.0.0"
__version_info__ = tuple(re.split("[.-]", __version__))
__title__ = "anybadge"
__summary__ = "A simple, flexible badge generator."
__uri__ = "https://github.com/jongracecox/anybadge"
