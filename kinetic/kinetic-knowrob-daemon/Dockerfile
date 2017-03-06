FROM openease/kinetic-swi
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

# Initialize the catkin workspace
USER ros
WORKDIR /home/ros/src
RUN /usr/bin/python /opt/ros/kinetic/bin/catkin_init_workspace

RUN echo "Cloning repositories..."
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b kinetic && \
    git clone --recursive https://github.com/knowrob/knowrob_addons.git -b kinetic && \
    git clone https://github.com/code-iai/iai_maps.git && \
    git clone https://github.com/code-iai/iai_common_msgs.git && \
    git clone https://github.com/code-iai/iai_cad_tools.git && \
    git clone https://github.com/RobotWebTools/mjpeg_server.git && \
    git clone https://github.com/RobotWebTools/tf2_web_republisher.git

WORKDIR /home/ros
# Build the catkin workspace
RUN /opt/ros/kinetic/bin/catkin_make

# ENTRYPOINT /opt/ros/kinetic/bin/roslaunch knowrob_roslog_launch knowrob_ease.launch
