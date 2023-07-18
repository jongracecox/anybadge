import argparse
import sys
import textwrap

from anybadge.styles import Style
from anybadge.templates import get_template
from anybadge import __version__ as anybadge_version
from . import config
from .badge import Badge


def parse_args(args):
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
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

"""
        ),
    )
    parser.add_argument("-l", "--label", type=str, help="The badge label.", default="")
    parser.add_argument("-v", "--value", type=str, help="The badge value.", default="")
    parser.add_argument(
        "-m",
        "--value-format",
        type=str,
        default=None,
        help='Formatting string for value (e.g. "%%.2f" for 2dp floats)',
    )
    parser.add_argument(
        "-c",
        "--color",
        type=str,
        help="For fixed color badges use --color to specify the badge color.",
        default=config.DEFAULT_COLOR,
    )
    parser.add_argument(
        "-p", "--prefix", type=str, help="Optional prefix for value.", default=""
    )
    parser.add_argument(
        "-s", "--suffix", type=str, help="Optional suffix for value.", default=""
    )
    parser.add_argument(
        "-d",
        "--padding",
        type=int,
        help="Number of characters to pad on either side of the badge text.",
        default=config.NUM_PADDING_CHARS,
    )
    parser.add_argument(
        "-lp",
        "--label-padding",
        type=int,
        help="Number of characters to pad on either side of the badge label.",
        default=None,
    )
    parser.add_argument(
        "-vp",
        "--value-padding",
        type=int,
        help="Number of characters to pad on either side of the badge value.",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--font",
        type=str,
        help="Font name.  Supported fonts: "
        ",".join(['"%s"' % x for x in config.FONT_WIDTHS.keys()]),
        default=config.DEFAULT_FONT,
    )
    parser.add_argument(
        "-z",
        "--font-size",
        type=int,
        help="Font size.",
        default=config.DEFAULT_FONT_SIZE,
    )
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        help="Location of alternative template .svg file.",
        default=get_template("default"),
    )
    parser.add_argument(
        "-st",
        "--style",
        type=str,
        help="Alternative style of badge to create. Valid "
        'values are "gitlab-scoped", "default". This '
        "overrides any templates passed using --template.",
    )
    parser.add_argument(
        "-u",
        "--use-max",
        action="store_true",
        help="Use the maximum threshold color when the value exceeds the "
        "maximum threshold.",
    )
    parser.add_argument("-f", "--file", type=str, help="Output file location.")
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    parser.add_argument(
        "-r",
        "--text-color",
        type=str,
        help="Text color. Single value affects both label"
        "and value colors.  A comma separated pair "
        "affects label and value text respectively.",
        default=config.DEFAULT_TEXT_COLOR,
    )
    parser.add_argument(
        "-e",
        "--semver",
        action="store_true",
        default=False,
        help="Treat value and thresholds as semantic versions.",
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Pairs of <upper>=<color>. "
        "For example 2=red 4=orange 6=yellow 8=good. "
        'Read this as "Less than 2 = red, less than 4 = orange...".',
    )
    return parser.parse_args(args)


def main(args=None):
    """Generate a badge based on command line arguments."""

    # Args may be sent from command line of as args directly.
    if not args:
        args = sys.argv[1:]

    if args == ["--version"]:
        print(anybadge_version)
        return

    # Parse command line arguments
    args = parse_args(args)

    label = args.label
    threshold_text = args.args
    suffix = args.suffix

    # Check whether thresholds were sent as one word, and is in the
    # list of available styles.  If so, swap in the style.
    if len(args.args) == 1 and Style.exists(args.args[0].upper()):
        style_name = args.args[0].upper()
        style = Style[style_name]
        threshold_text = style.threshold.split(" ")
        if not args.label and style.label:
            label = style.label
        if not args.suffix and style.suffix:
            suffix = style.suffix

    # Create threshold list from args
    threshold_list = [x.split("=") for x in threshold_text]
    threshold_dict = {x[0]: x[1] for x in threshold_list}

    # Create badge object
    badge = Badge(
        label,
        args.value,
        value_prefix=args.prefix,
        value_suffix=suffix,
        default_color=args.color,
        num_padding_chars=args.padding,
        num_label_padding_chars=args.label_padding,
        num_value_padding_chars=args.value_padding,
        font_name=args.font,
        font_size=args.font_size,
        template=args.template,
        style=args.style,
        use_max_when_value_exceeds=args.use_max,
        thresholds=threshold_dict,
        value_format=args.value_format,
        text_color=args.text_color,
        semver=args.semver,
    )

    if args.file:
        # Write badge SVG to file
        badge.write_badge(args.file, overwrite=args.overwrite)
    else:
        print(badge.badge_svg_text)


if __name__ == "__main__":
    main()
