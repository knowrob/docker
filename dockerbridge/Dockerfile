FROM ubuntu:12.04
MAINTAINER Moritz Horstmann, mhorst@tzi.de

RUN apt-get -qq update
RUN apt-get -qq install -y python-all python-pip python-dev

RUN pip install python-jsonrpc docker-py

WORKDIR /opt/dockerbridge
ADD . /opt/dockerbridge

EXPOSE 5001
CMD ["python", "dockerbridge.py"]
