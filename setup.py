#!/usr/bin/python
import os
import re
from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Attempt to get version number from TravisCI environment variable
version = os.environ.get("TRAVIS_TAG", default="0.0.0")

# Remove leading 'v'
version = re.sub("^v", "", version)

setup(
    name="anybadge",
    description="Simple, flexible badge generator for project badges.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    author="Jon Grace-Cox",
    author_email="jongracecox@gmail.com",
    packages=["anybadge"],
    py_modules=["anybadge_server"],
    setup_requires=["setuptools", "wheel"],
    tests_require=[],
    install_requires=["packaging"],
    package_data={"anybadge": ["templates/*.svg"]},
    options={"bdist_wheel": {"universal": False}},
    python_requires=">=3.4",
    url="https://github.com/jongracecox/anybadge",
    entry_points={
        "console_scripts": [
            "anybadge=anybadge.cli:main",
            "anybadge-server=anybadge.server.cli:main",
        ],
    },
    classifiers=["License :: OSI Approved :: MIT License"],
)
