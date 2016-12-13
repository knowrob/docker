FROM openease/hydro-swi
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

# Initialize the catkin workspace
USER ros
WORKDIR /home/ros/src
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace

RUN echo "Adding repositories...."
ADD ./src.tar /home/ros/src/

WORKDIR /home/ros
# Build the catkin workspace
RUN /opt/ros/hydro/bin/catkin_make
