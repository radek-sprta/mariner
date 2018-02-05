FROM python:alpine

MAINTAINER Radek Sprta <mail@radeksprta.eu>

LABEL eu.radeksprta.schema-version = "1.0" \
      eu.radeksprta.name = "Mariner" \
      eu.radeksprta.description = "Command line torrent searcher" \
      eu.radeksprta.version = "0.0.1" \
      eu.radeksprta.url = "https://radek-sprta.gitlab.io/mariner" \
      eu.radeksprta.vcs-url = "https://gitlab.com/radek-sprta/mariner"

RUN apk add --update \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    && pip3 install mariner

ENTRYPOINT ["mariner"]
