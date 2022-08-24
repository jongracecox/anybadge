from typing import Generator, Tuple

import requests
from invoke import task
from bs4 import BeautifulSoup

from anybadge.colors import Color


@task
def update(c):
    """Generate colors Enum from Mozilla color keywords."""
    url = "https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color_keywords"
    response = requests.get(url)

    # Extract colors from HTML

    def generator() -> Generator[Tuple[str, str], None, None]:
        soup = BeautifulSoup(response.content, features="html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        for row in rows[1:]:
            cols = row.findAll("code")
            yield cols[0].text.upper(), cols[1].text.upper()

    # Populate lookup from Enum
    color_lookup = {}
    for color in Color:
        color_lookup[color.name.upper()] = color.value.upper()

    def get_next_name(key: str) -> str:
        num = 1
        while True:
            num += 1
            next_name = f"{key}_{num}"
            if next_name not in color_lookup:
                return next_name

    # Add Mozilla values
    for name, value in generator():
        if name in color_lookup:
            existing_value = color_lookup[name]
            if value != existing_value:
                color_lookup[get_next_name(name)] = value
                print(
                    f"Found conflict: {name}: Mozilla={value}, Anybadge={existing_value}."
                )
        else:
            color_lookup[name.upper()] = value.upper()

    # Resolve any non-hex lookup values. These are normally references to other colors.
    for name, value in color_lookup.items():
        if not value.startswith("#"):
            color_lookup[name] = color_lookup[value]

    # Print final enum
    print("\nclass Color(Enum):")
    for name, value in sorted(color_lookup.items(), key=lambda x: x[1]):
        print(f'    {name} = "{value}"')
