FROM openease/easeapp
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

WORKDIR /opt/webapp
USER ros

ENV DOCKER_LINKS postgres_db:postgres dockerbridge:dockerbridge mongo_db:mongo
ENV DOCKER_VOLUMES user_data mesh_data summary_data episode_data
 
## copy this folder to the container
ADD . /opt/webapp/

CMD ["python", "runserver.py"]
