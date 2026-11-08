"""Logo support for badges.

A logo can be provided to a badge in a number of ways, resolved in this
order:

- A path to a local image file (``.svg``, ``.png``, ``.jpg`` or ``.gif``).
- An explicit URL (``http://`` or ``https://``).
- A `Simple Icons <https://simpleicons.org>`_ slug (e.g. ``python``).  The
  slug is first looked up in any configured local logo directories, and
  otherwise in the logos bundled with the package (see :func:`builtin_logos`),
  and is otherwise downloaded from the Simple Icons CDN at
  ``https://cdn.simpleicons.org``.

In all cases the image is embedded into the badge as a base64 ``data:``
URI, so the generated SVG remains fully self-contained and never loads
anything at view time.

Raw logo downloads are memoized in memory, so generating many badges with
the same logo (e.g. when running anybadge-server) downloads each logo
only once per process.

The :func:`fetch_logos` function provides a convenient way to vendor
logos for environments that are gated from the network (e.g. CI runners
or servers without egress).  Logos can be downloaded to plain files
wherever network access is available, committed or passed on as build
artifacts, and then used from disk via the ``logo_dirs`` search path.
"""

import base64
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from .. import config

#: Base URL of the Simple Icons CDN, used to download icons by slug.
SIMPLE_ICONS_CDN_URL: str = "https://cdn.simpleicons.org"

#: Directory containing the logo SVG files bundled with the package.
#: These provide offline logo support for common project logos.
BUILTIN_LOGOS_DIR: Path = Path(__file__).parent

#: Timeout (seconds) applied to logo download requests.
DOWNLOAD_TIMEOUT: float = 10.0

#: User-Agent sent with logo download requests.
USER_AGENT: str = "anybadge"

#: HTTP(S) URL pattern used to identify explicit logo URLs.
_URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)

#: Data URI prefix used for explicitly passed data URIs.
_DATA_URI_PATTERN = re.compile(r"^data:", re.IGNORECASE)

#: Mapping from detected MIME type to the file extension used when
#: writing logos to disk with :func:`fetch_logos`.
_FILE_EXTENSIONS: Dict[str, str] = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
}

#: In-process memoization of logo downloads and file reads, keyed by
#: source string, logo color and search directories tuple.
_LOGO_CACHE: Dict[Tuple, bytes] = {}


def _detect_mime_type(data: bytes) -> str:
    """Return the MIME type of an image based on magic bytes.

    Args:
        data: Image data to inspect.

    Returns:
        str: Detected MIME type.

    Raises:

        ValueError: When the image format is not recognized.
    """
    if data.startswith(b"\x89PNG"):
        return "image/png"
    if data.startswith(b"\xff\xd8"):
        return "image/jpeg"
    if data.startswith(b"GIF8"):
        return "image/gif"
    if b"<svg" in data[:2048].lower():
        return "image/svg+xml"
    raise ValueError(
        "Unrecognized logo image format. Supported formats are SVG, PNG, "
        "JPEG and GIF."
    )


def _download(url: str) -> bytes:
    """Download image data from a URL.

    Args:
        url: URL to download from.

    Returns:
        bytes: The downloaded image data.

    Raises:
        ValueError: When the download fails.
    """
    try:
        request = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response:
            return response.read()
    except (HTTPError, URLError, OSError, ValueError) as e:
        raise ValueError('Failed to download logo from "%s": %s' % (url, e))


def _read_local(path: Path) -> bytes:
    """Read image data from a local file.

    Args:
        path: Path of the image file.

    Returns:
        bytes: The image data.

    Raises:
        ValueError: When the file cannot be read.
    """
    try:
        with open(path, mode="rb") as file_handle:
            return file_handle.read()
    except OSError as e:
        raise ValueError('Failed to read logo file "%s": %s' % (path, e))


def _source_path(source: str, search_dirs: List[Union[str, Path]]) -> Optional[Path]:
    """Search local logo directories for a file matching a source name.

    Args:
        source: Logo name, matched against ``<name>.svg`` etc. in each
            directory.
        search_dirs: Directories to search, in order.

    Returns:
        Optional[Path]: Path of the first matching file, or None.
    """
    extensions = [""] + sorted(_FILE_EXTENSIONS.values())
    for search_dir in search_dirs:
        for extension in extensions:
            path = Path(search_dir) / ("%s%s" % (Path(source).name, extension))
            if path.is_file():
                return path
    return None


def _slug_url(source: str, logo_color: Optional[str]) -> str:
    """Return the Simple Icons CDN URL for a slug.

    Args:
        source: Simple Icons slug (e.g. ``python``).
        logo_color: Optional color for the icon (e.g. ``#fff``).  Applies
            to Simple Icons downloads only.

    Returns:
        str: URL to download the icon from.
    """
    url = "%s/%s" % (SIMPLE_ICONS_CDN_URL, quote(Path(source).name, safe=""))
    if logo_color:
        url += "/%s" % quote(logo_color.lstrip("#"), safe="")
    return url


def _load_logo_bytes(
    source: str, logo_color: Optional[str], search_dirs: List[Union[str, Path]]
) -> bytes:
    """Load logo image bytes without memoization.

    Args:
        source: Local file path, URL or Simple Icons slug.
        logo_color: Optional color for Simple Icons downloads.
        search_dirs: Local directories searched for logo files by name.

    Returns:
        bytes: The logo image data.

    Raises:
        ValueError: When the logo cannot be loaded.
    """
    if _DATA_URI_PATTERN.match(source):
        # A data URI was passed directly; decode it to raw image data so
        # it shares the same code path as other sources.
        _, _, payload = source.partition(",")
        try:
            return base64.b64decode(payload)
        except (ValueError, TypeError) as e:
            raise ValueError("Failed to decode logo data URI: %s" % e)

    if _URL_PATTERN.match(source):
        return _download(source)

    if os.path.isfile(source):
        return _read_local(Path(source))

    path = _source_path(source, search_dirs)
    if path:
        return _read_local(path)

    # Fall back to logos bundled with the package, which provide offline
    # support for common project logos without any network access.
    path = _source_path(source, [BUILTIN_LOGOS_DIR])
    if path:
        return _read_local(path)

    return _download(_slug_url(source, logo_color))


def builtin_logos() -> List[str]:
    """Return the names of logos bundled with the package.

    Returns:
        List[str]: Sorted list of logo names that can be used without any
        network access.
    """
    return sorted(path.stem for path in BUILTIN_LOGOS_DIR.glob("*.svg"))


def get_logo_bytes(
    source: str,
    logo_color: Optional[str] = None,
    search_dirs: Optional[List[Union[str, Path]]] = None,
) -> bytes:
    """Return logo image data for a source, memoizing downloads.

    Args:
        source: Local file path, URL, ``data:`` URI or Simple Icons slug.
        logo_color: Optional color for Simple Icons downloads.
        search_dirs: Local directories searched for logo files by name.

    Returns:
        bytes: The logo image data.

    Raises:
        ValueError: When the logo cannot be loaded.
    """
    key = (source, logo_color, tuple(str(d) for d in search_dirs or []))
    if key not in _LOGO_CACHE:
        _LOGO_CACHE[key] = _load_logo_bytes(source, logo_color, list(search_dirs or []))
    return _LOGO_CACHE[key]


def resolve_logo(
    source: str,
    logo_color: Optional[str] = None,
    search_dirs: Optional[List[Union[str, Path]]] = None,
) -> str:
    """Return a data URI for a logo source.

    Args:
        source: Local file path, URL, ``data:`` URI or Simple Icons slug.
        logo_color: Optional color for Simple Icons downloads.
        search_dirs: Local directories searched for logo files by name.

    Returns:
        str: Base64 ``data:`` URI containing the logo image.

    Raises:
        ValueError: When the logo cannot be loaded.
    """
    if _DATA_URI_PATTERN.match(source):
        return source
    data = get_logo_bytes(source, logo_color, search_dirs)
    mime_type = _detect_mime_type(data)
    encoded = base64.b64encode(data).decode("ascii")
    return "data:%s;base64,%s" % (mime_type, encoded)


def fetch_logos(
    sources: List[str],
    directory: Union[str, Path],
    logo_color: Optional[str] = None,
    overwrite: bool = False,
) -> List[Path]:
    """Download logos and write them as files.

    This is a convenience mechanism for environments that are gated from
    the network (e.g. CI runners or servers without egress): logos can be
    downloaded wherever network access is available, committed to source
    control or passed on as build artifacts, and then referenced by badge
    generation via ``logo_dirs`` without any network access.

    Args:
        sources: List of URLs or Simple Icons slugs to download.
        directory: Directory to write logo files into.  Created if it
            does not already exist.
        logo_color: Optional color for Simple Icons downloads.
        overwrite: Overwrite files that already exist, instead of
            skipping them.

    Returns:
        List[Path]: Paths of the files written.  Sources whose file
        already existed (and ``overwrite`` was not set) are skipped.

    Raises:
        ValueError: When a logo cannot be downloaded.
    """
    directory = Path(directory)
    written: List[Path] = []

    for source in sources:
        if _URL_PATTERN.match(source):
            stem = Path(urlparse(source).path).stem
            if not stem:
                raise ValueError(
                    'Failed to derive a file name from "%s". Please pass a '
                    "Simple Icons slug instead, or a URL ending in a file "
                    "name." % source
                )
        else:
            stem = Path(source).name

        # Skip sources that already have a vendored file, so no download
        # is attempted for them.
        if not overwrite and any(
            (directory / (stem + extension)).exists()
            for extension in _FILE_EXTENSIONS.values()
        ):
            continue

        data = get_logo_bytes(source, logo_color)
        mime_type = _detect_mime_type(data)
        extension = _FILE_EXTENSIONS[mime_type]

        output = directory / (stem + extension)
        directory.mkdir(parents=True, exist_ok=True)
        with open(output, mode="wb") as file_handle:
            file_handle.write(data)
        written.append(output)

    return written
