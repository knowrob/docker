#!/bin/sh
# Author: Daniel Beßler

SCRIPT=`readlink -f "$0"`
DIR=`dirname $SCRIPT`

$DIR/../../scripts/start-apt-cacher
echo "Building knowrob/indigo-knowrob-base....";
docker build -t knowrob/indigo-knowrob-base .

