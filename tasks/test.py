import subprocess
from pathlib import Path
from time import sleep

from invoke import task

PROJECT_DIR = Path(__file__).parent.parent
DOCKER_TAG = "test-anybadge:latest"


@task
def local(c):
    """Run local tests."""
    print("Running local tests...")
    subprocess.run(
        "pytest --doctest-modules --cov=anybadge --cov-report html:htmlcov anybadge tests",
        shell=True,
    )


def build_test_docker_image():
    print("Building test docker image... ")
    subprocess.run(f"(cd docker/test && docker build . -t {DOCKER_TAG})", shell=True)


@task
def docker(c):
    """Run dockerised tests."""
    print("Running containerised tests...")

    from tasks.housekeeping import clean
    from tasks.package import build

    clean(c)
    build(c)
    build_test_docker_image()
    subprocess.run(
        f"docker run --rm -v {PROJECT_DIR}:/app {DOCKER_TAG} /work/run_docker_tests.sh",
        shell=True,
    )


@task
def pypi(c, version="latest"):
    """Run tests against Pypi version."""
    print("Running tests against pypi version...")

    from tasks.housekeeping import clean

    clean(c)

    test_files = PROJECT_DIR / Path("test_files")
    test_files.mkdir(exist_ok=True)

    build_test_docker_image()
    print("Running tests in docker image... ")
    subprocess.run(
        f"docker run --rm -e VERSION={version} -v {test_files.absolute()}:/test_files {DOCKER_TAG} /work/run_pypi_tests.sh",
        shell=True,
    )


@task
def cli(c, version="latest"):
    """Run CLI tests against currently installed version."""
    print("Running tests against currently installed version...")

    from tasks.housekeeping import clean

    clean(c)
    test_files = PROJECT_DIR / Path("test_files")
    test_files.mkdir(exist_ok=True)

    shell_test = PROJECT_DIR / Path("docker/test/shell_tests.sh")

    subprocess.run(
        str(shell_test),
        shell=True,
    )
