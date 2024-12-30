# anybadge

Python project for generating badges for your projects

[![pypi package](https://badge.fury.io/py/anybadge.svg)](https://pypi.org/project/anybadge)
[![build status](https://api.travis-ci.com/jongracecox/anybadge.svg?branch=master)](https://app.travis-ci.com/github/jongracecox/anybadge)
[![downloads](https://img.shields.io/pypi/dm/anybadge.svg)](https://pypistats.org/packages/anybadge)
[![GitHub last commit](https://img.shields.io/github/last-commit/jongracecox/anybadge.svg)](https://github.com/jongracecox/anybadge/commits/master)
[![GitHub](https://img.shields.io/github/license/jongracecox/anybadge.svg)](https://github.com/jongracecox/anybadge/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jongracecox/anybadge.svg?style=social)](https://github.com/jongracecox/anybadge/stargazers)
[![Snyk health](https://snyk.io/advisor/python/anybadge/badge.svg)](https://snyk.io/advisor/python/anybadge)
[![Downloads](https://pepy.tech/badge/anybadge)](https://pepy.tech/project/anybadge)

[![buymeacoffee](https://camo.githubusercontent.com/c3f856bacd5b09669157ed4774f80fb9d8622dd45ce8fdf2990d3552db99bd27/68747470733a2f2f7777772e6275796d6561636f666665652e636f6d2f6173736574732f696d672f637573746f6d5f696d616765732f6f72616e67655f696d672e706e67)](https://www.buymeacoffee.com/jongracecox)

Supports: Python 3.7-3.13 (2.7-3.6 support has been dropped)

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
types can be used in the `default_color`, `text_color` and `thresholds` attributes. Color names are
taken from the [Mozilla color keywords list](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color_keywords).

Here is a Python example showing use of a named color and a custom color.

```python
import anybadge

badge = anybadge.Badge(label='custom color', value='teal', default_color='teal', num_padding_chars=1)
badge = anybadge.Badge(label='custom color', value='teal', default_color='#008080', num_padding_chars=1)
```

Available named colors are:

| Color Name    | Hex     | Example |
| ------------- | ------- | ------- |
| aliceblue     | #F0F8FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_aliceblue.svg)    |
| antiquewhite  | #FAEBD7 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_antiquewhite.svg) |
| aqua          | #00FFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_aqua.svg)         |
| aquamarine    | #7FFFD4 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_aquamarine.svg)   |
| azure         | #F0FFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_azure.svg)        |
| beige         | #F5F5DC | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_beige.svg)        |
| bisque        | #FFE4C4 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_bisque.svg)       |
| black         | #000000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_black.svg)        |
| blanchedalmond | #FFEBCD | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_blanchedalmond.svg)|
| blue          | #0000FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_blue.svg)         |
| blueviolet    | #8A2BE2 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_blueviolet.svg)   |
| bright_red    | #FF0000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_bright_red.svg)   |
| bright_yellow | #FFFF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_bright_yellow.svg)|
| brown         | #A52A2A | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_brown.svg)        |
| burlywood     | #DEB887 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_burlywood.svg)    |
| cadetblue     | #5F9EA0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_cadetblue.svg)    |
| chartreuse    | #7FFF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_chartreuse.svg)   |
| chocolate     | #D2691E | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_chocolate.svg)    |
| coral         | #FF7F50 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_coral.svg)        |
| cornflowerblue | #6495ED | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_cornflowerblue.svg)|
| cornsilk      | #FFF8DC | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_cornsilk.svg)     |
| crimson       | #DC143C | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_crimson.svg)      |
| darkblue      | #00008B | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkblue.svg)     |
| darkcyan      | #008B8B | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkcyan.svg)     |
| darkgoldenrod | #B8860B | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkgoldenrod.svg)|
| darkgray      | #A9A9A9 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkgray.svg)     |
| darkgreen     | #006400 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkgreen.svg)    |
| darkkhaki     | #BDB76B | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkkhaki.svg)    |
| darkmagenta   | #8B008B | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkmagenta.svg)  |
| darkolivegreen | #556B2F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkolivegreen.svg)|
| darkorange    | #FF8C00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkorange.svg)   |
| darkorchid    | #9932CC | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkorchid.svg)   |
| darkred       | #8B0000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkred.svg)      |
| darksalmon    | #E9967A | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darksalmon.svg)   |
| darkseagreen  | #8FBC8F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkseagreen.svg) |
| darkslateblue | #483D8B | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkslateblue.svg)|
| darkslategray | #2F4F4F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkslategray.svg)|
| darkturquoise | #00CED1 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkturquoise.svg)|
| darkviolet    | #9400D3 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_darkviolet.svg)   |
| deeppink      | #FF1493 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_deeppink.svg)     |
| deepskyblue   | #00BFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_deepskyblue.svg)  |
| dimgray       | #696969 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_dimgray.svg)      |
| dodgerblue    | #1E90FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_dodgerblue.svg)   |
| firebrick     | #B22222 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_firebrick.svg)    |
| floralwhite   | #FFFAF0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_floralwhite.svg)  |
| forestgreen   | #228B22 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_forestgreen.svg)  |
| fuchsia       | #FF00FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_fuchsia.svg)      |
| gainsboro     | #DCDCDC | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_gainsboro.svg)    |
| ghostwhite    | #F8F8FF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_ghostwhite.svg)   |
| gold          | #FFD700 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_gold.svg)         |
| goldenrod     | #DAA520 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_goldenrod.svg)    |
| gray          | #808080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_gray.svg)         |
| green         | #4C1    | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_green.svg)        |
| greenyellow   | #ADFF2F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_greenyellow.svg)  |
| green_2       | #008000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_green_2.svg)      |
| honeydew      | #F0FFF0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_honeydew.svg)     |
| hotpink       | #FF69B4 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_hotpink.svg)      |
| indianred     | #CD5C5C | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_indianred.svg)    |
| indigo        | #4B0082 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_indigo.svg)       |
| ivory         | #FFFFF0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_ivory.svg)        |
| khaki         | #F0E68C | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_khaki.svg)        |
| lavender      | #E6E6FA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lavender.svg)     |
| lavenderblush | #FFF0F5 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lavenderblush.svg)|
| lawngreen     | #7CFC00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lawngreen.svg)    |
| lemonchiffon  | #FFFACD | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lemonchiffon.svg) |
| lightblue     | #ADD8E6 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightblue.svg)    |
| lightcoral    | #F08080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightcoral.svg)   |
| lightcyan     | #E0FFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightcyan.svg)    |
| lightgoldenrodyellow | #FAFAD2 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightgoldenrodyellow.svg)|
| lightgray     | #D3D3D3 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightgray.svg)    |
| lightgreen    | #90EE90 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightgreen.svg)   |
| lightpink     | #FFB6C1 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightpink.svg)    |
| lightsalmon   | #FFA07A | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightsalmon.svg)  |
| lightseagreen | #20B2AA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightseagreen.svg)|
| lightskyblue  | #87CEFA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightskyblue.svg) |
| lightslategray | #778899 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightslategray.svg)|
| lightsteelblue | #B0C4DE | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightsteelblue.svg)|
| lightyellow   | #FFFFE0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lightyellow.svg)  |
| light_grey    | #9F9F9F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_light_grey.svg)   |
| lime          | #00FF00 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_lime.svg)         |
| limegreen     | #32CD32 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_limegreen.svg)    |
| linen         | #FAF0E6 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_linen.svg)        |
| maroon        | #800000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_maroon.svg)       |
| mediumaquamarine | #66CDAA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumaquamarine.svg)|
| mediumblue    | #0000CD | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumblue.svg)   |
| mediumorchid  | #BA55D3 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumorchid.svg) |
| mediumpurple  | #9370DB | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumpurple.svg) |
| mediumseagreen | #3CB371 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumseagreen.svg)|
| mediumslateblue | #7B68EE | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumslateblue.svg)|
| mediumspringgreen | #00FA9A | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumspringgreen.svg)|
| mediumturquoise | #48D1CC | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumturquoise.svg)|
| mediumvioletred | #C71585 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mediumvioletred.svg)|
| midnightblue  | #191970 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_midnightblue.svg) |
| mintcream     | #F5FFFA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mintcream.svg)    |
| mistyrose     | #FFE4E1 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_mistyrose.svg)    |
| moccasin      | #FFE4B5 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_moccasin.svg)     |
| navajowhite   | #FFDEAD | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_navajowhite.svg)  |
| navy          | #000080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_navy.svg)         |
| oldlace       | #FDF5E6 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_oldlace.svg)      |
| olive         | #808000 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_olive.svg)        |
| olivedrab     | #6B8E23 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_olivedrab.svg)    |
| orange        | #FE7D37 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_orange.svg)       |
| orangered     | #FF4500 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_orangered.svg)    |
| orange_2      | #FFA500 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_orange_2.svg)     |
| orchid        | #DA70D6 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_orchid.svg)       |
| palegoldenrod | #EEE8AA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_palegoldenrod.svg)|
| palegreen     | #98FB98 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_palegreen.svg)    |
| paleturquoise | #AFEEEE | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_paleturquoise.svg)|
| palevioletred | #DB7093 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_palevioletred.svg)|
| papayawhip    | #FFEFD5 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_papayawhip.svg)   |
| peachpuff     | #FFDAB9 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_peachpuff.svg)    |
| peru          | #CD853F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_peru.svg)         |
| pink          | #FFC0CB | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_pink.svg)         |
| plum          | #DDA0DD | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_plum.svg)         |
| powderblue    | #B0E0E6 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_powderblue.svg)   |
| purple        | #800080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_purple.svg)       |
| rebeccapurple | #663399 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_rebeccapurple.svg)|
| red           | #E05D44 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_red.svg)          |
| rosybrown     | #BC8F8F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_rosybrown.svg)    |
| royalblue     | #4169E1 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_royalblue.svg)    |
| saddlebrown   | #8B4513 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_saddlebrown.svg)  |
| salmon        | #FA8072 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_salmon.svg)       |
| sandybrown    | #F4A460 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_sandybrown.svg)   |
| seagreen      | #2E8B57 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_seagreen.svg)     |
| seashell      | #FFF5EE | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_seashell.svg)     |
| sienna        | #A0522D | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_sienna.svg)       |
| silver        | #C0C0C0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_silver.svg)       |
| skyblue       | #87CEEB | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_skyblue.svg)      |
| slateblue     | #6A5ACD | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_slateblue.svg)    |
| slategray     | #708090 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_slategray.svg)    |
| snow          | #FFFAFA | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_snow.svg)         |
| springgreen   | #00FF7F | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_springgreen.svg)  |
| steelblue     | #4682B4 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_steelblue.svg)    |
| tan           | #D2B48C | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_tan.svg)          |
| teal          | #008080 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_teal.svg)         |
| thistle       | #D8BFD8 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_thistle.svg)      |
| tomato        | #FF6347 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_tomato.svg)       |
| turquoise     | #40E0D0 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_turquoise.svg)    |
| violet        | #EE82EE | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_violet.svg)       |
| wheat         | #F5DEB3 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_wheat.svg)        |
| white         | #FFFFFF | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_white.svg)        |
| whitesmoke    | #F5F5F5 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_whitesmoke.svg)   |
| yellow        | #DFB317 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellow.svg)       |
| yellowgreen   | #9ACD32 | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellowgreen.svg)  |
| yellow_green  | #A4A61D | ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/color_yellow_green.svg) |

### Emojis

It is possible to use emoji characters in badge labels and values. Here are some examples:

![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pipeline_frown.svg)
![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pipeline_smile.svg)
![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/documentation_link.svg)
![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pypi_link.svg)

These files were created by using the **actual** emoji character in the label/value text. For example:

```python
badge = anybadge.Badge(label="Pipeline status", value="😄")
```

There are some caveats worth mentioning:
- The "look" of the emoji is determined by the client (Emoji characters are placed as-is into the SVG file, and are
  rendered client-side)
- Rendering may fail in some viewers and developer IDEs (for example, PyCharm does not render emojis in the svg viewer)
- Emojis can have different widths, so the layout may be affected. You can use `num_label_padding_chars` and
  `num_value_padding_chars` to fix (see below)

Here are some examples to show how to use padding to fix layout:

| Badge | Code                                                                 |
| ----- |----------------------------------------------------------------------|
| ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pipeline_smile.svg) | `anybadge.Badge("Pipeline status", "😄")` |
| ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/pipeline_smile_padding.svg) | `anybadge.Badge("Pipeline status", "😄", num_value_padding_chars=1)` |

### Value or label only

It is possible to create badges with only a label or only a value. This can be done by passing
an empty string to the appropriate field. Note that either a label or value must be provided.

| Badge                                                                           | Code                                 |
|---------------------------------------------------------------------------------|--------------------------------------|
| ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/label_only.svg) | `anybadge.Badge(label="Label only")` |
| ![](https://cdn.rawgit.com/jongracecox/anybadge/master/examples/value_only.svg) | `anybadge.Badge(value="Value only")` |

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
