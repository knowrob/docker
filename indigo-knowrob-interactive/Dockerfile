FROM knowrob/indigo-swi-rosjava
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# ensure to be in the right working directory:
WORKDIR /home/ros/custom_pkgs/src

# dummy 'add' command to always check out the repositories
# ADD ./Dockerfile /home/ros/src/
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b indigo-devel
RUN git clone --recursive https://github.com/knowrob/knowrob_addons.git -b indigo-devel
RUN git clone --recursive https://github.com/code-iai/knowrob_dev.git
RUN git clone https://github.com/code-iai/iai_maps.git
RUN git clone https://github.com/code-iai/iai_common_msgs.git
RUN git clone https://github.com/code-iai/iai_cad_tools.git

# copy PR2 meshes into docroot
# RUN mkdir -p /home/ros/knowrob/knowrob_vis/html/pr2_description/meshes
# RUN cp -r /opt/ros/indigo/share/pr2_description/meshes/* /home/ros/knowrob/knowrob_vis/html/pr2_description/meshes/

# build the catkin workspace
WORKDIR /home/ros/custom_pkgs
RUN /opt/ros/indigo/bin/catkin_make



# ENTRYPOINT /opt/ros/indigo/bin/roslaunch knowrob_vis knowrob_vis.launch

