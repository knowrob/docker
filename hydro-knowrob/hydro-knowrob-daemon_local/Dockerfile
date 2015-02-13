FROM knowrob/hydro-knowrob-base
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN echo "Adding repositories...."
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace

ADD ./src.tar /home/ros/src/

WORKDIR /home/ros

# build the catkin workspace
WORKDIR /home/ros
RUN /opt/ros/hydro/bin/catkin_make

ENTRYPOINT /opt/ros/hydro/bin/roslaunch knowrob_roslog_launch knowrob.launch

