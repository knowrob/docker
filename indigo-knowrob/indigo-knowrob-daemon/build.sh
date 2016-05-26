#!/bin/sh
# Author: Daniel Beßler, Ferenc Balint-Benczedi

SCRIPT=`readlink -f "$0"`
DIR=`dirname $SCRIPT`

$DIR/../../scripts/start-apt-cacher
echo "Building knowrob/indigo-knowrob-daemon....";
docker build -t knowrob/indigo-knowrob-daemon .

