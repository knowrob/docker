FROM knowrob/hydro-knowrob-base
MAINTAINER Moritz Tenorth, moritz@tenorth.de
USER root
RUN apt-get -y update && apt-get -y install openjdk-7-jdk texlive-latex-base imagemagick
RUN update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/bin/java" 1 && \
	update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin/javac" 1 && \
	update-alternatives --set java "/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/bin/java" && \
	update-alternatives --set javac "/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin/javac"
USER ros
# set up workspace and setup knowrob
WORKDIR /home/ros/src

RUN echo "Adding repositories...."
RUN /usr/bin/python /opt/ros/hydro/bin/catkin_init_workspace

ADD ./src.tar /home/ros/src/

WORKDIR /home/ros/src/knowrob/knowrob_vis

# Need write permissions for 'ros' user for generating JAVA classes with xjc
USER root
RUN chown -R ros /home/ros/src/
USER ros

WORKDIR /home/ros

ENV OPEN_EASE_APPLICATION true

# build the catkin workspace
RUN /opt/ros/hydro/bin/catkin_make

VOLUME /home/ros/summary_data
