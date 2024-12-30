#!/usr/bin/python
import os
import re
import subprocess
from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


def get_version():
    """Get the version from git tags.

    Version is determined by the latest git tag, and will be the tag name without the leading 'v'.

    Returns:
        str: The version number.
    """
    try:
        # Get the latest git tag
        version = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], encoding="utf-8"
        ).strip()
        version = re.sub("^v", "", version)
        return version

    except subprocess.CalledProcessError:
        return "0.0.0"


setup(
    name="anybadge",
    description="Simple, flexible badge generator for project badges.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=get_version(),
    author="Jon Grace-Cox",
    author_email="30441316+jongracecox@users.noreply.github.com",
    packages=["anybadge", "anybadge.templates", "anybadge.server"],
    py_modules=["anybadge_server"],
    setup_requires=["setuptools", "wheel"],
    tests_require=[],
    install_requires=["packaging"],
    package_data={"anybadge": ["templates/*.svg"]},
    options={"bdist_wheel": {"universal": False}},
    python_requires=">=3.7",
    url="https://github.com/jongracecox/anybadge",
    entry_points={
        "console_scripts": [
            "anybadge=anybadge.cli:main",
            "anybadge-server=anybadge.server.cli:main",
        ],
    },
    classifiers=["License :: OSI Approved :: MIT License"],
)
