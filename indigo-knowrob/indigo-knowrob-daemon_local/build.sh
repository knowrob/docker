#!/bin/sh
# Author: Daniel Beßler

NAMES="knowrob knowrob_addons knowrob_dev iai_maps iai_common_msgs iai_cad_tools"

SCRIPT=`readlink -f "$0"`
DIR=`dirname $SCRIPT`
LOCAL_DIR="$DIR/src"
KNOWROB_FOUND=0

is_knowrob_dir() {
  if [ ! -d "$1" ]; then
    return 1
  fi
  echo "Checking directory $1 ..."
  VALID=0
  for n in $NAMES; do
    if ls $1 | grep ^$n$ > /dev/null; then
      echo "    $n found."
    else
      echo "    $n not found."
      VALID=1
    fi
  done
  return $VALID
}

create_archive() {
  cd $1
  rm -rf ./src.tar
  tar --exclude=.svn --exclude=.git --exclude=build --exclude=bin --exclude=.gradle -cf ./src.tar ./*
  mv ./src.tar $DIR/
  cd $DIR
}

clone_knowrob_repo() {
  mkdir -p $LOCAL_DIR
  cd $LOCAL_DIR
  if ls $LOCAL_DIR | grep ^$1$ > /dev/null; then
    echo "$1 already cloned."
  else
    git clone --recursive $2 -b $3
  fi
  cd $DIR
}

clone_knowrob() {
  clone_knowrob_repo knowrob            https://github.com/knowrob/knowrob.git           master
  clone_knowrob_repo knowrob_addons     https://github.com/knowrob/knowrob_addons.git    master
  clone_knowrob_repo knowrob_tutorials  https://github.com/knowrob/knowrob_tutorials.git master
  clone_knowrob_repo knowrob_dev     https://github.com/code-iai/knowrob_dev.git      master
  clone_knowrob_repo iai_maps        https://github.com/code-iai/iai_maps.git         master
  clone_knowrob_repo iai_common_msgs https://github.com/code-iai/iai_common_msgs.git  master
  clone_knowrob_repo iai_cad_tools   https://github.com/code-iai/iai_cad_tools.git    master
}

echo "Script is executed at: $DIR"

# Try local directory first
is_knowrob_dir $LOCAL_DIR
if [ $? -eq 0 ]; then
  create_archive $LOCAL_DIR
  KNOWROB_FOUND=1
fi

# Try ROS_PACKAGE_PATH head directory
if [ $KNOWROB_FOUND -eq 0 ]; then
  if env | grep -q ^ROS_PACKAGE_PATH=; then
    echo "ROS_PACKAGE_PATH is defined."
    WS=`echo $ROS_PACKAGE_PATH | tr ":" "\n" | head -n 1`
    is_knowrob_dir $WS
    if [ $? -eq 0 ]; then
      create_archive $WS
      KNOWROB_FOUND=1
    fi
  else
    echo "WARNING: ROS_PACKAGE_PATH is not defined."
  fi
fi

# Checkout knowrob locally
if [ $KNOWROB_FOUND -eq 0 ]; then
  echo "Unable to locate knowrob installation. Checking it out via git..."
  clone_knowrob
  create_archive $LOCAL_DIR
fi

$DIR/../../scripts/start-apt-cacher
$DIR/../../scripts/start-nexus
echo "Building openease/indigo-knowrob-daemon....";
docker build -t openease/indigo-knowrob-daemon .

