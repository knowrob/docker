FROM ubuntu:trusty
MAINTAINER Moritz Tenorth, moritz@tenorth.de

RUN echo 'Acquire::http { Proxy "http://172.17.42.1:3142"; };' >> /etc/apt/apt.conf.d/01proxy
RUN apt-get -y update && apt-get -y install wget apt-utils


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Install ROS
#
RUN sh -c '. /etc/lsb-release && echo "deb http://packages.ros.org.ros.informatik.uni-freiburg.de/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
RUN wget http://packages.ros.org/ros.key -O - | apt-key add -
RUN apt-get -y update && apt-get -y install \
                emacs \
                git \
                libbullet-dev \
                libjson-java \
                libjson-glib-dev \
                mongodb-clients \
                openjdk-7-jdk \
                python-catkin-pkg \
                python-rospkg \
                python-wstool \
                python-yaml \
                ros-indigo-catkin \
                ros-indigo-iai-common-msgs \
                ros-indigo-mjpeg-server \
                ros-indigo-orocos-kdl \
                ros-indigo-robot-model \
                ros-indigo-ros \
                ros-indigo-ros-base \
                ros-indigo-rosbridge-suite \
                ros-indigo-tf2-web-republisher \
                ros-indigo-xacro \
                swi-prolog \
                swi-prolog-java


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create user 'ros'
#
RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros && echo "ros ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
ENV HOME /home/ros


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set up ROS environment
#
RUN cp /opt/ros/indigo/setup.sh /etc/profile.d/ros_indigo.sh
RUN rosdep init

WORKDIR /home/ros
USER ros
RUN chown -R ros:ros /home/ros
RUN rosdep update

RUN echo "export LD_LIBRARY_PATH=/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server" >> /home/ros/.bashrc
RUN echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /home/ros/.bashrc
RUN echo "source /home/ros/custom_pkgs/devel/setup.bash" >> /home/ros/.bashrc
RUN echo "source /home/ros/.bashrc" >> /home/ros/.bash_profile



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Install rosjava from source:
#

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set pre-build variables: equiv. to `source /opt/ros/indigo/setup.bash`
#
ENV CATKIN_SHELL bash
ENV CMAKE_PREFIX_PATH /opt/ros/indigo/
ENV CPATH /opt/ros/indigo/include/
ENV LD_LIBRARY_PATH /opt/ros/indigo/lib:/opt/ros/indigo/lib/x86_64-linux-gnu:/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server
ENV PATH /opt/ros/indigo/bin:.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
ENV PKG_CONFIG_PATH /opt/ros/indigo/lib/pkgconfig:/opt/ros/indigo/lib/x86_64-linux-gnu/pkgconfig
ENV PYTHONPATH /opt/ros/indigo/lib/python2.7/dist-packages/
ENV PYTHON_CODE_BUILD_ROSLISP_PACKAGE_DIRECTORIES "from __future__ import print_function import os env_name = 'CMAKE_PREFIX_PATH' paths = [path for path in os.environ[env_name].split(os.pathsep)] if env_name in os.environ and os.environ[env_name] != '' else [] workspaces = [path for path in paths if os.path.exists(os.path.join(path, '.catkin'))] paths = [] for workspace in workspaces: filename = os.path.join(workspace, '.catkin') data = '' with open(filename) as f: data = f.read() if data: paths.append(os.path.join(workspace, 'share', 'common-lisp')) print(os.pathsep.join(paths))"
ENV PYTHON_CODE_BUILD_ROS_PACKAGE_PATH "from __future__ import print_function import os env_name = 'CMAKE_PREFIX_PATH' paths = [path for path in os.environ[env_name].split(os.pathsep)] if env_name in os.environ and os.environ[env_name] != '' else [] workspaces = [path for path in paths if os.path.exists(os.path.join(path, '.catkin'))] paths = [] for workspace in workspaces: filename = os.path.join(workspace, '.catkin') data = '' with open(filename) as f: data = f.read() if data == '': paths.append(os.path.join(workspace, 'share')) paths.append(os.path.join(workspace, 'stacks')) else: for source_path in data.split(';'): paths.append(source_path) print(os.pathsep.join(paths))"
ENV PYTHON_CODE_BUILD_ROS_PACKAGE_PATH "from __future__ import print_function import os env_name = 'CMAKE_PREFIX_PATH' paths = [path for path in os.environ[env_name].split(os.pathsep)] if env_name in os.environ and os.environ[env_name] != '' else [] workspaces = [path for path in paths if os.path.exists(os.path.join(path, '.catkin'))] paths = [] for workspace in workspaces: filename = os.path.join(workspace, '.catkin') data = '' with open(filename) as f: data = f.read() if data == '': paths.append(os.path.join(workspace, 'share')) paths.append(os.path.join(workspace, 'stacks')) else: for source_path in data.split(';'): paths.append(source_path) print(os.pathsep.join(paths))"
ENV ROS_DISTRO indigo
ENV ROS_ETC_DIR /opt/ros/indigo/etc/ros/
ENV ROS_MASTER_URI http://localhost:11311
ENV ROS_PACKAGE_PATH /opt/ros/indigo/share:/opt/ros/indigo/stacks
ENV ROS_ROOT /opt/ros/indigo/share/ros/
ENV _envfile /opt/ros/indigo/etc/catkin/profile.d/20.transform.bash
ENV _envfile_workspace /opt/ros/indigo
ENV _sav_transform_roscomplete_rosrun _roscomplete_exe



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set up workspace and install rosjava packages
#
RUN mkdir -p /home/ros/system_pkgs/src
WORKDIR /home/ros/system_pkgs/src

RUN wstool init -j4 . https://raw.githubusercontent.com/yujinrobot/yujin_tools/master/rosinstalls/indigo/rosjava.rosinstall

# build the catkin workspace
WORKDIR /home/ros/system_pkgs/
RUN /opt/ros/indigo/bin/catkin_make




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create a separate workspace for custom packages to avoid problems with duplicate
# message packages needed for rosjava
#

RUN mkdir -p /home/ros/custom_pkgs/src
WORKDIR /home/ros/custom_pkgs/src

# set variables: equiv. to `source /home/ros/system_pkgs/devel/setup.bash`

ENV CATKIN_TEST_RESULTS_DIR /home/ros/system_pkgs/build/test_results
ENV CMAKE_PREFIX_PATH /home/ros/system_pkgs/devel:/opt/ros/indigo/
ENV CPATH /home/ros/system_pkgs/devel/include:/opt/ros/indigo/include
ENV LD_LIBRARY_PATH /home/ros/system_pkgs/devel/lib/x86_64-linux-gnu:/opt/ros/indigo/lib/x86_64-linux-gnu:/home/ros/system_pkgs/devel/lib:/opt/ros/indigo/lib:/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server
ENV PATH /opt/ros/indigo/bin:.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
ENV PKG_CONFIG_PATH /opt/ros/indigo/lib/pkgconfig:/opt/ros/indigo/lib/x86_64-linux-gnu/pkgconfig
ENV PYTHONPATH /home/ros/system_pkgs/devel/lib/python2.7/dist-packages:/opt/ros/indigo/lib/python2.7/dist-packages
ENV PYTHON_CODE_BUILD_ROSLISP_PACKAGE_DIRECTORIES "from __future__ import print_function import os env_name = 'CMAKE_PREFIX_PATH' paths = [path for path in os.environ[env_name].split(os.pathsep)] if env_name in os.environ and os.environ[env_name] != '' else [] workspaces = [path for path in paths if os.path.exists(os.path.join(path, '.catkin'))] paths = [] for workspace in workspaces: filename = os.path.join(workspace, '.catkin') data = '' with open(filename) as f: data = f.read() if data: paths.append(os.path.join(workspace, 'share', 'common-lisp')) print(os.pathsep.join(paths))"
ENV PYTHON_CODE_BUILD_ROS_PACKAGE_PATH "from __future__ import print_function import os env_name = 'CMAKE_PREFIX_PATH' paths = [path for path in os.environ[env_name].split(os.pathsep)] if env_name in os.environ and os.environ[env_name] != '' else [] workspaces = [path for path in paths if os.path.exists(os.path.join(path, '.catkin'))] paths = [] for workspace in workspaces: filename = os.path.join(workspace, '.catkin') data = '' with open(filename) as f: data = f.read() if data == '': paths.append(os.path.join(workspace, 'share')) paths.append(os.path.join(workspace, 'stacks')) else: for source_path in data.split(';'): paths.append(source_path) print(os.pathsep.join(paths))"
ENV ROSCONSOLE_CONFIG_FILE /home/ros/system_pkgs/src/ros_comm/tools/rosconsole/config/rosconsole.config
ENV ROS_DISTRO indigo
ENV ROS_ETC_DIR /home/ros/system_pkgs/devel/etc/ros
ENV ROS_MASTER_URI http://localhost:11311
ENV ROS_MAVEN_DEPLOYMENT_REPOSITORY /home/ros/system_pkgs/devel/share/maven
ENV ROS_MAVEN_PATH /home/ros/system_pkgs/devel/share/maven:/opt/ros/indigo/share/maven
ENV ROS_MAVEN_REPOSITORY https://github.com/rosjava/rosjava_mvn_repo/raw/master
ENV ROS_PACKAGE_PATH /home/ros/system_pkgs/src:/opt/ros/indigo/share:/opt/ros/indigo/stacks
ENV ROS_ROOT /home/ros/system_pkgs/src/ros/core/rosbuild
ENV _envfile /home/ros/system_pkgs/devel/etc/catkin/profile.d/20.transform.bash
ENV _envfile_workspace /opt/ros/indigo
ENV _sav_transform_roscomplete_rosrun _roscomplete_exe



# forward ports: KnowRob webserver + rosbridge
EXPOSE 1111 9090

# Volumes for mounting data containers
VOLUME /home/ros/knowrob_data
VOLUME /home/ros/sandbox

