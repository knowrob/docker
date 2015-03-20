#!/bin/bash

# path to prac application container
source /opt/practools/tools/prac/env.sh
source /opt/practools/tools/pracmln/env.sh
export PATH=$PATH:/opt/practools/tools/toulbar2/bin

echo 'application/mln                 mln' >> $HOME/.mime.types
echo 'application/db                  db' >> $HOME/.mime.types
echo 'application/pracmln             pracmln' >> $HOME/.mime.types

python /opt/webapp/runserver.py
# /bin/bash
