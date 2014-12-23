FROM knowrob/hydro-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# install python and flask
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-pip python-dev wget gcc ros-hydro-pr2-description imagemagick

RUN pip install Flask Flask-Misaka flask-user flask-babel flask-mail psycopg2 python-jsonrpc
WORKDIR /opt/webapp

# work as user 'ros'
RUN groupadd -f -g 999 docker # groupd ID '999' seems to be the docker group normally
RUN useradd -m -d /home/ros -p ros ros && adduser ros docker && chsh -s /bin/bash ros
ENV HOME /home/ros
RUN chown -R ros:ros /opt/webapp/
USER ros

## copy this folder to the container
ADD . /opt/webapp/

# copy PR2 meshes into docroot
RUN mkdir -p /opt/webapp/pr2_description/meshes
RUN cp -r /opt/ros/hydro/share/pr2_description/meshes/* /opt/webapp/pr2_description/meshes/

# Note: robotwebtools does not support loading of tifs as of now (05.12.14).
# The images must be converted to PNG and references in the model file must be updated.
# Convert tif to png
RUN for x in `ls /opt/webapp/pr2_description/meshes/*/*.tif`; do convert $x ${x%.tif}.png; done
# Update image referneces in dae files
# TODO: Seems dae files are loaded from /opt/ros/hydro/share/pr2_description.
#       Update images references there!
RUN for x in `ls /opt/webapp/pr2_description/meshes/*/*.dae`; do sed 's/.tif/.png/g' ${x} > ${x}.new && mv -v ${x}.new ${x}; done

# Expose volumes for maintenance
VOLUME /opt/webapp/

EXPOSE 5000
CMD ["python", "runserver.py"]
