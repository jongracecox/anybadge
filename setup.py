#!/usr/bin/python

import sys
import re
from setuptools import setup

def get_version():
    with open("anybadge.py", "r") as file_handle:
        file_text = file_handle.read()
    version_match = re.search(r'.* __version__ = [\'"]([^\'"]*)[\'"]', file_text)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to identify version string.")

setup(
    name='anybadge',
    description='Simple, flexible badge generator for project badges.',
    version=get_version(),
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules = ['anybadge'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=[],
    install_requires=[],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    platform=['any'],
    url='https://github.com/jongracecox/anybadge',
    entry_points = {
        'console_scripts': ['anybadge=anybadge:main'],
    }
)
