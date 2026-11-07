import re


EMOJI_REGEX = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)


def is_emoji(character):
    """Return True if character is an emoji.

    Examples:

        >>> is_emoji('👍')
        True

        >>> is_emoji('a')
        False

    """
    # Prefer the ``emoji`` package when it is available since its coverage of
    # emoji characters is complete, where as the fallback regex below only
    # covers a subset of emoji blocks.
    try:
        import emoji
    except ImportError:
        pass
    else:
        return emoji.is_emoji(character)

    return bool(EMOJI_REGEX.match(character))


def wrap_emoji_in_tspan(text, font_size, emoji_font_size):
    """Return text with emoji characters wrapped in <tspan> elements.

    Emoji fallback fonts are generally designed to render at a visually
    smaller size than Latin text at the same font size, so to keep badges
    looking balanced, emoji characters are wrapped in ``<tspan>`` elements
    that render them at ``emoji_font_size``.

    Emoji sequences are detected using the ``emoji`` package when it is
    available, falling back to a simple regex otherwise.

    Args:
        text(str): Text that may contain emoji characters.
        font_size(int): Font size used for text that is not emoji.
        emoji_font_size(int): Font size used for emoji characters.

    Returns: str

    Examples:

        >>> wrap_emoji_in_tspan('a\U0001F604b', 11, 14)
        'a<tspan font-size="14">\U0001F604</tspan>b'

        >>> wrap_emoji_in_tspan('abc', 11, 14)
        'abc'

        >>> wrap_emoji_in_tspan('\U0001F604', 11, 11)
        '\U0001F604'
    """
    if not text or emoji_font_size <= font_size:
        return text

    # Get a list of (start, end) offsets of emoji runs in the text. The emoji
    # package is preferred since it tracks the current Unicode emoji set,
    # including sequences such as skin tone modifiers and flag sequences.
    try:
        import emoji
    except ImportError:
        spans = [(match.start(), match.end()) for match in EMOJI_REGEX.finditer(text)]
    else:
        spans = []
        prev_end = None
        for match in emoji.emoji_list(text):
            if prev_end == match["match_start"]:
                # Merge consecutive matches into a single run
                spans[-1] = (spans[-1][0], match["match_end"])
            else:
                spans.append((match["match_start"], match["match_end"]))
            prev_end = spans[-1][1]

    result = []
    pos = 0
    for start, end in spans:
        result.append(text[pos:start])
        result.append(
            '<tspan font-size="%s">%s</tspan>' % (emoji_font_size, text[start:end])
        )
        pos = end
    result.append(text[pos:])
    return "".join(result)


def emojize_text(text):
    """Return text with ``:emoji:`` shortcodes converted to emoji characters.

    Conversion is only carried out when the optional ``emoji`` package is
    installed (``pip install anybadge[emoji]``). When it is not, the text is
    returned unchanged.

    Two conversion passes are made, so both shortcode spellings work: first
    Unicode CLDR shortcodes (e.g. ``:grinning_face:``), then GitHub-style
    aliases (e.g. ``:grinning:``).

    Args:
        text(str): Text possibly containing ``:emoji:`` shortcodes.

    Returns: str
    """
    try:
        import emoji
    except ImportError:
        return text

    text = emoji.emojize(text, language="en")
    return emoji.emojize(text, language="alias")


# Based on the following SO answer: https://stackoverflow.com/a/16008023/6252525
def _get_approx_string_width(
    text, font_width, fixed_width=False, emoji_font_scale=1.0
) -> int:
    """
    Get the approximate width of a string using a specific average font width.

    Args:
        text(str): Text string to calculate width of.
        font_width(int): Average width of font characters.
        fixed_width(bool): Indicates that the font is fixed width.
        emoji_font_scale(float): Width scale applied to emoji characters,
            used when emoji are rendered at a larger font size than the
            surrounding text.

    Returns:
        int: Width of string in pixels.

    Examples:

        Call the function with a string and the maximum character width of the font you are using:

            >>> int(_get_approx_string_width('hello', 10))
            29

        This example shows the comparison of simplistic calculation based on a fixed width.
        Given a test string and a fixed font width of 10, we can calculate the width
        by multiplying the length and the font character with:

            >>> test_string = 'GOOGLE|ijkl'
            >>> _get_approx_string_width(test_string, 10, fixed_width=True)
            110

        Since some characters in the string are thinner than others we expect that the
        apporximate text width will be narrower than the fixed width calculation:

            >>> _get_approx_string_width(test_string, 10)
            77

    """
    if fixed_width:
        return len(text) * font_width

    size = 0.0

    # A dictionary containing percentages that relate to how wide
    # each character will be represented in a variable width font.
    # These percentages can be calculated using the ``_get_character_percentage_dict`` function.
    char_width_percentages = {
        "lij|' ": 40.0,
        "![]fI.,:;/\\t": 50.0,
        '`-(){}r"': 60.0,
        "*^zcsJkvxy": 70.0,
        "aebdhnopqug#$L+<>=?_~FZT0123456789": 70.0,
        "BSPEAKVXY&UwNRCHD": 70.0,
        "QGOMm%W@": 100.0,
    }

    for s in text:
        percentage = 50.0
        if is_emoji(s):
            percentage = 75.0 * emoji_font_scale
        else:
            for k in char_width_percentages.keys():
                if s in k:
                    percentage = char_width_percentages[k]
                    break
        size += (percentage / 100.0) * float(font_width)

    return int(size)
