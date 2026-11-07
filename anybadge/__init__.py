import re

from .badge import Badge
from .colors import Color
from .styles import Style


def _get_version():
    """Return the installed distribution version for anybadge, if known.

    The installed distribution version is used when the package is installed
    (sdist, wheel or editable install).  "None" is returned when running from
    an uninstalled source checkout, or on Python 3.7 where importlib.metadata
    is not available in the standard library.
    """
    try:
        from importlib.metadata import version  # Python >= 3.8
    except ImportError:  # pragma: no cover - Python 3.7
        return None
    try:
        return version("anybadge")
    except Exception:  # pragma: no cover - uninstalled source checkout
        return None


# Package information
_version = _get_version()
version = __version__ = _version if _version else "0.0.0"
__version_info__ = tuple(re.split("[.-]", __version__))
__title__ = "anybadge"
__summary__ = "A simple, flexible badge generator."
__uri__ = "https://github.com/jongracecox/anybadge"
