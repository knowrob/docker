FROM ubuntu:14.04
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de	

ARG HOST_IP=172.17.0.1
ARG ROS_SOURCES="http://packages.ros.org/ros/ubuntu"

# Use apt-cacher container
# NOTE: Requires that apt-cacher server was started before build.
RUN echo 'Acquire::http { Proxy "http://'${HOST_IP}':3142"; };' >> /etc/apt/apt.conf.d/01proxy

# Install ROS
RUN apt-get -qq update && \
    apt-get -qq -y install wget apt-utils
RUN sh -c '. /etc/lsb-release && echo "deb ${ROS_SOURCES} $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
    apt-get -qq -y update && \
    apt-get -qq -y install ros-indigo-desktop swi-prolog swi-prolog-java libjson-java \
                           libjson-glib-dev python-yaml python-catkin-pkg python-rospkg \
                           emacs ros-indigo-catkin git ros-indigo-iai-common-msgs \
                           ros-indigo-rosjava ros-indigo-rosbridge-suite ros-indigo-tf2-web-republisher \
                           ros-indigo-mjpeg-server mongodb-clients mongodb-dev libmongo-client-dev \
                           ros-indigo-rosauth mencoder lame libavcodec-extra-54 \
                           openjdk-7-jdk texlive-latex-base imagemagick && \
    apt-get -qq -y autoremove && \
    apt-get -qq -y clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*
RUN update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/bin/java" 1 && \
    update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin/javac" 1 && \
    update-alternatives --set java "/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/bin/java" && \
    update-alternatives --set javac "/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin/javac"
# ROS environment setup
RUN cp /opt/ros/indigo/setup.sh /etc/profile.d/ros_indigo.sh && rosdep init

# Create user 'ros'
RUN useradd -m -d /home/ros -p ros ros && \
    adduser ros sudo && \
    chsh -s /bin/bash ros
ENV HOME /home/ros
WORKDIR /home/ros
# Switch to the new user 'ros'
USER ros
RUN mkdir /home/ros/src && \
    chown -R ros:ros /home/ros && \
    rosdep update

RUN echo "export LD_LIBRARY_PATH=/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server" >> /home/ros/.bashrc && \
    echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /home/ros/.bashrc && \
    echo "source /opt/ros/indigo/setup.bash" >> /home/ros/.bashrc && \
    echo "source /home/ros/.bashrc" >> /home/ros/.bash_profile

# set pre-build variables: only packages in /opt/ros
ENV PATH /home/ros/devel/bin:/opt/ros/indigo/bin:.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

ENV PATH=/home/ros/devel/bin:/opt/ros/indigo/bin:.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
ENV ROS_PACKAGE_PATH=/home/ros/src:/opt/ros/indigo/share:/opt/ros/indigo/stacks
ENV CMAKE_PREFIX_PATH=/home/ros/indigo/catkin_ws/devel:/opt/ros/indigo
ENV PKG_CONFIG_PATH=/home/ros/devel/lib/pkgconfig:/opt/ros/indigo/lib/pkgconfig
ENV ROS_MASTER_URI=http://localhost:11311
ENV ROS_MAVEN_DEPLOYMENT_REPOSITORY=/home/ros/devel/share/maven
ENV ROS_MAVEN_PATH=/home/ros/devel/share/maven:/opt/ros/indigo/share/maven
ENV ROS_WORKSPACE=/home/ros
ENV ROS_IP=127.0.0.1
ENV SWI_HOME_DIR=/usr/lib/swi-prolog
ENV PYTHONPATH=/home/ros/devel/lib/python2.7/dist-packages:/opt/ros/indigo/lib/python2.7/dist-packages
ENV LD_LIBRARY_PATH=/home/ros/devel/lib:/opt/ros/indigo/lib:/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server:/opt/ros/indigo/lib/python2.7/dist-packages

# Use nexus server that mirrors maven central and ROS repository.
# NOTE: Requires that nexus server was started before build.
ENV ROS_MAVEN_REPOSITORY=http://${HOST_IP}:8081/nexus/content/groups/public
# Configure maven to use the nexus server
RUN mkdir -p /home/ros/.m2
ADD mvn-settings.xml /home/ros/.m2/settings.xml

# Configuration of links and volumes
# TODO: Mount mesh_data read only. Note: Meshes can be generated in knowrob_vis and saved in mesh_data 
ENV DOCKER_LINKS mongo_db:mongo
ENV DOCKER_VOLUMES episode_data:ro mesh_data

# Forward ports: webserver + rosbridge
EXPOSE 1111 9090
