FROM ubuntu:12.04

run apt-get update
RUN apt-get install -y wget apt-utils
 
# install ROS
RUN sh -c '. /etc/lsb-release && echo "deb http://packages.ros.org.ros.informatik.uni-freiburg.de/ros/ubuntu precise main" > /etc/apt/sources.list.d/ros-latest.list'
#RUN sh -c '. /etc/lsb-release && echo "deb http://packages.ros.org/ros/ubuntu precise main" > /etc/apt/sources.list.d/ros-latest.list' 
RUN wget http://packages.ros.org/ros.key -O - | apt-key add - && \
    apt-get update && \
    apt-get install -y ros-hydro-desktop swi-prolog swi-prolog-java libjson-java libjson-glib-dev
