# anybadge

Python project for generating badges for your projects

[![pypi package](https://badge.fury.io/py/anybadge.svg)](https://pypi.org/project/anybadge)
[![build status](https://api.travis-ci.com/jongracecox/anybadge.svg?branch=master)](https://app.travis-ci.com/github/jongracecox/anybadge)
[![downloads](https://img.shields.io/pypi/dm/anybadge.svg)](https://pypistats.org/packages/anybadge)
[![GitHub last commit](https://img.shields.io/github/last-commit/jongracecox/anybadge.svg)](https://github.com/jongracecox/anybadge/commits/master)
[![GitHub](https://img.shields.io/github/license/jongracecox/anybadge.svg)](https://github.com/jongracecox/anybadge/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jongracecox/anybadge.svg?style=social)](https://github.com/jongracecox/anybadge/stargazers)

[![buymeacoffee](https://camo.githubusercontent.com/c3f856bacd5b09669157ed4774f80fb9d8622dd45ce8fdf2990d3552db99bd27/68747470733a2f2f7777772e6275796d6561636f666665652e636f6d2f6173736574732f696d672f637573746f6d5f696d616765732f6f72616e67655f696d672e706e67)](https://www.buymeacoffee.com/jongracecox)

Supports: Python 3.4-3.9 (2.7 support has been dropped)

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

| Color Name    | Hex     | Example |
| ------------- | ------- | ------- |
| aqua          | #00FFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_aqua.svg)         |
| black         | #000000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_black.svg)        |
| blue          | #0000FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_blue.svg)         |
| bright_red    | #FF0000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_bright_red.svg)   |
| bright_yellow | #FFFF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_bright_yellow.svg)|
| fuchsia       | #FF00FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_fuchsia.svg)      |
| gray          | #808080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_gray.svg)         |
| green         | #4C1    | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_green.svg)        |
| light_grey    | #9F9F9F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_light_grey.svg)   |
| lime          | #00FF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lime.svg)         |
| maroon        | #800000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_maroon.svg)       |
| navy          | #000080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_navy.svg)         |
| olive         | #808000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_olive.svg)        |
| orange        | #FE7D37 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_orange.svg)       |
| purple        | #800080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_purple.svg)       |
| red           | #E05D44 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_red.svg)          |
| silver        | #C0C0C0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_silver.svg)       |
| teal          | #008080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_teal.svg)         |
| white         | #FFFFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_white.svg)        |
| yellow        | #DFB317 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellow.svg)       |
| yellow_green  | #A4A61D | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellow_green.svg) |

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

### Command-line options

The command line options can be viewed using `anybadge --help`.

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

For Python API details you can use the inbuilt documentation:

```python
from anybadge import badge
help(badge)
```
