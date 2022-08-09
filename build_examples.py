import anybadge

if __name__ == "__main__":

    print(
        """| Color Name | Hex Code | Example |
    | ---------- | -------- | ------- |"""
    )
    for color in sorted(anybadge.colors.Color):

        file = "examples/color_" + color.name.lower() + ".svg"

        url = "https://cdn.rawgit.com/jongracecox/anybadge/master/" + file

        anybadge.Badge(
            label="Color", value=color.name, default_color=color.value
        ).write_badge(file, overwrite=True)

        print(f"| {color.name} | {color.value.upper()} | ![]({url}) |")
