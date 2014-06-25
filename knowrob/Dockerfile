FROM knowrob/hydro-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# install rosbridge, rosjava, git etc
run apt-get -y update
RUN apt-get -y install ros-hydro-rosbridge* git ros-hydro-rosjava* ros-hydro-iai-common-msgs


RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros


# ROS environment config
RUN echo "source /home/ros/devel/setup.bash" >> /home/ros/.bashrc
RUN echo "source /.bashrc" >> /.bash_profile


# Create ROS workspace
WORKDIR /home/ros
catkin_init_workspace

RUN git clone https://github.com/hansonrobotics/ros_pololu_servo


ENV HOME /home/ros
USER ros
CMD source

# start rosbridge
#RUN source /opt/ros/hydro/setup.bash
#RUN roslaunch rosbridge_server rosbridge_websocket.launch

# forward ports
EXPOSE 1111 9090

