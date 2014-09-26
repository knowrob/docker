FROM ubuntu:12.04
MAINTAINER Moritz Tenorth <knowrob@tenorth.de>

# Create data directory
RUN mkdir -p /opt/webapp/db

# copy initial DB to the container
ADD ./webrob.db /opt/webapp/db/

# Create data volume
VOLUME /opt/ros/webapp/db
