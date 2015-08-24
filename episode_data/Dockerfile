# NOTE: Must be started with --privileged so that mounting works

FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y curlftpfs

RUN echo "mount_max = 999" >> /etc/fuse.conf 
RUN echo "user_allow_other = 999" >> /etc/fuse.conf 

RUN mkdir /episodes
VOLUME /episodes

ADD mount-episodes.sh /
CMD ["/mount-episodes.sh"]
