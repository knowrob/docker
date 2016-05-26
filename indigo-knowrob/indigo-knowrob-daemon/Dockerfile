FROM knowrob/indigo-knowrob-base
MAINTAINER Ferenc Balint-Benczedi balintbe@cs.uni-bremen.de

USER root
RUN apt-get -y install texlive-latex-base imagemagick
USER ros
# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN /usr/bin/python /opt/ros/indigo/bin/catkin_init_workspace

# dummy 'add' command to always check out the repositories
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b master
RUN git clone --recursive https://github.com/knowrob/knowrob_addons.git -b master
RUN git clone --recursive https://github.com/knowrob/knowrob_tutorials.git -b master
RUN git clone --recursive https://github.com/code-iai/knowrob_dev.git
RUN git clone https://github.com/code-iai/iai_maps.git
RUN git clone https://github.com/code-iai/iai_common_msgs.git
RUN git clone https://github.com/code-iai/iai_cad_tools.git
WORKDIR /home/ros

ENV OPEN_EASE_APPLICATION true

# build the catkin workspace
RUN /opt/ros/indigo/bin/catkin_make

# ENTRYPOINT /opt/ros/indigo/bin/roslaunch knowrob_roslog_launch knowrob_ease.launch

