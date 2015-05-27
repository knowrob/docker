#!/bin/bash
# gosu postgres postgres --single <<- EOSQL
#    GRANT ALL PRIVILEGES ON DATABASE docker to docker;
# EOSQL

echo "******CREATING DOCKER AND TUTORIAL DATABASE******"
gosu postgres postgres --single <<- EOSQL
  CREATE DATABASE docker;
  CREATE DATABASE tutorial;
  CREATE USER docker;
  GRANT ALL PRIVILEGES ON DATABASE docker to docker;
  GRANT ALL PRIVILEGES ON DATABASE tutorial to docker;
EOSQL

echo "******WRITING SQL DUMP TO DATABASE TUTORIAL******"
gosu postgres pg_ctl -w start
gosu postgres psql -d tutorial -f /tmp/schema.sql
gosu postgres psql -d tutorial -f /tmp/tutorial.sql
gosu postgres pg_ctl stop
echo "******TUTORIAL CONTENT WRITTEN******"
