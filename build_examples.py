from pathlib import Path

import anybadge


def color_examples_table():
    """Output the Markdown table containing color examples."""
    print(
        """
| Color Name    | Hex     | Example |
| ------------- | ------- | ------- |"""
    )
    for color in sorted(anybadge.colors.Color):
        file = "examples/color_" + color.name.lower() + ".svg"

        url = "https://cdn.rawgit.com/jongracecox/anybadge/master/" + file

        anybadge.Badge(
            label="Color", value=color.name.lower(), default_color=color.value
        ).write_badge(file, overwrite=True)

        print(
            f"| {color.name.lower():<13} | {color.value.upper():<7} | ![]({f'{url})':<84}|"
        )


def other_examples():
    """Generate emoji example badges used in documentation."""
    examples_dir = Path(__file__).parent / Path("examples")
    for label, value, file, kwargs in [
        ("Pipeline status", "😄", "pipeline_smile.svg", {}),
        (
            "Pipeline status",
            "😄",
            "pipeline_smile_padding.svg",
            {"num_value_padding_chars": 1},
        ),
        ("Pipeline status", "😟", "pipeline_frown.svg", {"default_color": "Red"}),
        ("🔗", "Documentation", "documentation_link.svg", {}),
        ("🔗", "PyPi", "pypi_link.svg", {}),
        ("", "Value only", "value_only.svg", {}),
        ("Label only", "", "label_only.svg", {}),
    ]:
        anybadge.Badge(label=label, value=value, **kwargs).write_badge(
            examples_dir / Path(file), overwrite=True
        )


def main():
    color_examples_table()
    other_examples()


if __name__ == "__main__":
    main()
