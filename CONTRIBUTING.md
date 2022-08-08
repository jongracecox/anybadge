# Contributing to anybadge
I love your input! I want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## I use [Github Flow](https://docs.github.com/en/get-started/quickstart/github-flow), so all code changes happen through pull requests
Pull requests are the best way to propose changes to the codebase (I use
[Github Flow](https://docs.github.com/en/get-started/quickstart/github-flow)). I actively welcome your pull requests:

1. Fork the repo and create your branch from `master`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints (tbc)
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License
When you submit code changes, your submissions are understood to be under the same
[MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers
if that's a concern.

## Report bugs using Github's [issues](https://github.com/jongracecox/anybadge/issues)
I use GitHub issues to track public bugs. Report a bug by
[opening a new issue](https://github.com/jongracecox/anybadge/issues/new/choose).

## Write bug reports with detail, background, and sample code
**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can (ideally sample code that *anyone* with a basic setup can run to reproduce)
- What you expected would happen - (include explanation, screenshot, drawings, etc. to be exact)
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports.

## Use a Consistent Coding Style
Please follow the existing coding style.

## License
By contributing, you agree that your contributions will be licensed under its MIT License.

# Technical stuff

## Pre-commit
This projects makes use of [pre-commit](https://pre-commit.com) to add some safety checks and create consistency
in the project code. When committing changes to this project, please first [install pre-commit](https://pre-commit.com/#install),
then activate it for this project:

```bash
pip install pre-commit
pre-commit install
```

After installing pre-commit to your project (with `pre-commit install`), committing to the project will trigger a series
of checks, and fixers. This process may reject your commit or make changes to your code to bring it into line with the
project standards. For example, [Python black](https://github.com/psf/black) will be used to reformat any code. When
changes are made by these pre-commit hooks you will need to re-add and commit those changes in order for pre-commit to
pass.

Here is some example output from pre-commit:

```
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing tests/test_anybadge.py

fix end of files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing examples/color_teal.svg
```

This shows that two files were updated by hooks, and need to be re-added (with `git add`) before trying to commit again.

## Documentation
The `README.md` file contains a table showing example badges for the different built-in colors. If you modify the
appearance of badges, or the available colors please update the table using the following code:

```python
import anybadge
print("""| Color Name | Hex Code | Example |
| ---------- | -------- | ------- |""")
for color in sorted([c for c in anybadge.colors.Color], key=lambda x: x.name):
    file = 'examples/color_' + color.name.lower() + '.svg'
    url = 'https://cdn.rawgit.com/jongracecox/anybadge/master/' + file
    anybadge.Badge(label='Color', value=color, default_color=color.name.lower()).write_badge(file, overwrite=True)
    print("| {color} | {hex} | ![]({url}) |".format(color=color.name.lower(), hex=color.value.upper(), url=url))
```
