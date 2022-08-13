import subprocess

from invoke import task


@task
def docker_build(c):
    """Build docker image for anybadge server."""
    print("Building Docker image...")
    subprocess.run("docker build . -t anybadge:latest", shell=True)


@task
def docker_run(c, port=8000):
    """Run containerised anybadge server."""
    print("Running server in Docker container...")
    subprocess.run(
        f"docker run -it --rm -p{port}:{port}/tcp anybadge:latest --port={port}",
        shell=True,
    )


@task
def run(c, port=8000):
    """Run local anybadge server."""
    print("Running server locally...")
    subprocess.run(f"python3 anybadge_server.py --port={port}", shell=True)
