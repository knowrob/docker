FROM knowrob/hydro-swi
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

# install python and flask
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-pip python-dev wget gcc imagemagick mongodb libffi-dev

RUN easy_install pymongo
RUN pip install Flask Flask-Misaka flask-user flask-babel flask-mail psycopg2 python-jsonrpc tornado
WORKDIR /opt/webapp

# flag used in nginx configuration
ENV OPEN_EASE_WEBAPP true

# work as user 'ros'
RUN useradd -m -d /home/ros -p ros ros && chsh -s /bin/bash ros
ENV HOME /home/ros

## copy this folder to the container
ADD . /opt/webapp/
RUN chown -R ros:ros /opt/webapp/
  
USER ros

# Expose volumes for maintenance
VOLUME /opt/webapp/

EXPOSE 5000

CMD ["python", "runserver.py"]
