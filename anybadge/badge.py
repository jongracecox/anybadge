import os
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Type, Optional, Union

from . import config
from .colors import Color
from .exceptions import UnknownBadgeTemplate

from .helpers import _get_approx_string_width


# Try and obtain packaging package to support version comparison.
from .templates import get_template

from packaging.version import Version


class Badge:
    """
    Badge class used to generate badges.

    Args:
        label(str): Badge label text.
        value(str): Badge value text.
        font_name(str, optional): Name of font to use.
        font_size(int, optional): Font size.
        num_padding_chars(float, optional): Number of padding characters to use to give extra
            space around text.
        num_label_padding_chars(float, optional): Number of padding characters to use to give extra
            space around label text.
        num_value_padding_chars(float, optional): Number of padding characters to use to give extra
            space around value text.
        template(str, optional): String containing the SVG template.  This should be valid SVG
            file content with place holders for variables to be populated during rendering.
        style(str, optional): Style of badge to create. This will make anybadge render a badge in a
            different style. Valid values are "gitlab-scoped", "default". Default is "default".
        value_prefix(str, optional): Prefix to be placed before value.
        value_suffix(str, optional): Suffix to be placed after value.
        thresholds(dict, optional): A dictionary containing thresholds used to select badge
            color based on the badge value.
        default_color(str, optional): Badge color as a name or as an HTML color code.
        use_max_when_value_exceeds(bool, optional): Choose whether to use the maximum threshold
            value when the badge value exceeds the top threshold.  Default is True.
        value_format(str, optional) String with formatting to be used to format the value text.
        text_color(str, optional): Text color as a name or as an HTML color code.
        semver(bool, optional): Used to indicate that the value is a semantic version number.

    Examples:

        Create a simple green badge:

        >>> badge = Badge('label', 123, default_color='green')

        Write a badge to file, overwriting any existing file:

        >>> badge = Badge('label', 123, default_color='green')
        >>> badge.write_badge('demo.svg', overwrite=True)

        Here are a number of examples showing thresholds, since there
        are certain situations that may not be obvious:

        >>> badge = Badge('pipeline', 'passing', thresholds={'passing': 'green', 'failing': 'red'})
        >>> badge.badge_color
        'green'

        2.32 is not <2
        2.32 is < 4, so 2.32 yields orange
        >>> badge = Badge('pylint', 2.32, thresholds={2: 'red',
        ...                                           4: 'orange',
        ...                                           8: 'yellow',
        ...                                           10: 'green'})
        >>> badge.badge_color
        'orange'

        8 is not <8
        8 is <4, so 8 yields orange
        >>> badge = Badge('pylint', 8, thresholds={2: 'red',
        ...                                        4: 'orange',
        ...                                        8: 'yellow',
        ...                                        10: 'green'})
        >>> badge.badge_color
        'green'

        10 is not <8, but use_max_when_value_exceeds defaults to
        True, so 10 yields green
        >>> badge = Badge('pylint', 11, thresholds={2: 'red',
        ...                                         4: 'orange',
        ...                                         8: 'yellow',
        ...                                         10: 'green'})
        >>> badge.badge_color
        'green'

        11 is not <10, and use_max_when_value_exceeds is set to
        False, so 11 yields the default color '#4c1'
        >>> badge = Badge('pylint', 11, use_max_when_value_exceeds=False,
        ...               thresholds={2: 'red', 4: 'orange', 8: 'yellow',
        ...                           10: 'green'})
        >>> badge.badge_color
        '#4c1'
    """

    #: Singleton variable to track current max mask_id. This is used by _get_next_mask_str class method.
    mask_id: int

    def __init__(
        self,
        label,
        value,
        font_name: Optional[str] = None,
        font_size: Optional[int] = None,
        num_padding_chars: Optional[int] = None,
        num_label_padding_chars: Optional[float] = None,
        num_value_padding_chars: Optional[float] = None,
        template: Optional[Union[Path, str]] = None,
        style: Optional[str] = None,
        value_prefix: Optional[str] = "",
        value_suffix: Optional[str] = "",
        thresholds: Optional[Dict[float, str]] = None,
        default_color: Optional[str] = None,
        use_max_when_value_exceeds: Optional[bool] = True,
        value_format: Optional[str] = None,
        text_color: Optional[str] = None,
        semver: Optional[bool] = False,
    ):
        """Constructor for Badge class."""
        # Set defaults if values were not passed
        if not font_name:
            font_name = config.DEFAULT_FONT
        if not font_size:
            font_size = config.DEFAULT_FONT_SIZE
        if num_label_padding_chars is None:
            if num_padding_chars is None:
                num_label_padding_chars = config.NUM_PADDING_CHARS
            else:
                num_label_padding_chars = num_padding_chars
        if num_value_padding_chars is None:
            if num_padding_chars is None:
                num_value_padding_chars = config.NUM_PADDING_CHARS
            else:
                num_value_padding_chars = num_padding_chars
        if isinstance(template, Path):
            template = str(template)
        if not template:
            template = get_template("default")
        if style not in ["gitlab-scoped"]:
            style = "default"
        if not default_color:
            default_color = config.DEFAULT_COLOR
        if not text_color:
            text_color = config.DEFAULT_TEXT_COLOR

        self.label = label
        self.value = value

        if self.label is None:
            self.label = ""
        if self.value is None:
            self.value = ""

        if len(str(self.label)) == 0 and len(str(self.value)) == 0:
            raise ValueError("Either a label or a value must be provided for a badge.")

        self.value_is_version = semver

        self.value_format = value_format
        if value_format:
            value_text = str(value_format % self.value_type(value))
        else:
            value_text = str(self.value_type(value))
        self.value_prefix = value_prefix
        self.value_suffix = value_suffix

        # Combine prefix, value and suffix into a single value_text string

        if value_prefix:
            self.value_text = value_prefix
        else:
            self.value_text = ""

        self.value_text += value_text

        if value_suffix:
            self.value_text += value_suffix

        if font_name not in config.FONT_WIDTHS:
            raise ValueError(
                'Font name "%s" not found. '
                "Available fonts: %s"
                % (font_name, ", ".join(config.FONT_WIDTHS.keys()))
            )
        self.font_name = font_name
        self.font_size = font_size
        self.num_label_padding_chars = num_label_padding_chars
        self.num_value_padding_chars = num_value_padding_chars
        self.template = template
        self.style = style
        self.thresholds = thresholds
        self.default_color = default_color

        # text_color can be passed as a single value or a pair of comma delimited values
        self.text_color = text_color
        text_colors = text_color.split(",")
        self.label_text_color = text_colors[0]
        self.value_text_color = text_colors[0]
        if len(text_colors) > 1:
            self.value_text_color = text_colors[1]

        self.use_max_when_value_exceeds = use_max_when_value_exceeds
        self.mask_str = self.__class__._get_next_mask_str()

    def __repr__(self) -> str:
        """Return a representation of the Badge object instance.

        The output of the __repr__ function could be used to recreate the current object.

        Examples:

            >>> badge = Badge('example', '123.456')
            >>> repr(badge)
            "Badge('example', '123.456')"

            >>> badge = Badge('example', '123.456', value_suffix='TB')
            >>> repr(badge)
            "Badge('example', '123.456', value_suffix='TB')"

            >>> badge = Badge('example', '123.456', text_color='#111111', value_suffix='TB')
            >>> repr(badge)
            "Badge('example', '123.456', value_suffix='TB', text_color='#111111')"

            >>> badge = Badge('example', '123', num_padding_chars=5)
            >>> repr(badge)
            "Badge('example', '123', num_padding_chars=5)"

            >>> badge = Badge('example', '123', num_label_padding_chars=5)
            >>> repr(badge)
            "Badge('example', '123', num_label_padding_chars=5)"

            >>> badge = Badge('example', '123', num_label_padding_chars=5, num_value_padding_chars=6,
            ...               template='template.svg', value_prefix='$', thresholds={10: 'green', 30: 'red'},
            ...               default_color='red', use_max_when_value_exceeds=False, value_format="%s m/s")
            >>> repr(badge)
            "Badge('example', '123', num_label_padding_chars=5, num_value_padding_chars=6, template='template.svg', value_prefix='$', thresholds={10: 'green', 30: 'red'}, default_color='red', use_max_when_value_exceeds=False, value_format='%s m/s')"

        """
        optional_args = ""
        if self.font_name != config.DEFAULT_FONT:
            optional_args += ", font_name=%s" % repr(self.font_name)
        if self.font_size != config.DEFAULT_FONT_SIZE:
            optional_args += ", font_size=%s" % repr(self.font_size)
        if self.num_label_padding_chars == self.num_value_padding_chars:
            if self.num_label_padding_chars != config.NUM_PADDING_CHARS:
                optional_args += ", num_padding_chars=%s" % repr(
                    self.num_label_padding_chars
                )
        else:
            if self.num_label_padding_chars != config.NUM_PADDING_CHARS:
                optional_args += ", num_label_padding_chars=%s" % repr(
                    self.num_label_padding_chars
                )
            if self.num_value_padding_chars != config.NUM_PADDING_CHARS:
                optional_args += ", num_value_padding_chars=%s" % repr(
                    self.num_value_padding_chars
                )
        if self.template != get_template("default"):
            optional_args += ", template=%s" % repr(self.template)
        if self.style != "default":
            optional_args += ", style=%s" % repr(self.style)
        if self.value_prefix != "":
            optional_args += ", value_prefix=%s" % repr(self.value_prefix)
        if self.value_suffix != "":
            optional_args += ", value_suffix=%s" % repr(self.value_suffix)
        if self.thresholds:
            optional_args += ", thresholds=%s" % repr(self.thresholds)
        if self.default_color != config.DEFAULT_COLOR:
            optional_args += ", default_color=%s" % repr(self.default_color)
        if not self.use_max_when_value_exceeds:
            optional_args += ", use_max_when_value_exceeds=%s" % repr(
                self.use_max_when_value_exceeds
            )
        if self.value_format:
            optional_args += ", value_format=%s" % repr(self.value_format)
        if self.text_color != config.DEFAULT_TEXT_COLOR:
            optional_args += ", text_color=%s" % repr(self.text_color)

        return "%s(%s, %s%s)" % (
            self.__class__.__name__,
            repr(self.label),
            repr(self.value),
            optional_args,
        )

    def _repr_svg_(self) -> str:
        """Return SVG representation when used inside Jupyter notebook cells.

        This will render the SVG immediately inside a notebook cell when creating
        a Badge instance without assigning it to an identifier.
        """
        return self.badge_svg_text

    @classmethod
    def _get_next_mask_str(cls) -> str:
        """Return a new mask ID from a singleton sequence maintained on the class.

        Returns: str
        """
        if not hasattr(cls, "mask_id"):
            cls.mask_id = 0

        cls.mask_id += 1

        return config.MASK_ID_PREFIX + str(cls.mask_id)

    def _get_svg_template(self) -> str:
        """Return the correct SVG template to render, based on the style and template
        that have been set

        Returns: str
        """
        if self.style == "gitlab-scoped":
            return get_template("gitlab_scoped")

        # Identify whether template is a file or the actual template text

        if len(self.template.split("\n")) == 1:
            try:
                return get_template(self.template)
            except UnknownBadgeTemplate:
                pass

            with open(self.template, mode="r") as file_handle:
                return file_handle.read()
        else:
            return self.template

    @property
    def semver_version(self) -> Version:
        """The semantic version represented by the value string.

        Returns: Version
        """
        return Version(self.value)

    @property
    def semver_thresholds(self) -> Optional[OrderedDict]:
        """Thresholds as a dict using Version as keys."""
        # Version is not a hashable type, so can't be used to create an
        # ordered dict directly. First we need to create an ordered list of keys
        if not self.thresholds:
            return None

        ordered_keys = sorted(self.thresholds.keys(), key=Version)
        return OrderedDict((key, self.thresholds[key]) for key in ordered_keys)

    @property
    def float_thresholds(self) -> Optional[Dict[float, str]]:
        """Thresholds as a dict using floats as keys."""
        if not self.thresholds:
            return None
        return {float(k): v for k, v in self.thresholds.items()}

    @property
    def value_is_float(self) -> bool:
        """Identify whether the value text is a float.

        Returns: bool
        """

        # If the value is an int then it should not be considered a float.
        # We need to check this first before we check whether it is a float because the
        # float check also returns True for an int string.
        if self.value_is_int:
            return False

        try:
            _ = float(self.value)
        except (ValueError, TypeError):
            return False
        else:
            return True

    @property
    def value_is_int(self) -> bool:
        """Identify whether the value text is an int.

        Returns: bool
        """
        try:
            a = float(self.value)
            b = int(self.value)
        except (ValueError, TypeError):
            return False
        else:
            return a == b

    @property
    def value_type(self) -> Type:
        """The Python type associated with the value.

        Returns: type
        """
        if self.value_is_version:
            return Version
        if self.value_is_float:
            return float
        elif self.value_is_int:
            return int
        else:
            return str

    @property
    def label_width(self) -> int:
        """The SVG width of the label text.

        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │             Value              │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
                 ◀────────▶
                 label_width

        Returns: int
        """
        if len(str(self.label)) == 0:
            return 0

        return int(
            self.get_text_width(str(self.label))
            + (2.0 * self.num_label_padding_chars * self.font_width)
        )

    @property
    def value_width(self) -> int:
        """The SVG width of the value text.

        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │           Value text           │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
                                                ◀────────▶
                                                value_width

        Returns: int
        """
        if len(str(self.value_text)) == 0:
            return 0

        return int(
            self.get_text_width(str(self.value_text))
            + (2.0 * self.num_value_padding_chars * self.font_width)
        )

    @property
    def value_box_width(self) -> int:
        """The SVG width of the value text box.

        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │           Value text           │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
                                    ◀────────────────────────────────▶
                                             value_box_width

        Returns: int
        """
        return self.value_width - 9

    @property
    def font_width(self) -> int:
        """Return the width multiplier for a font.

        Returns:
            int: Maximum pixel width of badges selected font.

        Example:

            >>> Badge(label='x', value='1').font_width
            10
        """
        return config.FONT_WIDTHS[self.font_name][self.font_size]

    @property
    def color_split_position(self) -> int:
        """The SVG x position where the color split should occur.

                                     Split
                                       │
                                    ┌──┘
                                    ▼
        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │           Value text           │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
        ◀───────────────────────────▶
               color_split_pos

        Returns: int
        """
        return self.badge_width - self.value_width

    @property
    def label_anchor(self) -> float:
        """The SVG x position of the middle anchor for the label text.

                    Middle of
                      label
                     ┌──┘
                     ▼
        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │           Value text           │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
        ◀───────────▶
         label_anchor

        Returns: float
        """
        return self.color_split_position / 2

    @property
    def value_anchor(self) -> float:
        """The SVG x position of the middle anchor for the value text.

                                                   Middle of
                                                     value
                                                    ┌──┘
                                                    ▼
        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │           Value text           │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
        ◀──────────────────────────────────────────▶
                                               value_anchor

        Returns: float
        """
        return self.color_split_position + (
            (self.badge_width - self.color_split_position) / 2
        )

    @property
    def label_anchor_shadow(self) -> float:
        """The SVG x position of the label shadow anchor.

        The shadow for the label will appear behind the label.

              ┌ Text ──────────────────┐
              │                        │
              │                        ├────┐
              │                        │    │
              └────┬───────────────────┘    │
                   │                        │
                   └───────────── Shadow ───┘

        The label_anchor_shadow is the distance from left to center of shadow:

        ┌─────────────────────────────┬─────────────────────────────────┐
        │     ┌────────────┐          │                                 │
        │     │            ├─┐        │           Value text            │
        │     └─┬──────────┘ │        │                                 │
        │       └────────────┘        │                                 │
        └─────────────────────────────┴─────────────────────────────────┘
        ◀─────────────▶
        label_anchor_shadow

        Returns: float
        """
        return self.label_anchor + 1

    @property
    def value_anchor_shadow(self) -> float:
        """The SVG x position of the value shadow anchor.

        ┌─────────────────────────────┬─────────────────────────────────┐
        │                             │        ┌────────────┐           │
        │         Label text          │        │            ├─┐         │
        │                             │        └─┬──────────┘ │         │
        │                             │          └────────────┘         │
        └─────────────────────────────┴─────────────────────────────────┘
        ◀───────────────────────────────────────────────▶
                                               value_anchor_shadow
        Returns: float
        """
        return self.value_anchor + 1

    @property
    def badge_width(self) -> int:
        """The total width of badge.

        ┌───────────────────────────┬────────────────────────────────┐
        │                           │                                │
        │        Label text         │           Value text           │
        │                           │                                │
        └───────────────────────────┴────────────────────────────────┘
        ◀───────────────────────────────────────────────────────────▶
                                 badge_width

        Returns: int

        Examples:

            >>> badge = Badge('pylint', '5')
            >>> badge.badge_width
            61
        """
        return self.label_width + self.value_width

    @property
    def arc_start(self) -> int:
        """The position where the arc on the arc should start.

        Returns: int

        Examples:

            >>> badge = Badge('pylint', '5')
            >>> badge.arc_start
            51
        """
        return self.badge_width - 10

    @property
    def badge_svg_text(self) -> str:
        """The badge SVG text.

        Returns: str
        """

        badge_text = self._get_svg_template()

        return (
            badge_text.replace("{{ badge width }}", str(self.badge_width))
            .replace("{{ font name }}", self.font_name)
            .replace("{{ font size }}", str(self.font_size))
            .replace("{{ label }}", self.label)
            .replace("{{ value }}", self.value_text)
            .replace("{{ label anchor }}", str(self.label_anchor))
            .replace("{{ label anchor shadow }}", str(self.label_anchor_shadow))
            .replace("{{ value anchor }}", str(self.value_anchor))
            .replace("{{ value anchor shadow }}", str(self.value_anchor_shadow))
            .replace("{{ color }}", self.badge_color_code)
            .replace("{{ label text color }}", self.label_text_color)
            .replace("{{ value text color }}", self.value_text_color)
            .replace("{{ color split x }}", str(self.color_split_position))
            .replace("{{ value width }}", str(self.value_width))
            .replace("{{ mask id }}", self.mask_str)
            .replace("{{ value box width }}", str(self.value_box_width))
            .replace("{{ arc start }}", str(self.arc_start))
        )

    def __str__(self) -> str:
        """Return string representation of badge.

        This will return the badge SVG text.

        Returns: str

        Examples:

            >>> print(Badge('example', '123'))  # doctest: +ELLIPSIS
            <?xml version="1.0" encoding="UTF-8"?>
            ...
        """
        return self.badge_svg_text

    def get_text_width(self, text) -> int:
        """Return the width of text.

        Args:
            text(str): Text to get the pixel width of.

        Returns:
            int: Pixel width of the given text based on the badges selected font.

        This implementation assumes a fixed font of:

        font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11"
        >>> badge = Badge('x', 1, font_name='DejaVu Sans,Verdana,Geneva,sans-serif', font_size=11)
        >>> badge.get_text_width('pylint')
        34
        """
        return _get_approx_string_width(text, self.font_width)

    @property
    def badge_color(self) -> str:
        """Badge color based on the configured thresholds.

        Returns: str"""
        # If no thresholds were passed then return the default color
        if not self.thresholds:
            return self.default_color

        if self.value_type == str:
            if self.value in self.thresholds:
                return self.thresholds[self.value]
            else:
                return self.default_color

        thresholds: Optional[Union[Dict[float, str], OrderedDict[float, str]]]

        # Set value and thresholds based on the value type. This will result in either
        # value and thresholds as floats or value and thresholds as semantic versions.
        if self.value_type == Version:
            value = self.semver_version
            thresholds = self.semver_thresholds
        else:
            value = float(self.value)
            thresholds = self.float_thresholds

        color = None

        if thresholds:

            # Convert the threshold dictionary into a sorted list of lists
            threshold_list = [[self.value_type(i[0]), i[1]] for i in thresholds.items()]
            threshold_list.sort(key=lambda x: x[0])

            for threshold, color in threshold_list:
                if value < threshold:
                    return color

        # If we drop out the top of the range then return the last max color
        if color and self.use_max_when_value_exceeds:
            return color
        else:
            return self.default_color

    @property
    def badge_color_code(self) -> str:
        """Return the color code for the badge.

        Returns: str

        Raises: ValueError when an invalid badge color is set.
        """
        color = self.badge_color

        if isinstance(color, Color):
            return color.value

        if color[0] == "#":
            return color

        color = color.upper()

        prefixes = ["BRIGHT", "YELLOW", "LIGHT"]

        try:
            return Color[color.upper()].value
        except KeyError:
            pass

        # For backward compatibility with old color names (that were lowercase and didn't
        # contain underscores) we will try to get the same color.

        for prefix in prefixes:
            if color.startswith(prefix) and color != prefix and "_" not in color:
                try:
                    return Color[color.replace(prefix, prefix + "_")].value
                except KeyError:
                    pass

        raise ValueError(
            'Invalid color code "%s". ' "Valid color codes are: %s",
            (color, ", ".join(list(Color.__members__.keys()))),
        )

    def write_badge(self, file_path: Union[str, Path], overwrite=False) -> None:
        """Write badge to file."""

        if isinstance(file_path, str):

            if file_path.endswith("/"):
                raise ValueError("File location may not be a directory.")

            file: Path = Path(file_path)
        else:
            file = file_path

        # Validate path (part 1)
        if file.is_dir():
            raise ValueError("File location may not be a directory.")

        # Ensure we're using a .svg extension
        file = file.with_suffix(".svg")

        # Validate path (part 2)
        if not overwrite and file.exists():
            raise RuntimeError('File "{}" already exists.'.format(file))

        with open(file, mode="w") as file_handle:
            file_handle.write(self.badge_svg_text)
