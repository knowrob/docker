FROM knowrob/hydro-swi
 
# install rosbridge
run apt-get update
RUN apt-get install -y ros-hydro-rosbridge*
 
# forward ports
EXPOSE 1111 9090

RUN rosdep init

RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros

RUN echo "source /opt/ros/hydro/setup.bash" >> /home/ros/.bashrc

ENV HOME /home/ros
CMD /bin/bash

# start rosbridge
#RUN source /opt/ros/hydro/setup.bash
#RUN roslaunch rosbridge_server rosbridge_websocket.launch


