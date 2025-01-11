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
    return bool(EMOJI_REGEX.match(character))


# Based on the following SO answer: https://stackoverflow.com/a/16008023/6252525
def _get_approx_string_width(text, font_width, fixed_width=False) -> int:
    """
    Get the approximate width of a string using a specific average font width.

    Args:
        text(str): Text string to calculate width of.
        font_width(int): Average width of font characters.
        fixed_width(bool): Indicates that the font is fixed width.

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
            percentage = 75.0
        else:
            for k in char_width_percentages.keys():
                if s in k:
                    percentage = char_width_percentages[k]
                    break
        size += (percentage / 100.0) * float(font_width)

    return int(size)
