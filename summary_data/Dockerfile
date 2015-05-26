FROM ubuntu:12.04
MAINTAINER Asil Kaan Bozcuoglu <asil@tzi.de>

RUN apt-get -y update
RUN apt-get -y install git wget tar

RUN mkdir -p /home/ros/summary_data

WORKDIR /home/ros/summary_data
RUN wget "https://www.dropbox.com/s/x622c5wyt9ikoos/video.tar"
RUN /bin/tar -xvf video.tar

VOLUME /home/ros/summary_data
