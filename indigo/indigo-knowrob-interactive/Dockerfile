FROM openease/indigo-swi
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

# Initialize the catkin workspace
USER ros
WORKDIR /home/ros/src
RUN /usr/bin/python /opt/ros/indigo/bin/catkin_init_workspace

RUN echo "Cloning repositories..."
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b master && \
    git clone --recursive https://github.com/knowrob/knowrob_addons.git -b master && \
    git clone --recursive https://github.com/code-iai/knowrob_dev.git -b master && \
    git clone https://github.com/code-iai/iai_maps.git && \
    git clone https://github.com/code-iai/iai_common_msgs.git && \
    git clone https://github.com/code-iai/iai_cad_tools.git

WORKDIR /home/ros
# Build the catkin workspace
RUN /opt/ros/indigo/bin/catkin_make

# ENTRYPOINT /opt/ros/indigo/bin/roslaunch knowrob_vis knowrob_vis.launch
