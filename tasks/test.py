import subprocess
from pathlib import Path

from invoke import task

from tasks.housekeeping import clean

PROJECT_DIR = Path(__file__).parent.parent


@task
def local(c):
    """Run local tests."""
    print("Running local tests...")
    subprocess.run(
        "pytest --doctest-modules --cov=anybadge --cov-report html:htmlcov anybadge tests",
        shell=True,
    )


def build_test_docker_image():
    subprocess.run(
        f"(cd docker/test && docker build . -t test-anybadge:latest)", shell=True
    )


@task
def docker(c):
    """Run dockerised tests."""
    print("Running containerised tests...")

    subprocess.run("invoke clean", shell=True)
    subprocess.run("invoke build", shell=True)
    build_test_docker_image()
    subprocess.run(
        f"docker run -v {PROJECT_DIR}:/app test-anybadge:latest /work/run_docker_tests.sh",
        shell=True,
    )


@task
def pypi(c, version="latest"):
    """Run tests against Pypi version."""
    print("Running tests against pypi version...")

    clean(c)
    test_files = PROJECT_DIR / Path("test_files")
    test_files.mkdir(exist_ok=True)

    build_test_docker_image()
    subprocess.run(
        f"docker run -e VERSION={version} -v {test_files.absolute()}:/test_files test-anybadge:latest /work/run_pypi_tests.sh",
        shell=True,
    )
