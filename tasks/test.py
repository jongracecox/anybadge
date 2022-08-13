import subprocess
from pathlib import Path

from invoke import task

PROJECT_DIR = Path(__file__).parent.parent


@task
def local(c):
    """Run local tests."""
    print("Running local tests...")
    subprocess.run(
        "pytest --doctest-modules --cov=anybadge --cov-report html:htmlcov anybadge tests",
        shell=True,
    )


@task
def docker(c):
    """Run dockerised tests."""
    print("Running containerised tests...")

    subprocess.run("invoke clean", shell=True)
    subprocess.run("invoke build", shell=True)
    subprocess.run(
        f"(cd docker/test && docker build . -t test-anybadge:latest)", shell=True
    )
    subprocess.run(
        f"docker run -v {PROJECT_DIR}:/app test-anybadge:latest /work/run_docker_tests.sh",
        shell=True,
    )
