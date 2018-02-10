#!/usr/bin/python
from setuptools import setup
from mister_bump import bump

setup(
    name='anybadge',
    description='Simple, flexible badge generator for project badges.',
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
    platform=['any'],
    url='https://github.com/jongracecox/anybadge',
    entry_points={
        'console_scripts': ['anybadge=anybadge:main'],
    }
)
