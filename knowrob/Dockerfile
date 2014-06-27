FROM knowrob/hydro-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# create user 'ros'
RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros
ENV HOME /home/ros


# install helper packages for ROS

RUN apt-get -y update
RUN apt-get -y install python-yaml python-catkin-pkg python-rospkg emacs swi-prolog-java
RUN apt-get -y install git ros-hydro-iai-common-msgs ros-hydro-rosjava ros-hydro-rosbridge-suite

# ROS environment setup

RUN echo "export LD_LIBRARY_PATH=/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server" >> /home/ros/.bashrc
RUN echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /home/ros/.bashrc
RUN echo source /home/ros/devel/setup.bash >> /home/ros/.bashrc
RUN echo source /home/ros/.bashrc >> /home/ros/.bash_profile


WORKDIR /home/ros
RUN cp /opt/ros/hydro/setup.sh /etc/profile.d/ros_hydro.sh
ENV PYTHONPATH /opt/ros/hydro/lib/python2.7/dist-packages
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace


# check out and setup knowrob
RUN git clone https://github.com/knowrob/knowrob.git -b indigo-devel

# forward ports: KnowRob webserver + rosbridge
EXPOSE 1111 9090


USER ros
ENTRYPOINT /opt/ros/hydro/bin/roslaunch /home/ros/src/knowrob/knowrob_vis/launch/knowrob_vis.launch

