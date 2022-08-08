import anybadge

if __name__ == "__main__":

    print(
        """| Color Name | Hex Code | Example |
    | ---------- | -------- | ------- |"""
    )
    for color, hex in sorted(anybadge.COLORS.items()):

        file = "examples/color_" + color + ".svg"

        url = "https://cdn.rawgit.com/jongracecox/anybadge/master/" + file

        anybadge.Badge(label="Color", value=color, default_color=color).write_badge(
            file, overwrite=True
        )

        print(
            "| {color} | {hex} | ![]({url}) |".format(
                color=color, hex=hex.upper(), url=url
            )
        )
