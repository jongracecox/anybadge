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
        data = pkgutil.get_data(__name__, name + ".svg")
    except FileNotFoundError as e:
        raise UnknownBadgeTemplate from e

    if not data:
        raise UnknownBadgeTemplate

    # Normalize newlines so that a Windows checkout (with CRLF files) produces
    # the same template text as a Linux checkout.
    return data.decode("utf-8").replace("\r\n", "\n")
