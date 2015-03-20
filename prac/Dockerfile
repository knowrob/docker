FROM ubuntu:14.04
MAINTAINER Mareike <mareikep@cs.uni-bremen.de>
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
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

# clone prac and pracmln repos
# RUN git clone https://github.com/danielnyga/prac.git $WORKDIR
# RUN git clone https://github.com/danielnyga/pracmln.git $WORKDIR


VOLUME ["/opt/practools"]
ENTRYPOINT /bin/bash /opt/practools/init.bash
