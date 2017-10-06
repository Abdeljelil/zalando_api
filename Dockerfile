FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties sudo
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update && apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv wget

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

# postgres 9.6
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add -
RUN apt-get update
RUN apt-get -y install postgresql postgresql-contrib

COPY . /opt/zalando_api
WORKDIR /opt/zalando_api

RUN make install

EXPOSE 8080
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
