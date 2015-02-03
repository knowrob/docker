FROM knowrob/hydro-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# Use apt-cacher container
RUN echo 'Acquire::http { Proxy "http://172.17.42.1:3142"; };' >> /etc/apt/apt.conf.d/01proxy

# install helper packages for ROS
RUN apt-get -y install python-yaml python-catkin-pkg python-rospkg emacs ros-hydro-catkin git ros-hydro-iai-common-msgs \
                       ros-hydro-rosjava ros-hydro-rosbridge-suite ros-hydro-tf2-web-republisher ros-hydro-mjpeg-server ros-hydro-pr2-description \
                       mongodb-clients

# create user 'ros'
RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros
ENV HOME /home/ros

# ROS environment setup
RUN cp /opt/ros/hydro/setup.sh /etc/profile.d/ros_hydro.sh && rosdep init

WORKDIR /home/ros
USER ros
RUN mkdir /home/ros/src && chown -R ros:ros /home/ros && rosdep update

RUN echo "export LD_LIBRARY_PATH=/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server" >> /home/ros/.bashrc && \
    echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /home/ros/.bashrc && \
    echo source /home/ros/devel/setup.bash >> /home/ros/.bashrc && \
    echo source /home/ros/.bashrc >> /home/ros/.bash_profile

# set pre-build variables: only packages in /opt/ros
ENV PATH /home/ros/devel/bin:/opt/ros/hydro/bin:.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# set post-build variables:
ENV ROS_PACKAGE_PATH /home/ros/src:/opt/ros/hydro/share:/opt/ros/hydro/stacks
ENV CMAKE_PREFIX_PATH /home/ros/hydro/catkin_ws/devel:/opt/ros/hydro
ENV PKG_CONFIG_PATH /home/ros/devel/lib/pkgconfig:/opt/ros/hydro/lib/pkgconfig
ENV ROS_MASTER_URI http://localhost:11311
ENV ROS_MAVEN_DEPLOYMENT_REPOSITORY /home/ros/devel/share/maven
ENV ROS_MAVEN_PATH /home/ros/devel/share/maven:/opt/ros/hydro/share/maven
ENV ROS_MAVEN_REPOSITORY https://github.com/rosjava/rosjava_mvn_repo/raw/master
ENV ROS_WORKSPACE /home/ros
ENV ROS_IP 127.0.0.1
ENV LD_LIBRARY_PATH /home/ros/devel/lib:/opt/ros/hydro/lib:/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server:/opt/ros/hydro/lib/python2.7/dist-packages
ENV SWI_HOME_DIR /usr/lib/swi-prolog
ENV PYTHONPATH /home/ros/devel/lib/python2.7/dist-packages:/opt/ros/hydro/lib/python2.7/dist-packages

# forward ports: KnowRob webserver + rosbridge
EXPOSE 1111 9090

# Volumes for mounting data containers
VOLUME /home/ros/knowrob_data
VOLUME /home/ros/sandbox
