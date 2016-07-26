FROM knowrob/hydro-knowrob-base
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN echo "Cloning repositories..."
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace

# dummy 'add' command to always check out the repositories
ADD ./Dockerfile /home/ros/src/
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b master
RUN git clone --recursive https://github.com/knowrob/knowrob_addons.git -b master
RUN git clone --recursive https://github.com/code-iai/knowrob_dev.git -b master
RUN git clone https://github.com/code-iai/iai_maps.git
RUN git clone https://github.com/code-iai/iai_common_msgs.git
RUN git clone https://github.com/code-iai/iai_cad_tools.git
WORKDIR /home/ros

# build the catkin workspace
RUN /opt/ros/hydro/bin/catkin_make

# ENTRYPOINT /opt/ros/hydro/bin/roslaunch knowrob_vis knowrob_vis.launch

