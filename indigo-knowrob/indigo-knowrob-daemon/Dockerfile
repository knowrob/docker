FROM knowrob/indigo-knowrob-base
MAINTAINER Ferenc Balint-Benczedi balintbe@cs.uni-bremen.de

USER root
RUN mkdir /home/ros/.ssh/
ADD rs_openease /home/ros/.ssh/id_rsa
RUN touch /home/ros/.ssh/known_hosts && \
    ssh-keyscan -T 60 github.com >> /home/ros/.ssh/known_hosts && \
    chown -R ros:ros /home/ros/.ssh 
    
    
USER ros
# set up workspace and setup knowrob
WORKDIR /home/ros/src
RUN /usr/bin/python /opt/ros/indigo/bin/catkin_init_workspace
   

# dummy 'add' command to always check out the repositories
RUN git clone git@github.com:code-iai/robosherlock_demos.git && \
    git clone --recursive https://github.com/knowrob/knowrob.git -b master && \
    git clone --recursive https://github.com/knowrob/knowrob_addons.git -b master && \
    git clone --recursive https://github.com/knowrob/knowrob_tutorials.git -b master && \
    git clone --recursive https://github.com/code-iai/knowrob_dev.git && \
    git clone https://github.com/code-iai/iai_maps.git && \
    git clone https://github.com/code-iai/iai_common_msgs.git && \
    git clone https://github.com/code-iai/iai_cad_tools.git && \
    git clone https://github.com/code-iai/designator_integration && \
    git clone https://github.com/bbferka/robosherlock.git && \
    git clone https://github.com/bbferka/rs_addons.git && \
    git clone https://github.com/bbferka/rs_turn_table.git && \
    git clone https://github.com/code-iai/rs_resources.git && \
    git clone git@github.com:code-iai/rs_kbreasoning.git -b acat_demo && \
    /home/ros/local/src/caffe/scripts/download_model_binary.py /home/ros/src/rs_resources/caffe/models/bvlc_reference_caffenet/

WORKDIR /home/ros

ENV OPEN_EASE_APPLICATION true

# build the catkin workspace
RUN /opt/ros/indigo/bin/catkin_make

# ENTRYPOINT /opt/ros/indigo/bin/roslaunch knowrob_roslog_launch knowrob_ease.launch

