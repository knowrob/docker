#!/bin/sh
# Author: Daniel Beßler

DIR=`pwd`

if [ ! -d src ]; then
  echo "No ´src´ directory preset, creating a symlink from catkin workspace...";
  
  WS=`echo $ROS_PACKAGE_PATH | tr ":" "\n" | head -n 1`
  echo "Using catkin workspace at: " + $WS;
  
  ln -s $WS ${DIR}/src
fi

echo "Creating ´src´ archive....";
cd src
tar --exclude=.svn --exclude=.git --exclude=build --exclude=.gradle -cf ./src.tar ./*
mv ./src.tar ${DIR}/
cd ..

echo "Building knowrob/hydro-knowrob-daemon....";
docker build -t knowrob/hydro-knowrob-daemon .
