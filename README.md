# anybadge

Python project for generating badges for your projects

[![build status](https://api.travis-ci.org/jongracecox/anybadge.svg?branch=master)](https://travis-ci.org/jongracecox/anybadge)

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

```
anybadge --value=<VALUE> --file=<FILE> <TEMPLATE-NAME>
```

For example:

```bash
anybadge --value=2.22 --file=pylint.svg pylint
```

### Examples

#### Pylint using template
```
anybadge --value=2.22 --file=pylint.svg pylint
```
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pylint.svg) 

#### Pylint using arguments
```
anybadge -l pylint -v 2.22 -f pylint.svg 2=red 4=orange 8=yellow 10=green
```
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pylint.svg) 

#### Coverage using template
```
anybadge --value=65 --file=coverage.svg coverage
``` 
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/coverage.svg)

#### Pipeline, using labeled colors
```
anybadge --label=pipeline --value=passing --file=pipeline.svg passing=green failing=red
```
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pipeline.svg)

#### Badge with fixed color
```
anybadge --label=awesomeness --value="110%" --file=awesomeness.svg --color=#97CA00
```
![pylint](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/awesomeness.svg)

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
   -n FONT, --font FONT  "DejaVu Sans,Verdana,Geneva,sans-serif"
   -z FONT_SIZE, --font-size FONT_SIZE
                         Font size.
   -t TEMPLATE, --template TEMPLATE
                         Location of alternative template .svg file.
   -u, --use-max         Use the maximum threshold color when the value exceeds
                         the maximum threshold.
   -f FILE, --file FILE  Output file location.
   -o, --overwrite       Overwrite output file if it already exists.
   -r TEXT_COLOR, --text-color TEXT_COLOR
                         Text color. Single value affects both labeland value
                         colors. A comma separated pair affects label and value
                                 text respectively.

Examples
--------

Here are some usage specific command line examples that may save time on defining
thresholds.

Pylint::

anybadge.py --value=2.22 --file=pylint.svg pylint
anybadge.py --label=pylint --value=2.22 --file=pylint.svg 2=red 4=orange 8=yellow 10=green

Coverage::

anybadge.py --value=65 --file=coverage.svg coverage
anybadge.py --label=coverage --value=65 --suffix='%%' --file=coverage.svg 50=red 60=orange 80=yellow 100=green

CI Pipeline::

anybadge.py --label=pipeline --value=passing --file=pipeline.svg passing=green failing=red

Python usage
============
Here is the output of ``help(anybadge)``::

Help on module anybadge:

NAME
   anybadge - anybadge

FILE
   /home/jon/Git/anybadge/anybadge.py

DESCRIPTION
   A Python module for generating badges for your projects, with a focus on
   simplicity and flexibility.

CLASSES
   __builtin__.object
       Badge

   class Badge(__builtin__.object)
    |  Badge class used to generate badges.
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
    |      >>> badge = Badge('pylint', 6, thresholds={2: 'red',
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
    |      False, so 11 yields the default color '#a4a61d'
    |      >>> badge = Badge('pylint', 11, use_max_when_value_exceeds=False,
    |      ...               thresholds={2: 'red', 4: 'orange', 8: 'yellow',
    |      ...                           10: 'green'})
    |      >>> badge.badge_color
    |      '#a4a61d'
    |
    |  Methods defined here:
    |
    |  __init__(self, label, value, font_name='DejaVu Sans,Verdana,Geneva,sans-serif', font_size=11, num_padding_chars=0.5, template='<?xml version="1.0" encoding="UTF-8"?>\n<svg xmln...hor }}" y="14">{{ value }}</text>\n    </g>\n</svg>', value_prefix='', value_suffix='', thresholds=None, default_color='#a4a61d', use_max_when_value_exceeds=True, value_format=None, text_color='#fff')
    |      Constructor for Badge class.
    |
    |  get_text_width(self, text)
    |      Return the width of text.
    |
    |      This implementation assumes a fixed font of:
    |
    |      font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11"
    |      >>> badge = Badge('x', 1, font_name='DejaVu Sans,Verdana,Geneva,sans-serif', font_size=11)
    |      >>> badge.get_text_width('pylint')
    |      42
    |
    |  write_badge(self, file_path, overwrite=False)
    |      Write badge to file.
    |
    |  ----------------------------------------------------------------------
    |  Static methods defined here:
    |
    |  get_font_width(font_name, font_size)
    |      Return the width multiplier for a font.
    |
    |      >>> Badge.get_font_width('DejaVu Sans,Verdana,Geneva,sans-serif', 11)
    |      7
    |
    |  ----------------------------------------------------------------------
    |  Data descriptors defined here:
    |
    |  __dict__
    |      dictionary for instance variables (if defined)
    |
    |  __weakref__
    |      list of weak references to the object (if defined)
    |
    |  badge_color
    |      Find the badge color based on the thresholds.
    |
    |  badge_color_code
    |      Return the color code for the badge.
    |
    |  badge_svg_text
    |      The badge SVG text.
    |
    |  badge_width
    |      The total width of badge.
    |
    |      >>> badge = Badge('pylint', '5', font_name='DejaVu Sans,Verdana,Geneva,sans-serif',
    |      ...               font_size=11)
    |      >>> badge.badge_width
    |      91
    |
    |  color_split_position
    |      The SVG x position where the color split should occur.
    |
    |  font_width
    |      Return the badge font width.
    |
    |  label_anchor
    |      The SVG x position of the middle anchor for the label text.
    |
    |  label_anchor_shadow
    |      The SVG x position of the label shadow anchor.
    |
    |  label_width
    |      The SVG width of the label text.
    |
    |  value_anchor
    |      The SVG x position of the middle anchor for the value text.
    |
    |  value_anchor_shadow
    |      The SVG x position of the value shadow anchor.
    |
    |  value_is_float
    |      Identify whether the value text is a float.
    |
    |  value_is_int
    |      Identify whether the value text is an int.
    |
    |  value_type
    |      The Python type associated with the value.
    |
    |  value_width
    |      The SVG width of the value text.

FUNCTIONS
   main()
       Generate a badge based on command line arguments.

   parse_args()
       Parse the command line arguments.

DATA
   BADGE_TEMPLATES = {'coverage': {'label': 'coverage', 'suffix': '%', 't...
   COLORS = {'green': '#97CA00', 'lightgrey': '#9f9f9f', 'orange': '#fe7d...
   DEFAULT_COLOR = '#a4a61d'
   DEFAULT_FONT = 'DejaVu Sans,Verdana,Geneva,sans-serif'
   DEFAULT_FONT_SIZE = 11
   DEFAULT_TEXT_COLOR = '#fff'
   FONT_WIDTHS = {'DejaVu Sans,Verdana,Geneva,sans-serif': {11: 7}}
   NUM_PADDING_CHARS = 0.5
   TEMPLATE_SVG = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmln...ho...
   __summary__ = 'A simple, flexible badge generator.'
   __title__ = 'anybadge'
   __uri__ = 'https://github.com/jongracecox/anybadge'
   __version__ = '0.2.0.dev1'
   __version_info__ = ('0', '2', '0', 'dev1')
   version = '0.2.0.dev1'

VERSION
   0.2.0.dev1
```
