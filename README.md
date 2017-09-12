# anybadge
Python project for generating badges for your projects

[![build status](https://api.travis-ci.org/jongracecox/anybadge.svg?branch=master)](https://travis-ci.org/jongracecox/anybadge)

# Overview
`anybadge` can be used to add badge generation to your Python projects,
and also provides a command line interface.

This utility can be used to generate .svg badge images, using configurable
thresholds for coloring the badges based on the badge value.  Many badge
generation tools just provide the ability to specify the color of badge.
`anybadge` allows you to specify the label, badge value, and color, but
is also allows you to specify a set of thresholds that can be used to
select a color based on the badge value.

# Basic usage
As an example, if you want to produce a pylint badge, you may run `anybadge`
from the command line like this:

```
anybadge.py -l pylint -v 2.22 -f pylint.svg 2=red 4=orange 6=yellow 8=green 10=brightgreen
```

In this example the label is set to "pylint", the value "2.22", and an
output file called "pylint.svg".  The thresholds are provided in pairs
of `<value>=color`.  Values can be integer or floats for ranges, and
string values are also supported.

# Installation
You can install the latest release of `anybadge` using `pip`:

```
pip install anybadge
```

This will install the Python package, and also make `anybadge` available
as a command line utility.

# Getting help
To get help from the command line utility, just run:

```
anybadge --help
```

# Usage

## Output
Running the utility with the `--file` option will result in the .svg image being
written to file.  Without the `--file` option the `.svg` file content will be
written to stdout, so can be redirected to a file.

## Thresholds
Some thresholds have been built in to save time.  To use these thresholds you
can simply specify the template name instead of threshold value/color pairs.

## Command line options

```
positional arguments:
  args                  Pairs of <upper>=<color>. For example 2=red 4=orange
                        6=yellow 8=good 10=brightgreen. Read this as "Less
                        than 2 = red, less than 4 = orange...".

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
```

## Examples

Here are some usage specific examples that may save time on defining
thresholds.

### Pylint

```
anybadge.py --value=2.22 --file=pylint.svg pylint
```

```
anybadge.py --label=pylint --value=2.22 --file=pylint.svg 2=red 4=orange 6=yellow 8=green 10=brightgreen
```

### Coverage

```
anybadge.py --value=65 --file=coverage.svg coverage
```

```
anybadge.py --label=coverage --value=65 --suffix='%%' --file=coverage.svg 50=red 60=orange 75=yellow 90=green 100=brightgreen
```

### CI Pipeline

```
anybadge.py --label=pipeline --value=passing --file=pipeline.svg passing=green failing=red
```
