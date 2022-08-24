"""Invoke tasks for the project."""
import glob
import os
import subprocess
from pathlib import Path

from invoke import task, Collection
from tasks import test, server, housekeeping, colors

PROJECT_DIR = Path(__file__).parent.parent

os.chdir(PROJECT_DIR)


@task
def build(c):
    """Build the package."""
    print("Building package...")
    subprocess.run(["python", "setup.py", "bdist_wheel"])


@task
def install(c):
    """Install the locally built version from dist."""
    print("Installing package...")
    file_list = list((Path(PROJECT_DIR) / Path("dist")).glob("anybadge-*.whl"))
    if len(file_list) > 1:
        print("Not sure which dist package to install. Clean dist directory first.")
        return
    dist_file = file_list[0]
    print(f"Installing: {dist_file}")
    subprocess.run(["pip", "install", "--force-reinstall", dist_file])


@task
def examples(c):
    """Generate examples markdown."""
    print("Generating examples markdown...")
    from build_examples import main

    main()


namespace = Collection(test, server, housekeeping, colors)
for fn in [build, examples, install]:
    namespace.add_task(fn)
