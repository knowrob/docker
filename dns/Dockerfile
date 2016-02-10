FROM ubuntu:12.04
MAINTAINER Daniel Beßler, danielb@tzi.de

RUN apt-get update
RUN apt-get install -y python-all

WORKDIR /
ADD . /

EXPOSE 53
CMD ["python", "dummy-server"]
