FROM ubuntu:14.04
MAINTAINER Ferenc Balint-Benczedi

RUN apt-get -qq update && apt-get -qq install -y wget apt-utils


# Install ROS
RUN sh -c '. /etc/lsb-release && echo "deb http://packages.ros.org.ros.informatik.uni-freiburg.de/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
RUN wget http://packages.ros.org/ros.key -O - | apt-key add - && \
    apt-get -y update && apt-get -y install \
                
                libjson-java \
                libjson-glib-dev \
                mongodb-clients \
                ros-indigo-desktop \
                swi-prolog \
                swi-prolog-java