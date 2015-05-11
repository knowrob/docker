FROM openease/easeapp
MAINTAINER Mareike Picklum, mareikep@cs.uni-bremen.de
USER root

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-support python-scipy python-pip python-dev python-jpype ipython python-tk wget git python-nltk libpq-dev openjdk-7-jre default-jre-headless
RUN update-java-alternatives --jre -s java-1.7.0-openjdk-amd64
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
ENV PATH $JAVA_HOME/bin:$PATH

ENV DOCKER_LINKS postgres_db:postgres dockerbridge:dockerbridge
ENV DOCKER_VOLUMES user_data prac_tools

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /opt/webapp
USER ros
ADD . /opt/webapp/

ENTRYPOINT /bin/bash /opt/webapp/init.bash

