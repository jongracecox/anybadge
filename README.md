# anybadge

Python project for generating badges for your projects

[![pypi package](https://badge.fury.io/py/anybadge.svg)](https://pypi.org/project/anybadge)
[![build status](https://api.travis-ci.org/jongracecox/anybadge.svg?branch=master)](https://travis-ci.org/jongracecox/anybadge)
[![downloads](https://img.shields.io/pypi/dm/anybadge.svg)](https://pypistats.org/packages/anybadge)
[![GitHub last commit](https://img.shields.io/github/last-commit/jongracecox/anybadge.svg)](https://github.com/jongracecox/anybadge/commits/master)
[![GitHub](https://img.shields.io/github/license/jongracecox/anybadge.svg)](https://github.com/jongracecox/anybadge/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jongracecox/anybadge.svg?style=social)](https://github.com/jongracecox/anybadge/stargazers)

[![buymeacoffee](https://camo.githubusercontent.com/c3f856bacd5b09669157ed4774f80fb9d8622dd45ce8fdf2990d3552db99bd27/68747470733a2f2f7777772e6275796d6561636f666665652e636f6d2f6173736574732f696d672f637573746f6d5f696d616765732f6f72616e67655f696d672e706e67)](https://www.buymeacoffee.com/jongracecox)

## Overview

`anybadge` can be used to add badge generation to your Python projects,
and also provides a command line interface.

This utility can be used to generate .svg badge images, using configurable
thresholds for coloring the badges based on the badge value.  Many badge
generation tools just provide the ability to specify the color of badge.
`anybadge` allows you to specify the label, badge value, and color, but
it also allows you to specify a set of thresholds that can be used to
select a color based on the badge value.

`anybadge` may be useful for companies developing internally, or any time
making calls to external badge services is not possible, or undesirable.
In this situation using `anybadge` will be easier than running your own
internal badge service.

The package can be imported into your python code, or run direct from the
command line.

## Demo

You can find a [repl.it demo here](https://repl.it/@JonGrace_Cox/anybadge-demo).
This will allow you to see what the package can do and play with it to test outputs.

## Basic usage

### Command line

As an example, if you want to produce a pylint badge, you may run `anybadge`
from the command line like this:

```bash
anybadge -l pylint -v 2.22 -f pylint.svg 2=red 4=orange 8=yellow 10=green
```

This would result in a badge like this:

![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pylint.svg)

In this example the label is set to "pylint", the value "2.22", and an
output file called "pylint.svg".  The thresholds are provided in pairs
of `<value>=color`  Values can be integer or floats for ranges, and
string values are also supported.

### Python

Here is the same example implemented in Python code:

```python
import anybadge

# Define thresholds: <2=red, <4=orange <8=yellow <10=green
thresholds = {2: 'red',
              4: 'orange',
              6: 'yellow',
              10: 'green'}

badge = anybadge.Badge('pylint', 2.22, thresholds=thresholds)

badge.write_badge('pylint.svg')
```

## Installation

`anybadge` is available in PyPi at https://pypi.python.org/pypi/anybadge

You can install the latest release of `anybadge` using `pip`:

```bash
pip install anybadge
```

This will install the Python package, and also make `anybadge` available
as a command line utility.

## Getting help

To get help from the command line utility, just run:

```bash
anybadge --help
```

## Command line usage

### Output

Running the utility with the `--file` option will result in the .svg image being
written to file.  Without the `--file` option the `.svg` file content will be
written to stdout, so can be redirected to a file.

### Thresholds

Some thresholds have been built in to save time.  To use these thresholds you
can simply specify the template name instead of threshold value/color pairs.

```bash
anybadge --value=<VALUE> --file=<FILE> <TEMPLATE-NAME>
```

For example:

```bash
anybadge --value=2.22 --file=pylint.svg pylint
```

### Colors

Anybadge comes with some pre-defined colors, which can be referred to by name.  It also
supports the use of custom colors by using the hex representation of the color.  Both color
types can be used in the `default_color`, `text_color` and `thresholds` attributes.

Here is a Python example showing use of a named color and a custom color.

```python
import anybadge

badge = anybadge.Badge(label='custom color', value='teal', default_color='teal', num_padding_chars=1)
badge = anybadge.Badge(label='custom color', value='teal', default_color='#008080', num_padding_chars=1)
```

Available named colors are:

| Color Name | Hex Code | Example |
| ---------- | -------- | ------- |
| aqua | #00FFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_aqua.svg) |
| black | #000000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_black.svg) |
| blue | #0000FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_blue.svg) |
| brightred | #FF0000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_brightred.svg) |
| brightyellow | #FFFF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_brightyellow.svg) |
| fuchsia | #FF00FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_fuchsia.svg) |
| gray | #808080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_gray.svg) |
| green | #4C1 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_green.svg) |
| lightgrey | #9F9F9F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightgrey.svg) |
| lime | #00FF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lime.svg) |
| maroon | #800000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_maroon.svg) |
| navy | #000080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_navy.svg) |
| olive | #808000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_olive.svg) |
| orange | #FE7D37 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_orange.svg) |
| purple | #800080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_purple.svg) |
| red | #E05D44 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_red.svg) |
| silver | #C0C0C0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_silver.svg) |
| teal | #008080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_teal.svg) |
| white | #FFFFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_white.svg) |
| yellow | #DFB317 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellow.svg) |
| yellowgreen | #A4A61D | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellowgreen.svg) |

This table was generated with the following code:

```python
print("""| Color Name | Hex Code | Example |
| ---------- | -------- | ------- |""")
for color, hex in sorted(anybadge.COLORS.items()):
    file = 'examples/color_' + color + '.svg'
    url = 'https://cdn.rawgit.com/jongracecox/anybadge/master/' + file
    anybadge.Badge(label='Color', value=color, default_color=color).write_badge(file, overwrite=True)
    print("| {color} | {hex} | ![]({url}) |".format(color=color, hex=hex.upper(), url=url))
```

### Semantic version support

Anybadge supports semantic versions for value and threshold keys. This supports color-coded
badges based on version numbering. Here are some examples:

```python
badge = Badge(
    label='Version',
    value='3.0.0',
    thresholds={'3.0.0': 'red', '3.2.0': 'orange', '999.0.0': 'green'},
    semver=True
)
```

In the above example the thresholds equate to the following:

* If value is < 3.0.0 then badge will be red.
* If value is < 3.2.0 then badge will be orange.
* If value is < 999.0.0 then badge will be green.

Each threshold entry is used to define the upper bounds of the threshold. If you don't know the
upper bound for your version number threshold you will need to provide an extreme upper bound -
in this example it is `999.0.0`.

### Examples

#### Pylint using template
```bash
anybadge --value=2.22 --file=pylint.svg pylint
```
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pylint.svg)

#### Pylint using arguments
```bash
anybadge -l pylint -v 2.22 -f pylint.svg 2=red 4=orange 8=yellow 10=green
```
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pylint.svg)

#### Coverage using template
```bash
anybadge --value=65 --file=coverage.svg coverage
```
![coverage](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/coverage.svg)

#### Pipeline, using labeled colors
```bash
anybadge --label=pipeline --value=passing --file=pipeline.svg passing=green failing=red
```
![pipeline](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pipeline.svg)

#### Badge with fixed color
```bash
anybadge --label=awesomeness --value="110%" --file=awesomeness.svg --color='#97CA00'
```
![awesomeness](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/awesomeness.svg)

#### GitLab Scoped style badge
```bash
anybadge --style=gitlab-scoped --label=Project --value=Archimedes --file=gitlab_scoped.svg --color='#c1115d'
```
![gitlab_scoped](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/gitlab_scoped.svg)

#### Thresholds based on semantic versions
```bash
anybadge --label=Version --value=2.4.5 --file=version.svg 1.0.0=red 2.4.6=orange 2.9.1=yellow 999.0.0=green
```

#### Importing in your own app
```python
from anybadge import Badge

test1 = Badge(
    label,
    value,
    font_name='DejaVu Sans,Verdana,Geneva,sans-serif',
    font_size=11,
    num_padding_chars=0.5,
    template='<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{{ badge width }}" height="20">\n    <linearGradient id="b" x2="0" y2="100%">\n        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>\n        <stop offset="1" stop-opacity=".1"/>\n    </linearGradient>\n    <mask id="a">\n        <rect width="{{ badge width }}" height="20" rx="3" fill="#fff"/>\n    </mask>\n    <g mask="url(#a)">\n        <path fill="#555" d="M0 0h{{ color split x }}v20H0z"/>\n        <path fill="{{ color }}" d="M{{ color split x }} 0h{{ value width }}v20H{{ color split x }}z"/>\n        <path fill="url(#b)" d="M0 0h{{ badge width }}v20H0z"/>\n    </g>\n    <g fill="{{ label text color }}" text-anchor="middle" font-family="{{ font name }}" font-size="{{ font size }}">\n        <text x="{{ label anchor shadow }}" y="15" fill="#010101" fill-opacity=".3">{{ label }}</text>\n        <text x="{{ label anchor }}" y="14">{{ label }}</text>\n    </g>\n    <g fill="{{ value text color }}" text-anchor="middle" font-family="{{ font name }}" font-size="{{ font size }}">\n        <text x="{{ value anchor shadow }}" y="15" fill="#010101" fill-opacity=".3">{{ value }}</text>\n        <text x="{{ value anchor }}" y="14">{{ value }}</text>\n    </g>\n</svg>',
    value_prefix='',
    value_suffix='',
    thresholds=None,
    default_color='#4c1',
    use_max_when_value_exceeds=True,
    value_format=None,
    text_color='#fff'
)

test1.write_badge('test1.svg')
```

### Options

These are the command line options:

```
positional arguments:
  args                  Pairs of <upper>=<color>. For example 2=red 4=orange
                        6=yellow 8=good. Read this as "Less than 2 = red, less
                        than 4 = orange...".

optional arguments:
  -h, --help            show this help message and exit
  -l LABEL, --label LABEL
                        The badge label.
  -v VALUE, --value VALUE
                        The badge value.
  -m VALUE_FORMAT, --value-format VALUE_FORMAT
                        Formatting string for value (e.g. "%.2f" for 2dp
                        floats)
  -c COLOR, --color COLOR
                        For fixed color badges use --colorto specify the badge
                        color.
  -p PREFIX, --prefix PREFIX
                        Optional prefix for value.
  -s SUFFIX, --suffix SUFFIX
                        Optional suffix for value.
  -d PADDING, --padding PADDING
                        Number of characters to pad on either side of the
                        badge text.
  -lp LABEL_PADDING, --label-padding LABEL_PADDING
                        Number of characters to pad on either side of the
                        badge label.
  -vp VALUE_PADDING, --value-padding VALUE_PADDING
                        Number of characters to pad on either side of the
                        badge value.
  -n FONT, --font FONT  "DejaVu Sans,Verdana,Geneva,sans-serif"Font name.
                        Supported fonts: ,"Arial, Helvetica, sans-serif"
  -z FONT_SIZE, --font-size FONT_SIZE
                        Font size.
  -t TEMPLATE, --template TEMPLATE
                        Location of alternative template .svg file.
  -s STYLE, --style STYLE
                        Alternative style of badge to create. Valid values are
                        "gitlab-scoped", "default". This overrides any templates
                        passed using --template.
  -u, --use-max         Use the maximum threshold color when the value exceeds
                        the maximum threshold.
  -f FILE, --file FILE  Output file location.
  -o, --overwrite       Overwrite output file if it already exists.
  -r TEXT_COLOR, --text-color TEXT_COLOR
                        Text color. Single value affects both labeland value
                        colors. A comma separated pair affects label and value
                        text respectively.
```

Examples
--------

Here are some usage specific command line examples that may save time on defining
thresholds.

Pylint::

```
anybadge.py --value=2.22 --file=pylint.svg pylint
anybadge.py --label=pylint --value=2.22 --file=pylint.svg 2=red 4=orange 8=yellow 10=green
```

Coverage::

```
anybadge.py --value=65 --file=coverage.svg coverage
anybadge.py --label=coverage --value=65 --suffix='%%' --file=coverage.svg 50=red 60=orange 80=yellow 100=green
```

CI Pipeline::

```
anybadge.py --label=pipeline --value=passing --file=pipeline.svg passing=green failing=red
```

Python usage
============
Here is the output of ``help(anybadge)``::

```
Help on module anybadge:

NAME
    anybadge - anybadge

DESCRIPTION
    A Python module for generating badges for your projects, with a focus on
    simplicity and flexibility.

CLASSES
    builtins.object
        Badge

    class Badge(builtins.object)
     |  Badge(label, value, font_name=None, font_size=None, num_padding_chars=None, num_label_padding_chars=None, num_value_padding_chars=None, template=None, style=None, value_prefix='', value_suffix='', thresholds=None, default_color=None, use_max_when_value_exceeds=True, value_format=None, text_color=None, semver=False)
     |
     |  Badge class used to generate badges.
     |
     |  Args:
     |      label(str): Badge label text.
     |      value(str): Badge value text.
     |      font_name(str, optional): Name of font to use.
     |      font_size(int, optional): Font size.
     |      num_padding_chars(float, optional): Number of padding characters to use to give extra
     |          space around text.
     |      num_label_padding_chars(float, optional): Number of padding characters to use to give extra
     |          space around label text.
     |      num_value_padding_chars(float, optional): Number of padding characters to use to give extra
     |          space around value text.
     |      template(str, optional): String containing the SVG template.  This should be valid SVG
     |          file content with place holders for variables to be populated during rendering.
     |      style(str, optional): Style of badge to create. This will make anybadge render a badge in a
     |          different style. Valid values are "gitlab-scoped", "default". Default is "default".
     |      value_prefix(str, optional): Prefix to be placed before value.
     |      value_suffix(str, optional): Suffix to be placed after value.
     |      thresholds(dict, optional): A dictionary containing thresholds used to select badge
     |          color based on the badge value.
     |      default_color(str, optional): Badge color as a name or as an HTML color code.
     |      use_max_when_value_exceeds(bool, optional): Choose whether to use the maximum threshold
     |          value when the badge value exceeds the top threshold.  Default is True.
     |      value_format(str, optional) String with formatting to be used to format the value text.
     |      text_color(str, optional): Text color as a name or as an HTML color code.
     |      semver(bool, optional): Used to indicate that the value is a semantic version number.
     |
     |  Examples:
     |
     |      Create a simple green badge:
     |
     |      >>> badge = Badge('label', 123, default_color='green')
     |
     |      Write a badge to file, overwriting any existing file:
     |
     |      >>> badge = Badge('label', 123, default_color='green')
     |      >>> badge.write_badge('demo.svg', overwrite=True)
     |
     |      Here are a number of examples showing thresholds, since there
     |      are certain situations that may not be obvious:
     |
     |      >>> badge = Badge('pipeline', 'passing', thresholds={'passing': 'green', 'failing': 'red'})
     |      >>> badge.badge_color
     |      'green'
     |
     |      2.32 is not <2
     |      2.32 is < 4, so 2.32 yields orange
     |      >>> badge = Badge('pylint', 2.32, thresholds={2: 'red',
     |      ...                                           4: 'orange',
     |      ...                                           8: 'yellow',
     |      ...                                           10: 'green'})
     |      >>> badge.badge_color
     |      'orange'
     |
     |      8 is not <8
     |      8 is <4, so 8 yields orange
     |      >>> badge = Badge('pylint', 8, thresholds={2: 'red',
     |      ...                                        4: 'orange',
     |      ...                                        8: 'yellow',
     |      ...                                        10: 'green'})
     |      >>> badge.badge_color
     |      'green'
     |
     |      10 is not <8, but use_max_when_value_exceeds defaults to
     |      True, so 10 yields green
     |      >>> badge = Badge('pylint', 11, thresholds={2: 'red',
     |      ...                                         4: 'orange',
     |      ...                                         8: 'yellow',
     |      ...                                         10: 'green'})
     |      >>> badge.badge_color
     |      'green'
     |
     |      11 is not <10, and use_max_when_value_exceeds is set to
     |      False, so 11 yields the default color '#4c1'
     |      >>> badge = Badge('pylint', 11, use_max_when_value_exceeds=False,
     |      ...               thresholds={2: 'red', 4: 'orange', 8: 'yellow',
     |      ...                           10: 'green'})
     |      >>> badge.badge_color
     |      '#4c1'
     |
     |  Methods defined here:
     |
     |  __init__(self, label, value, font_name=None, font_size=None, num_padding_chars=None, num_label_padding_chars=None, num_value_padding_chars=None, template=None, style=None, value_prefix='', value_suffix='', thresholds=None, default_color=None, use_max_when_value_exceeds=True, value_format=None, text_color=None, semver=False)
     |      Constructor for Badge class.
     |
     |  __repr__(self)
     |      Return a representation of the Badge object instance.
     |
     |      The output of the __repr__ function could be used to recreate the current object.
     |
     |      Examples:
     |
     |          >>> badge = Badge('example', '123.456')
     |          >>> repr(badge)
     |          "Badge('example', '123.456')"
     |
     |          >>> badge = Badge('example', '123.456', value_suffix='TB')
     |          >>> repr(badge)
     |          "Badge('example', '123.456', value_suffix='TB')"
     |
     |          >>> badge = Badge('example', '123.456', text_color='#111111', value_suffix='TB')
     |          >>> repr(badge)
     |          "Badge('example', '123.456', value_suffix='TB', text_color='#111111')"
     |
     |          >>> badge = Badge('example', '123', num_padding_chars=5)
     |          >>> repr(badge)
     |          "Badge('example', '123', num_padding_chars=5)"
     |
     |          >>> badge = Badge('example', '123', num_label_padding_chars=5)
     |          >>> repr(badge)
     |          "Badge('example', '123', num_label_padding_chars=5)"
     |
     |          >>> badge = Badge('example', '123', num_label_padding_chars=5, num_value_padding_chars=6,
     |          ...               template='template.svg', value_prefix='$', thresholds={10: 'green', 30: 'red'},
     |          ...               default_color='red', use_max_when_value_exceeds=False, value_format="%s m/s")
     |          >>> repr(badge)
     |          "Badge('example', '123', num_label_padding_chars=5, num_value_padding_chars=6, template='template.svg', value_prefix='$', thresholds={10: 'green', 30: 'red'}, default_color='red', use_max_when_value_exceeds=False, value_format='%s m/s')"
     |
     |  __str__(self)
     |      Return string representation of badge.
     |
     |      This will return the badge SVG text.
     |
     |      Returns: str
     |
     |      Examples:
     |
     |          >>> print(Badge('example', '123'))  # doctest: +ELLIPSIS
     |          <?xml version="1.0" encoding="UTF-8"?>
     |          ...
     |
     |  get_text_width(self, text)
     |      Return the width of text.
     |
     |      Args:
     |          text(str): Text to get the pixel width of.
     |
     |      Returns:
     |          int: Pixel width of the given text based on the badges selected font.
     |
     |      This implementation assumes a fixed font of:
     |
     |      font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11"
     |      >>> badge = Badge('x', 1, font_name='DejaVu Sans,Verdana,Geneva,sans-serif', font_size=11)
     |      >>> badge.get_text_width('pylint')
     |      34
     |
     |  write_badge(self, file_path, overwrite=False)
     |      Write badge to file.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  arc_start
     |      The position where the arc on the gitlab-scoped should start.
     |
     |      Returns: int
     |
     |      Examples:
     |
     |          >>> badge = Badge('pylint', '5')
     |          >>> badge.arc_start
     |          58
     |
     |  badge_color
     |      Badge color based on the configured thresholds.
     |
     |      Returns: str
     |
     |  badge_color_code
     |      Return the color code for the badge.
     |
     |      Returns: str
     |
     |      Raises: ValueError when an invalid badge color is set.
     |
     |  badge_svg_text
     |      The badge SVG text.
     |
     |      Returns: str
     |
     |  badge_width
     |      The total width of badge.
     |
     |      Returns: int
     |
     |      Examples:
     |
     |          >>> badge = Badge('pylint', '5')
     |          >>> badge.badge_width
     |          61
     |
     |  color_split_position
     |      The SVG x position where the color split should occur.
     |
     |      Returns: int
     |
     |  float_thresholds
     |      Thresholds as a dict using floats as keys.
     |
     |  font_width
     |      Return the width multiplier for a font.
     |
     |      Returns:
     |          int: Maximum pixel width of badges selected font.
     |
     |      Example:
     |
     |          >>> Badge(label='x', value='1').font_width
     |          10
     |
     |  label_anchor
     |      The SVG x position of the middle anchor for the label text.
     |
     |      Returns: float
     |
     |  label_anchor_shadow
     |      The SVG x position of the label shadow anchor.
     |
     |      Returns: float
     |
     |  label_width
     |      The SVG width of the label text.
     |
     |      Returns: int
     |
     |  semver_thresholds
     |      Thresholds as a dict using LooseVersion as keys.
     |
     |  semver_version
     |      The semantic version represented by the value string.
     |
     |      Returns: LooseVersion
     |
     |  value_anchor
     |      The SVG x position of the middle anchor for the value text.
     |
     |      Returns: float
     |
     |  value_anchor_shadow
     |      The SVG x position of the value shadow anchor.
     |
     |      Returns: float
     |
     |  value_box_width
     |      The SVG width of the value text box.
     |
     |      Returns: int
     |
     |  value_is_float
     |      Identify whether the value text is a float.
     |
     |      Returns: bool
     |
     |  value_is_int
     |      Identify whether the value text is an int.
     |
     |      Returns: bool
     |
     |  value_type
     |      The Python type associated with the value.
     |
     |      Returns: type
     |
     |  value_width
     |      The SVG width of the value text.
     |
     |      Returns: int
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    main(args=None)
        Generate a badge based on command line arguments.

    parse_args(args)
        Parse the command line arguments.

DATA
    BADGE_TEMPLATES = {'coverage': {'label': 'coverage', 'suffix': '%', 't...
    COLORS = {'aqua': '#00FFFF', 'black': '#000000', 'blue': '#0000FF', 'b...
    DEFAULT_COLOR = '#4c1'
    DEFAULT_FONT = 'DejaVu Sans,Verdana,Geneva,sans-serif'
    DEFAULT_FONT_SIZE = 11
    DEFAULT_TEXT_COLOR = '#fff'
    FONT_WIDTHS = {'Arial, Helvetica, sans-serif': {11: 8}, 'DejaVu Sans,V...
    MASK_ID_PREFIX = 'anybadge_'
    NUM_PADDING_CHARS = 0.5
    TEMPLATE_GITLAB_SCOPED_SVG = '<?xml version="1.0" encoding="UTF-8"?>\n...
    TEMPLATE_SVG = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmln...ho...
    VERSION_COMPARISON_SUPPORTED = True
    __summary__ = 'A simple, flexible badge generator.'
    __title__ = 'anybadge'
    __uri__ = 'https://github.com/jongracecox/anybadge'
    __version_info__ = ('0', '0', '0')
    version = '0.0.0'

VERSION
    0.0.0
```
