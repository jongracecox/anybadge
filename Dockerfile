FROM python:3-alpine

WORKDIR /app

RUN apk update

RUN pip install -U pip && pip install packaging

COPY anybadge/ /app/anybadge/
COPY anybadge_server.py /app/.

ENTRYPOINT ["./anybadge_server.py"]

# Example command to run Docker container
# docker run -it --rm -p8000:8000 -e ANYBADGE_LISTEN_ADDRESS="" -e ANYBADGE_LOG_LEVEL=DEBUG labmonkey/anybadge:1.0
