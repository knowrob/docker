FROM knowrob/hydro-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# install python and flask
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-pip python-dev wget gcc ros-hydro-pr2-description

RUN pip install Flask Flask-Misaka docker-py
WORKDIR /opt/webapp

## copy this folder to the container
ADD . /opt/webapp/


# copy PR2 meshes into docroot
RUN mkdir -p /opt/webapp/pr2_description/meshes
RUN cp -r /opt/ros/hydro/share/pr2_description/meshes/* /opt/webapp/pr2_description/meshes/


EXPOSE 5000
CMD ["python", "webrob.py"]
