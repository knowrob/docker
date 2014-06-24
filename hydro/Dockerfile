FROM ubuntu:12.04
 
# ubuntu precise image doesn't have universe repo
run apt-get update
RUN apt-get install -y wget apt-utils
 
# install ROS
RUN sh -c '. /etc/lsb-release && echo "deb http://ros.informatik.uni-freiburg.de/packages/ros/ubuntu precise main" > /etc/apt/sources.list.d/ros-latest.list'
RUN wget http://packages.ros.org/ros.key -O - | apt-key add -
RUN apt-get update
RUN apt-get install -y ros-hydro-desktop swi-prolog swi-prolog-java libjson-java libjson-glib-dev
