import subprocess
from pathlib import Path

from invoke import task

PROJECT_DIR = Path(__file__).parent.parent


def run_build():
    subprocess.run(["python", "setup.py", "bdist_wheel"])


@task
def build(c):
    """Build the package and write wheel to 'dist/' directory."""
    print("Building package...")
    run_build()


@task
def install(c):
    """Install the locally built version from 'dist/'."""
    print("Installing package...")
    file_list = list((Path(PROJECT_DIR) / Path("dist")).glob("anybadge-*.whl"))
    if len(file_list) > 1:
        print("Not sure which dist package to install. Clean dist directory first.")
        return
    dist_file = file_list[0]
    print(f"Installing: {dist_file}")
    subprocess.run(["pip", "install", "--force-reinstall", dist_file])
