#!/usr/bin/python
import os
import re
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Attempt to get version number from TravisCI environment variable
version = os.environ.get('TRAVIS_TAG', default='0.0.0')

# Remove leading 'v'
version = re.sub('^v', '', version)

setup(
    name='anybadge',
    description='Simple, flexible badge generator for project badges.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['anybadge', 'anybadge_server'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=[],
    install_requires=['packaging'],
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
