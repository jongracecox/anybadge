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

    # Badges created with :emoji: shortcodes. These require the emoji package
    # (``pip install anybadge[emoji]``), and produce SVGs identical to the
    # equivalent badges created with actual emoji characters above.
    for label, value, file in [
        ("Pipeline status", ":smile:", "pipeline_smile_shortcode.svg"),
        (":rocket: Deploy", ":100:", "rocket_deploy.svg"),
    ]:
        anybadge.Badge(label=label, value=value).write_badge(
            examples_dir / Path(file), overwrite=True
        )

    # The same shortcode badge again, but with the emoji package made absent,
    # to show what is rendered without the optional ``emoji`` dependency:
    # shortcodes are left as-is in the badge text.
    import sys

    emoji_module = sys.modules.get("emoji")
    sys.modules["emoji"] = None
    try:
        badge = anybadge.Badge(label="Pipeline status", value=":smile:")
    finally:
        if emoji_module is None:
            del sys.modules["emoji"]
        else:
            sys.modules["emoji"] = emoji_module
    badge.write_badge(
        examples_dir / Path("pipeline_smile_without_emoji_package.svg"), overwrite=True
    )

    # Logo example badges, using icons bundled with the package.
    for label, value, file, kwargs in [
        ("Stars", "23,414", "logo_github_left.svg", {"logo": "github"}),
        (
            "Stars",
            "23,414",
            "logo_github_right.svg",
            {"logo": "github", "logo_position": "right"},
        ),
        ("Python", "3.13", "logo_python.svg", {"logo": "python"}),
        ("Docker", "passing", "logo_docker_pipeline.svg", {"logo": "docker"}),
    ]:
        anybadge.Badge(label=label, value=value, **kwargs).write_badge(
            examples_dir / Path(file), overwrite=True
        )


def main():
    color_examples_table()
    other_examples()


if __name__ == "__main__":
    main()
