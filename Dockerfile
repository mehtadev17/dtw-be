FROM python:3.7-alpine

COPY entrypoint /entrypoint
RUN apk add --no-cache --update \
     dumb-init \
     gcc \
     musl-dev \
     libc-dev \
     linux-headers \
     postgresql-dev \
     python3-dev \
     && chmod +x /entrypoint

WORKDIR /app

COPY ./dtw/. /app
RUN pip install -r /app/requirements.txt

EXPOSE 8080
ENTRYPOINT ["/entrypoint"]
