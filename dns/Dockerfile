FROM ubuntu
MAINTAINER Daniel Beßler, danielb@tzi.de

RUN apt-get -qq update
RUN apt-get -qq install -y python-all

WORKDIR /
ADD . /

EXPOSE 53
CMD ["python", "dummy-server"]
