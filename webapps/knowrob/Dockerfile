FROM openease/easeapp
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

WORKDIR /opt/webapp
USER ros

## copy this folder to the container
ADD . /opt/webapp/

CMD ["python", "runserver.py"]
