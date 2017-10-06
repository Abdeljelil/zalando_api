FROM ubuntu:16.04

ENV LANG en_US.utf8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apt-get update && apt-get install -y software-properties-common locales wget sudo
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
RUN locale-gen en_US.UTF-8

RUN apt-get update && apt-get install -y build-essential python3.6 python3.6-dev \ 
    python3-pip python3.6-venv python-software-properties postgresql-9.6

# update pip
RUN python3.6 -m pip install pip --upgrade && python3.6 -m pip install wheel

COPY . /opt/zalando_api
WORKDIR /opt/zalando_api

RUN make install

EXPOSE 8080
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
