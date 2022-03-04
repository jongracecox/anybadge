"""Templates package."""
import pkgutil

from anybadge.exceptions import UnknownBadgeTemplate


def get_template(name: str) -> str:
    """Get a template by name.

    Examples:

        >>> get_template('default')  # doctest: +ELLIPSIS
        '<?xml version="1.0" encoding="UTF-8...

    """
    try:
        return pkgutil.get_data(__name__, name + ".svg").decode("utf-8")
    except FileNotFoundError as e:
        raise UnknownBadgeTemplate from e
