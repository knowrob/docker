FROM openease/easeapp
MAINTAINER Mareike <mareikep@cs.uni-bremen.de>
USER root
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# begin remove
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-scipy python-pip python-dev python-jpype ipython python-tk wget git python-nltk libpq-dev openjdk-7-jre default-jre-headless
RUN update-alternatives --config java

ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/

RUN mkdir /opt/practools
WORKDIR /opt/practools
ADD . opt/practools/
RUN ls -la /opt/practools
RUN ls -la /opt/practools/tools

# create prac apps and set variables
ENV PRAC_HOME /opt/practools/tools/prac
ENV PROBCOG_HOME /opt/practools/tools/pracmln
RUN cd $PROBCOG_HOME && python make_apps.py && source $PROBCOG_HOME/env.sh && cd $PRAC_HOME && python make_apps.py
# end remove

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

## copy this folder to the container
#ADD . /opt/webapp/
ADD webrob /opt/webapp/
ADD init.bash /opt/webapp/
ADD requirements.txt /opt/webapp/


WORKDIR /opt/webapp

# mount point for user_data volume
RUN mkdir /home/ros/user_data
ENV USER_DATA /home/ros/user_data
RUN chown -R ros:ros /home/ros/user_data

RUN update-mime-database /usr/share/mime

RUN chmod +x /opt/webapp/init.bash

USER ros

# EXPOSE 5000

ENTRYPOINT /bin/bash /opt/webapp/init.bash



