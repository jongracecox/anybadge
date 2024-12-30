"""Invoke tasks for the project."""

import glob
import os
import subprocess
from pathlib import Path

from invoke import task, Collection
from tasks import test, server, housekeeping, colors, package

PROJECT_DIR = Path(__file__).parent.parent

os.chdir(PROJECT_DIR)


@task
def examples(c):
    """Generate examples markdown."""
    print("Generating examples markdown...")
    from build_examples import main

    main()


namespace = Collection(test, server, housekeeping, colors, package)
for fn in [examples]:
    namespace.add_task(fn)
