#!/bin/sh
# Author: Daniel Beßler

RUNNING=$(docker inspect --format="{{ .State.Running }}" apt-cacher-run 2>/dev/null)
if [ $? -eq 1 ]; then # container does not exist
  echo "No apt-cacher container exists, creating a new one..."
  cd $DIR/../../apt-cacher-ng
  docker build -t apt-cacher .
  docker run -d -p 3142:3142 --name apt-cacher-run apt-cacher
  cd $DIR
fi
if [ X"$RUNNING" = X"false" ]; then # container exists, but stopped
  echo "apt-cacher container exists, starting it..."
  docker rm apt-cacher-run
  cd $DIR/../../apt-cacher-ng
  docker build -t apt-cacher .
  docker run -d -p 3142:3142 --name apt-cacher-run apt-cacher
  cd $DIR
fi

echo "Building knowrob/hydro-knowrob-base....";
docker build -t knowrob/hydro-knowrob-base .

