FROM knowrob/indigo-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# create user 'ros'
RUN useradd -m -d /home/ros -p ros ros && adduser ros sudo && chsh -s /bin/bash ros
RUN echo "ros ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
ENV HOME /home/ros



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# install helper packages for ROS

RUN apt-get -y update
RUN apt-get -y install python-yaml python-catkin-pkg python-rospkg emacs swi-prolog-java ros-indigo-catkin ros-indigo-catkin ros-indigo-ros python-wstool
RUN apt-get -y install git ros-indigo-iai-common-msgs ros-indigo-rosbridge-suite ros-indigo-tf2-web-republisher ros-indigo-mjpeg-server
RUN apt-get -y install mongodb-clients openjdk-7-jdk libbullet-dev ros-indigo-orocos-kdl ros-indigo-xacro ros-indigo-robot-model



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ROS environment setup
RUN cp /opt/ros/indigo/setup.sh /etc/profile.d/ros_indigo.sh
RUN rosdep init

WORKDIR /home/ros
USER ros
RUN chown -R ros:ros /home/ros
RUN rosdep update

RUN echo "export LD_LIBRARY_PATH=/usr/lib/jvm/default-java/jre/lib/amd64:/usr/lib/jvm/default-java/jre/lib/amd64/server" >> /home/ros/.bashrc
RUN echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /home/ros/.bashrc
RUN echo source /home/ros/custom_pkgs/devel/setup.bash >> /home/ros/.bashrc
RUN echo source /home/ros/.bashrc >> /home/ros/.bash_profile



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# set pre-build variables: equiv. to `source /opt/ros/indigo/setup.bash`

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
# set up workspace and install rosjava packages
# 
RUN mkdir -p /home/ros/system_pkgs/src
WORKDIR /home/ros/system_pkgs/src

RUN git clone -b indigo       https://github.com/rosjava/rosjava_build_tools.git
RUN git clone -b indigo       https://github.com/rosjava/rosjava_bootstrap.git
RUN git clone -b indigo-devel https://github.com/ros/genmsg.git
RUN git clone -b indigo-devel https://github.com/ros/gencpp.git
RUN git clone -b indigo-devel https://github.com/ros/genpy.git
RUN git clone -b groovy-devel https://github.com/ros/message_generation.git
RUN git clone -b groovy-devel https://github.com/ros/message_runtime.git
RUN git clone -b indigo       https://github.com/stonier/genjava.git
RUN git clone -b indigo       https://github.com/stonier/rosjava_test_msgs.git
RUN git clone -b indigo       https://github.com/rosjava/rosjava_core.git
RUN git clone -b indigo       https://github.com/rosjava/rosjava_extras.git
RUN git clone -b indigo       https://github.com/rosjava/zeroconf_jmdns_suite.git

# Message dependencies (geometry_experimental is for tf2)
RUN git clone -b indigo-devel https://github.com/ros/ros_comm_msgs.git
RUN git clone -b groovy-devel https://github.com/ros/std_msgs.git
RUN git clone -b indigo-devel https://github.com/ros/common_msgs.git
RUN git clone -b indigo-devel https://github.com/ros/geometry_experimental.git  #tf2
RUN git clone -b indigo-devel https://github.com/ros/ros.git  # test_roslib_comm
RUN git clone -b indigo-devel https://github.com/ros/ros_comm.git  # rosgraph_msgs
# end rosjava repositories

# build the catkin workspace
WORKDIR /home/ros/system_pkgs/
RUN /opt/ros/indigo/bin/catkin_make



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Install KnowRob into a separate workspace to avoid problems with duplicate
# message packages
# 

RUN mkdir -p /home/ros/custom_pkgs/src
WORKDIR /home/ros/custom_pkgs/src

# set post-build variables: equiv. to `source /home/ros/system_pkgs/devel/setup.bash`
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


# dummy 'add' command to always check out the repositories
# ADD ./Dockerfile /home/ros/src/
RUN git clone --recursive https://github.com/knowrob/knowrob.git -b indigo-devel
RUN git clone --recursive https://github.com/knowrob/knowrob_addons.git -b indigo-devel
RUN git clone --recursive https://github.com/code-iai/knowrob_dev.git
RUN git clone https://github.com/code-iai/iai_maps.git
RUN git clone https://github.com/code-iai/iai_common_msgs.git
RUN git clone https://github.com/code-iai/iai_cad_tools.git

# copy PR2 meshes into docroot
# RUN mkdir -p /home/ros/knowrob/knowrob_vis/html/pr2_description/meshes
# RUN cp -r /opt/ros/indigo/share/pr2_description/meshes/* /home/ros/knowrob/knowrob_vis/html/pr2_description/meshes/

# build the catkin workspace
WORKDIR /home/ros/custom_pkgs
RUN /opt/ros/indigo/bin/catkin_make




# forward ports: KnowRob webserver + rosbridge
EXPOSE 1111 9090

# Volumes for mounting data containers
VOLUME /home/ros/knowrob_data
VOLUME /home/ros/sandbox


# ENTRYPOINT /opt/ros/indigo/bin/roslaunch knowrob_vis knowrob_vis.launch

