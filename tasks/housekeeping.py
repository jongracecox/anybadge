import glob
import subprocess
from invoke import task


def delete_files(files: str):
    for file in glob.glob(files):
        print(f"  Deleting {file}")
        subprocess.run(["rm", "-rf", file])


@task
def clean(c):
    """Clean up the project area."""
    print("Cleaning the project directory...")
    delete_files("dist/*")
    delete_files("tests/test_*.svg")
    delete_files("test_files/*")
