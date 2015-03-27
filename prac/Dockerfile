FROM ubuntu:14.04
MAINTAINER Mareike <mareikep@cs.uni-bremen.de>
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-all 

RUN mkdir /opt/practools
WORKDIR /opt/practools
ADD . opt/practools/

# clone prac and pracmln repos instead of copying them
# RUN git clone https://github.com/danielnyga/prac.git $WORKDIR/tools
# RUN git clone https://github.com/danielnyga/pracmln.git $WORKDIR/tools

# create prac apps and set variables
ENV PRAC_HOME /opt/practools/tools/prac
ENV PROBCOG_HOME /opt/practools/tools/pracmln
RUN cd $PROBCOG_HOME && python make_apps.py && source $PROBCOG_HOME/env.sh && cd $PRAC_HOME && python make_apps.py

VOLUME /opt/practools
