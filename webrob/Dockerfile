FROM knowrob/hydro-swi
MAINTAINER Moritz Tenorth, moritz@tenorth.de

# install python and flask
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-pip python-dev wget gcc imagemagick

RUN pip install Flask Flask-Misaka docker-py flask-user flask-babel flask-mail psycopg2
WORKDIR /opt/webapp

# work as user 'ros'
RUN groupadd -f -g 999 docker # groupd ID '999' seems to be the docker group normally
RUN useradd -m -d /home/ros -p ros ros && adduser ros docker && chsh -s /bin/bash ros
ENV HOME /home/ros
RUN chown -R ros:ros /opt/webapp/
  
USER ros

## copy this folder to the container
ADD . /opt/webapp/
# Expose volumes for maintenance
VOLUME /opt/webapp/

EXPOSE 5000
CMD ["python", "runserver.py"]
