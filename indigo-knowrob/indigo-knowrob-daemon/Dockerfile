FROM knowrob/indigo-knowrob-base
MAINTAINER Ferenc Balint-Benczedi balintbe@cs.uni-bremen.de

USER ros
# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN /usr/bin/python /opt/ros/indigo/bin/catkin_init_workspace

# dummy 'add' command to always check out the repositories
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b master && \
    git clone --recursive https://github.com/knowrob/knowrob_addons.git -b master && \
    git clone --recursive https://github.com/knowrob/knowrob_tutorials.git -b master && \
    git clone --recursive https://github.com/code-iai/knowrob_dev.git && \
    git clone https://github.com/code-iai/iai_maps.git && \
    git clone https://github.com/code-iai/iai_common_msgs.git && \
    git clone https://github.com/code-iai/iai_cad_tools.git && \
    git clone https://github.com/bbferka/robosherlock.git

WORKDIR /home/ros

ENV OPEN_EASE_APPLICATION true

# build the catkin workspace
RUN /opt/ros/indigo/bin/catkin_make

#RUN ln -s /dev/null /dev/raw1394

# ENTRYPOINT /opt/ros/indigo/bin/roslaunch knowrob_roslog_launch knowrob_ease.launch

