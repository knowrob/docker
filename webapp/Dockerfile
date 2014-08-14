FROM ubuntu:12.04
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# install python and flask
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-pip python-dev wget gcc


RUN pip install Flask Flask-Misaka docker-py

WORKDIR /opt/webapp


# copy this file to the container
ADD . /opt/webapp/

EXPOSE 5000
CMD ["python", "webrob.py"]
