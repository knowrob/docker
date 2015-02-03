FROM knowrob/hydro-swi-base
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN echo "Adding repositories...."
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace

# dummy 'add' command to always check out the repositories
ADD ./Dockerfile /home/ros/src/
ADD ./src.tar /home/ros/src/

WORKDIR /home/ros

# copy PR2 meshes into docroot
RUN mkdir -p /home/ros/knowrob/knowrob_vis/html/pr2_description/meshes
RUN cp -r /opt/ros/hydro/share/pr2_description/meshes/* /home/ros/knowrob/knowrob_vis/html/pr2_description/meshes/

# build the catkin workspace
WORKDIR /home/ros
RUN /opt/ros/hydro/bin/catkin_make

ENTRYPOINT /opt/ros/hydro/bin/roslaunch knowrob_roslog_launch knowrob.launch

