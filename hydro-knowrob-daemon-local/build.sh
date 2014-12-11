#!/bin/sh
# Author: Daniel Beßler

DIR=`pwd`

WS=`echo $ROS_PACKAGE_PATH | tr ":" "\n" | head -n 1`
echo "Using catkin workspace at: $WS";

echo "Creating ´src´ archive....";
cd $WS
rm -rf ./src.tar
tar --exclude=.svn --exclude=.git --exclude=build --exclude=.gradle -cf ./src.tar ./*
cd $DIR
mv ${WS}/src.tar .

echo "Building knowrob/hydro-knowrob-daemon....";
docker build -t knowrob/hydro-knowrob-daemon .
