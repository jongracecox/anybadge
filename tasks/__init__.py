"""Invoke tasks for the project."""
import glob
import os
import subprocess
from pathlib import Path

from invoke import task, Collection
from tasks import test, server

PROJECT_DIR = Path(__file__).parent.parent

os.chdir(PROJECT_DIR)


@task
def build(c):
    """Build the package."""
    print("Building package...")
    subprocess.run(["python", "setup.py", "bdist_wheel"])


@task
def examples(c):
    """Generate examples markdown."""
    print("Generating examples markdown...")
    from build_examples import main

    main()


def delete_files(files: str):
    for file in glob.glob(files):
        print(f"  Deleting {file}")
        subprocess.run(["rm", "-rf", file])


@task()
def clean(c):
    """Clean up the project area."""
    print("Cleaning the project directory...")
    delete_files("dist/*")
    delete_files("tests/test_*.svg")


namespace = Collection(test, server)
for fn in [build, examples, clean]:
    namespace.add_task(fn)
