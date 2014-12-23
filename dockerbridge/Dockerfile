FROM ubuntu:12.04
MAINTAINER Moritz Horstmann, mhorst@tzi.de

RUN apt-get update
RUN apt-get install -y python-all python-pip python-dev

RUN pip install python-jsonrpc docker-py

WORKDIR /opt/dockerbridge
ADD . /opt/dockerbridge

EXPOSE 5001
CMD ["python", "dockerbridge.py"]
