FROM openease/easeapp
MAINTAINER Mareike Picklum, mareikep@cs.uni-bremen.de
USER root
# RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-scipy python-jpype python-tk git python-nltk libpq-dev openjdk-7-jre default-jre-headless
RUN update-alternatives --config java

ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /opt/webapp
USER ros
ADD . /opt/webapp/

# RUN update-mime-database /usr/share/mime
# RUN chmod +x /opt/webapp/init.bash

# CMD ["./opt/webapp/init.bash"]
ENTRYPOINT /bin/bash /opt/webapp/init.bash

# CMD ["python", "runserver.py"]
