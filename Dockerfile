FROM python:3-stretch

WORKDIR /app

RUN apt-get update

COPY anybadge.py anybadge_server.py ./

ENTRYPOINT ./anybadge_server.py

# Example command to run Docker container
# docker run -it --rm -p8000:8000 -e ANYBADGE_LISTEN_ADDRESS="" -e ANYBADGE_LOG_LEVEL=DEBUG labmonkey/anybadge:1.0
