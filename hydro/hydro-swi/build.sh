#!/bin/sh
# Author: Daniel Beßler
SCRIPT=`readlink -f "$0"`
DIR=`dirname $SCRIPT`
HOST_IP=`ip route list dev docker0 | awk 'NR==1 {print $NF}'`

$DIR/../scripts/start-apt-cacher
$DIR/../scripts/start-nexus
echo "Building openease/hydro-swi....";
docker build --build-arg HOST_IP=${HOST_IP} "$@" -t openease/hydro-swi $DIR

