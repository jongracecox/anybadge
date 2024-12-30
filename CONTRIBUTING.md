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

Please follow the existing coding style. Your code should be standardised using
[Python Black](https://github.com/psf/black) using pre-commit when you make commits - please ensure you have
pre-commit installed (see [here](#install-pre-commit)).

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

# Development environment

Setup your development environment with the following steps:

- [Check out the project](#check-out-the-project)
- [Install build requirements](#install-build-requirements)
- [Install pre-commit](#install-pre-commit)

## Check out the project

Clone the project:

```bash
git clone https://github.com/jongracecox/anybadge.git
```

## Install build requirements

Install build requirements with:

```bash
pip install -r build-requirements.txt
```

## Install pre-commit

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

# Development activities

## Invoke

The project has some [Python invoke](https://www.pyinvoke.org/) tasks to help automate things. After installing
build requirements you can run `inv --list` to see a list of available tasks.

For example:

```
> inv --list
Available tasks:

  examples              Generate examples markdown.
  colors.update         Generate colors Enum from Mozilla color keywords.
  housekeeping.clean    Clean up the project area.
  package.build         Build the package and write wheel to 'dist/' directory.
  package.install       Install the locally built version from 'dist/'.
  server.docker-build   Build docker image for anybadge server.
  server.docker-run     Run containerised anybadge server.
  server.run            Run local anybadge server.
  test.cli              Run CLI tests against currently installed version.
  test.docker           Run dockerised tests.
  test.local            Run local tests.
  test.pypi             Run tests against Pypi version.
```

You can get help for a command using `inv --help <command>`.

Invoke tasks are defined in the `tasks/` directory in the project. Feel free to add new and useful tasks.

## Running tests

### Local tests

You can run tests locally using:

```bash
inv package.build && inv package.install && inv test.local
```

### Containerised tests

When running locally, you will be running tests against the code in the project. This has some disadvantages,
specifically running locally may not detect files that are not included in the package build, e.g. sub-modules,
templates, examples, etc. For this reason we have a containerised test. This can be run using:

```bash
inv test.docker
```

This will clean up the project `dist` directory, build the package locally, build the docker image,
spin up a docker container, install the package and run the tests. The tests should run using the installed
package and not the project source code, so this method should be used as a final test before pushing.

### PyPi tests

It is useful to validate PyPi releases when a new version is deployed. This should be done after every
release.

#### Running tests

To test the latest available PyPi package, run:

```bash
inv test.pypi
```

To test a specific version of a PyPi package, run:

```bash
inv test.pypi --version=<VERSION>
```

When the tests run they will output test files into a `<VERSION>_<DATETIME>` directory under `test_files/`.
After running tests, inspect the console output to see if there were any errors then inspect each file in the
`test_files` directory.

#### Adding tests

The PyPi tests are implemented in `docker/test/shell_tests.sh`. If you find a bug, then adding a test to this script
could be useful, and quicker than adding a unittest.

### CLI tests

To run the CLI tests that execute as part of the `inv test.pypi` against a local install you can use:

```bash
inv test.cli
```

If you would like to build, install and run the cli tests against a local install (which can be useful when editing
CLI code), you can use:

```bash
inv package.build && inv package.install && inv test.cli
```

Note that this will force install the built wheel from the project `dist/` directory over any existing local install.

### Tox tests

To run tox tests against all supported Python versions:

```bash
pip install tox
tox
```

## Documentation

The `README.md` file contains a table showing example badges for the different built-in colors. If you modify the
appearance of badges, or the available colors please update the table using the invoke task:

```bash
inv examples
```

## Color enumeration

The `anybadge.colors.Color` enum provides an easy way to specify badge colors. The enum
can be updated with new definitions from Mozilla by running `inv colors.update`. This will
download and parse the Mozilla color keywords table, combine it with existing colors in the
Enum (maintaining all old values and using numbered suffixes for new values), and generate new
Enum code that can be copied into the `colors.py` module.

After updating the module the example badges must be re-generated, and the table added to the
`README.md` document (see [here](#documentation)).
