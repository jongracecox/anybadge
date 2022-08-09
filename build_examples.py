import anybadge

if __name__ == "__main__":

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
