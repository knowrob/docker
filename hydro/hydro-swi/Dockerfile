FROM ubuntu:12.04
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

ARG HOST_IP=172.17.0.1
#ARG ROS_SOURCES="http://packages.ros.org/ros-shadow-fixed/ubuntu"
ARG ROS_SOURCES="http://packages.ros.org.ros.informatik.uni-freiburg.de/ros/ubuntu"
#ARG ROS_SOURCES="http://packages.ros.org/ros/ubuntu"

# Use apt-cacher container
# NOTE: Requires that apt-cacher server was started before build.
RUN echo 'Acquire::http { Proxy "http://'${HOST_IP}':3142"; };' >> /etc/apt/apt.conf.d/01proxy

# Install ROS
RUN apt-get -qq update && \
    apt-get -qq -y install wget apt-utils
RUN sh -c '. /etc/lsb-release && echo "deb ${ROS_SOURCES} precise main" > /etc/apt/sources.list.d/ros-latest.list'
RUN wget http://packages.ros.org/ros.key -O - | apt-key add - && \
    apt-get -qq -y update && \
    apt-get -qq -y install ros-hydro-desktop swi-prolog swi-prolog-java libjson-java \
                           libjson-glib-dev python-yaml python-catkin-pkg python-rospkg \
                           emacs ros-hydro-catkin git ros-hydro-iai-common-msgs \
                           ros-hydro-rosjava ros-hydro-rosbridge-suite ros-hydro-tf2-web-republisher \
                           ros-hydro-mjpeg-server mongodb-clients mongodb-dev libmongo-client-dev \
                           ros-hydro-rosauth mencoder lame libavcodec-extra-53 \
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
RUN cp /opt/ros/hydro/setup.sh /etc/profile.d/ros_hydro.sh && rosdep init

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
    echo "source /opt/ros/hydro/setup.bash" >> /home/ros/.bashrc && \
    echo "source /home/ros/.bashrc" >> /home/ros/.bash_profile

ENV PATH=/home/ros/devel/bin:/opt/ros/hydro/bin:.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games \
    ROS_PACKAGE_PATH=/home/ros/src:/opt/ros/hydro/share:/opt/ros/hydro/stacks \
    CMAKE_PREFIX_PATH=/home/ros/hydro/catkin_ws/devel:/opt/ros/hydro \
    PKG_CONFIG_PATH=/home/ros/devel/lib/pkgconfig:/opt/ros/hydro/lib/pkgconfig \
    ROS_MASTER_URI=http://localhost:11311 \
    ROS_MAVEN_DEPLOYMENT_REPOSITORY=/home/ros/devel/share/maven \
    ROS_MAVEN_PATH=/home/ros/devel/share/maven:/opt/ros/hydro/share/maven \
    ROS_WORKSPACE=/home/ros \
    ROS_IP=127.0.0.1 \
    SWI_HOME_DIR=/usr/lib/swi-prolog \
    PYTHONPATH=/home/ros/devel/lib/python2.7/dist-packages:/opt/ros/hydro/lib/python2.7/dist-packages \
    LD_LIBRARY_PATH=/home/ros/devel/lib:/opt/ros/hydro/lib:/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server:/opt/ros/hydro/lib/python2.7/dist-packages

# Use nexus server that mirrors maven central and ROS repository.
# NOTE: Requires that nexus server was started before build.
ENV ROS_MAVEN_REPOSITORY=http://${HOST_IP}:8081/nexus/content/groups/public
# Configure maven to use the nexus server
RUN mkdir -p /home/ros/.m2
ADD mvn-settings.xml /home/ros/.m2/settings.xml

# Configuration of links and volumes
# TODO: Mount mesh_data read only. Note: Meshes can be generated in knowrob_vis and saved in mesh_data 
ENV DOCKER_LINKS mongo_db:mongo \
    DOCKER_VOLUMES episode_data:ro mesh_data

# Forward ports: webserver + rosbridge
EXPOSE 1111 9090
