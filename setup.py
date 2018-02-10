#!/usr/bin/python
from setuptools import setup
from mister_bump import bump
from m2r import parse_from_file
import restructuredtext_lint

# Parser README.md into reStructuredText format
rst_readme = parse_from_file('README.md')

# Validate the README, checking for errors
errors = restructuredtext_lint.lint(rst_readme)

# Raise an exception for any errors found
if errors:
    print(rst_readme)
    raise ValueError('README.md contains errors: ',
                     ', '.join([e.message for e in errors]))

setup(
    name='anybadge',
    description='Simple, flexible badge generator for project badges.',
    long_description=rst_readme,
    version=bump(),
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['anybadge'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=[],
    install_requires=[],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    url='https://github.com/jongracecox/anybadge',
    entry_points={
        'console_scripts': ['anybadge=anybadge:main'],
    }
)
