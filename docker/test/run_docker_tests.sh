#!/bin/bash

echo "Running tests..."
mkdir tmp && cd tmp
mkdir tests
pip install /app/dist/anybadge*.whl
pytest --doctest-modules --cov=anybadge --cov-report html:htmlcov /app/anybadge /app/tests
