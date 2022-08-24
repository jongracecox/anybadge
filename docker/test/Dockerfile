FROM python:3.10.0

WORKDIR /work

RUN apt update && pip install -U pip
COPY requirements.txt ./
RUN pip install -r ./requirements.txt
COPY run_docker_tests.sh ./
COPY run_pypi_tests.sh ./
COPY helpers.sh ./
COPY shell_tests.sh ./
