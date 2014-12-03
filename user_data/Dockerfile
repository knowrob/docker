FROM ubuntu:12.04
MAINTAINER Moritz Tenorth <knowrob@tenorth.de>

RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros

# Create data directory
RUN mkdir -p /home/ros/user_data
RUN chown -R ros:ros /home/ros

# Create sandbox data volume
VOLUME /home/ros/user_data
