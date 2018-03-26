#!/usr/bin/python
"""
anybadge

A Python module for generating badges for your projects, with a focus on
simplicity and flexibility.
"""
import os
import re

# Package information
version = __version__ = "0.1.0.dev2"
__version_info__ = tuple(re.split('[.-]', __version__))
__title__ = "anybadge"
__summary__ = "A simple, flexible badge generator."
__uri__ = "https://github.com/jongracecox/anybadge"


# Set some defaults
DEFAULT_FONT = 'DejaVu Sans,Verdana,Geneva,sans-serif'
DEFAULT_FONT_SIZE = 11
NUM_PADDING_CHARS = 0.5
DEFAULT_COLOR = '#4c1'
DEFAULT_TEXT_COLOR = '#fff'

# Dictionary for looking up approx pixel widths of
# supported fonts and font sizes.
FONT_WIDTHS = {
    'DejaVu Sans,Verdana,Geneva,sans-serif': {
        11: 7
    }
}

# Create a dictionary of colors to make selections
# easier.
COLORS = {
    'green': '#4c1',
    'yellowgreen': '#a4a61d',
    'yellow': '#dfb317',
    'orange': '#fe7d37',
    'red': '#e05d44',
    'lightgrey': '#9f9f9f',
}

# Template SVG with placeholders for various items that
# will be added during final creation.
TEMPLATE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{{ badge width }}" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="{{ badge width }}" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h{{ color split x }}v20H0z"/>
        <path fill="{{ color }}" d="M{{ color split x }} 0h{{ value width }}v20H{{ color split x }}z"/>
        <path fill="url(#b)" d="M0 0h{{ badge width }}v20H0z"/>
    </g>
    <g fill="{{ label text color }}" text-anchor="middle" font-family="{{ font name }}" font-size="{{ font size }}">
        <text x="{{ label anchor shadow }}" y="15" fill="#010101" fill-opacity=".3">{{ label }}</text>
        <text x="{{ label anchor }}" y="14">{{ label }}</text>
    </g>
    <g fill="{{ value text color }}" text-anchor="middle" font-family="{{ font name }}" font-size="{{ font size }}">
        <text x="{{ value anchor shadow }}" y="15" fill="#010101" fill-opacity=".3">{{ value }}</text>
        <text x="{{ value anchor }}" y="14">{{ value }}</text>
    </g>
</svg>"""

# Define some templates that can be used for common badge types, saving
# from having to provide thresholds and labels each time.
BADGE_TEMPLATES = {
    'pylint': {
        'threshold': '2=red 4=orange 8=yellow 10=green',
        'label': 'pylint'
    },
    'coverage': {
        'threshold': '50=red 60=orange 80=yellow 100=green',
        'label': 'coverage',
        'suffix': '%'
    }
}


class Badge(object):
    """
    Badge class used to generate badges.

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

    def __init__(self, label, value, font_name=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE,
                 num_padding_chars=NUM_PADDING_CHARS, template=TEMPLATE_SVG,
                 value_prefix='', value_suffix='', thresholds=None, default_color=DEFAULT_COLOR,
                 use_max_when_value_exceeds=True, value_format=None, text_color=DEFAULT_TEXT_COLOR):
        """Constructor for Badge class."""
        self.label = label
        self.value = value
        if value_format:
            value_text = str(value_format % self.value_type(value))
        else:
            value_text = str(self.value_type(value))
        self.value_text = value_prefix + value_text + value_suffix
        self.font_name = font_name
        self.font_size = font_size
        self.num_padding_chars = num_padding_chars
        self.template = template
        self.thresholds = thresholds
        self.default_color = default_color

        # text_color can be passed as a single value or a pair of comma delimited values
        text_colors = text_color.split(',')
        self.label_text_color = text_colors[0]
        self.value_text_color = text_colors[0]
        if len(text_colors) > 1:
            self.value_text_color = text_colors[1]

        self.use_max_when_value_exceeds = use_max_when_value_exceeds

    @property
    def value_is_float(self):
        """Identify whether the value text is a float."""
        try:
            _ = float(self.value)
        except ValueError:
            return False
        else:
            return True

    @property
    def value_is_int(self):
        """Identify whether the value text is an int."""
        try:
            a = float(self.value)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b

    @property
    def value_type(self):
        """The Python type associated with the value."""
        if self.value_is_float:
            return float
        elif self.value_is_int:
            return int
        else:
            return str

    @property
    def label_width(self):
        """The SVG width of the label text."""
        return self.get_text_width(self.label)

    @property
    def value_width(self):
        """The SVG width of the value text."""
        return self.get_text_width(str(self.value_text))

    @property
    def font_width(self):
        """Return the badge font width."""
        return self.get_font_width(font_name=self.font_name, font_size=self.font_size)

    @property
    def color_split_position(self):
        """The SVG x position where the color split should occur."""
        return self.get_text_width(' ') + self.label_width + \
            int(float(self.font_width) * float(self.num_padding_chars))

    @property
    def label_anchor(self):
        """The SVG x position of the middle anchor for the label text."""
        return self.color_split_position / 2

    @property
    def value_anchor(self):
        """The SVG x position of the middle anchor for the value text."""
        return self.color_split_position + ((self.badge_width - self.color_split_position) / 2)

    @property
    def label_anchor_shadow(self):
        """The SVG x position of the label shadow anchor."""
        return self.label_anchor + 1

    @property
    def value_anchor_shadow(self):
        """The SVG x position of the value shadow anchor."""
        return self.value_anchor + 1

    @property
    def badge_width(self):
        """The total width of badge.

        >>> badge = Badge('pylint', '5', font_name='DejaVu Sans,Verdana,Geneva,sans-serif',
        ...               font_size=11)
        >>> badge.badge_width
        91
        """
        return self.get_text_width('   ' + ' ' * int(float(self.num_padding_chars) * 2.0)) \
            + self.label_width + self.value_width

    @property
    def badge_svg_text(self):
        """The badge SVG text."""

        # Identify whether template is a file or the actual template text
        if len(self.template.split('\n')) == 1:
            with open(self.template, mode='r') as file_handle:
                badge_text = file_handle.read()
        else:
            badge_text = self.template

        return badge_text.replace('{{ badge width }}', str(self.badge_width)) \
            .replace('{{ font name }}', self.font_name) \
            .replace('{{ font size }}', str(self.font_size)) \
            .replace('{{ label }}', self.label) \
            .replace('{{ value }}', self.value_text) \
            .replace('{{ label anchor }}', str(self.label_anchor)) \
            .replace('{{ label anchor shadow }}', str(self.label_anchor_shadow)) \
            .replace('{{ value anchor }}', str(self.value_anchor)) \
            .replace('{{ value anchor shadow }}', str(self.value_anchor_shadow)) \
            .replace('{{ color }}', self.badge_color_code) \
            .replace('{{ label text color }}', self.label_text_color) \
            .replace('{{ value text color }}', self.value_text_color) \
            .replace('{{ color split x }}', str(self.color_split_position)) \
            .replace('{{ value width }}', str(self.badge_width - self.color_split_position))

    @staticmethod
    def get_font_width(font_name, font_size):
        """Return the width multiplier for a font.

        >>> Badge.get_font_width('DejaVu Sans,Verdana,Geneva,sans-serif', 11)
        7
        """
        return FONT_WIDTHS[font_name][font_size]

    def get_text_width(self, text):
        """Return the width of text.

        This implementation assumes a fixed font of:

        font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11"
        >>> badge = Badge('x', 1, font_name='DejaVu Sans,Verdana,Geneva,sans-serif', font_size=11)
        >>> badge.get_text_width('pylint')
        42
        """
        return len(text) * self.get_font_width(self.font_name, self.font_size)

    @property
    def badge_color(self):
        """Find the badge color based on the thresholds."""
        # If no thresholds were passed then return the default color
        if not self.thresholds:
            return self.default_color

        if self.value_type == str:
            if self.value in self.thresholds:
                return self.thresholds[self.value]
            else:
                return self.default_color

        # Convert the threshold dictionary into a sorted list of lists
        threshold_list = [[self.value_type(i[0]), i[1]] for i in self.thresholds.items()]
        threshold_list.sort(key=lambda x: x[0])

        color = None

        for threshold, color in threshold_list:
            if float(self.value) < float(threshold):
                return color

        # If we drop out the top of the range then return the last max color
        if color and self.use_max_when_value_exceeds:
            return color
        else:
            return self.default_color

    @property
    def badge_color_code(self):
        """Return the color code for the badge."""
        color = self.badge_color
        if color[0] == '#':
            return color
        return COLORS[color]

    def write_badge(self, file_path, overwrite=False):
        """Write badge to file."""

        # Validate path (part 1)
        if file_path.endswith('/'):
            raise Exception('File location may not be a directory.')

        # Get absolute filepath
        path = os.path.abspath(file_path)
        if not path.lower().endswith('.svg'):
            path += '.svg'

        # Validate path (part 2)
        if not overwrite and os.path.exists(path):
            raise Exception('File "{}" already exists.'.format(path))

        with open(path, mode='w') as file_handle:
            file_handle.write(self.badge_svg_text)


def parse_args():
    """Parse the command line arguments."""
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
Command line utility to generate .svg badges.

This utility can be used to generate .svg badge images, using configurable
thresholds for coloring.  Values can be passed as string, integer or floating
point.  The type will be detected automatically.

Running the utility with a --file option will result in the .svg image being
written to file.  Without the --file option the .svg file content will be
written to stdout, so can be redirected to a file.

Some thresholds have been built in to save time.  To use these thresholds you
can simply specify the template name instead of threshold value/color pairs.

examples:

    Here are some usage specific examples that may save time on defining
    thresholds.

    Pylint
        anybadge.py --value=2.22 --file=pylint.svg pylint

        anybadge.py --label=pylint --value=2.22 --file=pylint.svg \\
          2=red 4=orange 8=yellow 10=green

    Coverage
        anybadge.py --value=65 --file=coverage.svg coverage

        anybadge.py --label=coverage --value=65 --suffix='%%' --file=coverage.svg \\
          50=red 60=orange 80=yellow 100=green

    CI Pipeline
        anybadge.py --label=pipeline --value=passing --file=pipeline.svg \\
          passing=green failing=red

'''))
    parser.add_argument('-l', '--label', type=str, help='The badge label.')
    parser.add_argument('-v', '--value', type=str, help='The badge value.', required=True)
    parser.add_argument('-m', '--value-format', type=str, default=None,
                        help='Formatting string for value (e.g. "%%.2f" for 2dp floats)')
    parser.add_argument('-c', '--color', type=str, help='For fixed color badges use --color'
                                                        'to specify the badge color.',
                        default=DEFAULT_COLOR)
    parser.add_argument('-p', '--prefix', type=str, help='Optional prefix for value.',
                        default='')
    parser.add_argument('-s', '--suffix', type=str, help='Optional suffix for value.',
                        default='')
    parser.add_argument('-d', '--padding', type=int, help='Number of characters to pad on '
                                                          'either side of the badge text.',
                        default=NUM_PADDING_CHARS)
    parser.add_argument('-n', '--font', type=str,
                        help='Font name.  Supported fonts: '
                             ','.join(['"%s"' % x for x in FONT_WIDTHS.keys()]),
                        default=DEFAULT_FONT)
    parser.add_argument('-z', '--font-size', type=int, help='Font size.',
                        default=DEFAULT_FONT_SIZE)
    parser.add_argument('-t', '--template', type=str, help='Location of alternative '
                                                           'template .svg file.',
                        default=TEMPLATE_SVG)
    parser.add_argument('-u', '--use-max', action='store_true',
                        help='Use the maximum threshold color when the value exceeds the '
                             'maximum threshold.')
    parser.add_argument('-f', '--file', type=str, help='Output file location.')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Overwrite output file if it already exists.')
    parser.add_argument('-r', '--text-color', type=str, help='Text color. Single value affects both label'
                                                             'and value colors.  A comma separated pair '
                                                             'affects label and value text respectively.',
                        default=DEFAULT_TEXT_COLOR)
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Pairs of <upper>=<color>. '
                        'For example 2=red 4=orange 6=yellow 8=good. '
                        'Read this as "Less than 2 = red, less than 4 = orange...".')
    return parser.parse_args()


def main():
    """Generate a badge based on command line arguments."""
    # Parse command line arguments
    args = parse_args()

    label = args.label
    threshold_text = args.args
    suffix = args.suffix

    # Check whether thresholds were sent as one word, and is in the
    # list of templates.  If so, swap in the template.
    if len(args.args) == 1 and args.args[0] in BADGE_TEMPLATES:
        template_name = args.args[0]
        template_dict = BADGE_TEMPLATES[template_name]
        threshold_text = template_dict['threshold'].split(' ')
        if not args.label:
            label = template_dict['label']
        if not args.suffix and 'suffix' in template_dict:
            suffix = template_dict['suffix']

    if not label:
        raise ValueError('Label has not been set.  Please use --label argument.')

    # Create threshold list from args
    threshold_list = [x.split('=') for x in threshold_text]
    threshold_dict = {x[0]: x[1] for x in threshold_list}

    # Create badge object
    badge = Badge(label, args.value, value_prefix=args.prefix, value_suffix=suffix,
                  default_color=args.color, num_padding_chars=args.padding, font_name=args.font,
                  font_size=args.font_size, template=args.template,
                  use_max_when_value_exceeds=args.use_max, thresholds=threshold_dict,
                  value_format=args.value_format, text_color=args.text_color)

    if args.file:
        # Write badge SVG to file
        badge.write_badge(args.file, overwrite=args.overwrite)
    else:
        print(badge.badge_svg_text)

if __name__ == '__main__':
    main()
