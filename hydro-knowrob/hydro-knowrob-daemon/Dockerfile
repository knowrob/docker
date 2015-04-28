FROM knowrob/hydro-knowrob-base
MAINTAINER Moritz Tenorth, moritz@tenorth.de
USER root
RUN apt-get -y install openjdk-7-jdk texlive-latex-base imagemagick
RUN update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/bin/java" 1 && \
	update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin/javac" 1 && \
	update-alternatives --set java "/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/bin/java" && \
	update-alternatives --set javac "/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin/javac"
USER ros
# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN echo "Cloning repositories..."
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace

# dummy 'add' command to always check out the repositories
#ADD ./Dockerfile /
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b indigo-devel
RUN git clone --recursive https://github.com/knowrob/knowrob_addons.git -b indigo-devel
RUN git clone --recursive https://github.com/code-iai/knowrob_dev.git
RUN git clone https://github.com/code-iai/iai_maps.git
RUN git clone https://github.com/code-iai/iai_common_msgs.git
RUN git clone https://github.com/code-iai/iai_cad_tools.git
WORKDIR /home/ros

ENV OPEN_EASE_APPLICATION true

# build the catkin workspace
RUN /opt/ros/hydro/bin/catkin_make

ENTRYPOINT /opt/ros/hydro/bin/roslaunch knowrob_roslog_launch knowrob_ease.launch
