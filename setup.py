#!/usr/bin/python
import os
import re
from setuptools import setup
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

# Attempt to get version number from TravisCI environment variable
version = os.environ.get('TRAVIS_TAG', default='0.0.0')

# Remove leading 'v'
version = re.sub('^v', '', version)

setup(
    name='anybadge',
    description='Simple, flexible badge generator for project badges.',
    long_description=rst_readme,
    version=version,
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['anybadge', 'anybadge_server'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=['unittest'],
    install_requires=[],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    url='https://github.com/jongracecox/anybadge',
    entry_points={
        'console_scripts': ['anybadge=anybadge:main',
                            'anybadge-server=anybadge_server:main'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
