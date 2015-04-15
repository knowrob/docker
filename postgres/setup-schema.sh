#!/bin/bash
# echo "******CREATING DOCKER DATABASE******"
# gosu postgres postgres --single <<- EOSQL
#     CREATE USER docker;
#     CREATE DATABASE docker;
# EOSQL

# echo "Loading schema and tutorials..."
# gosu postgres pg_ctl -w start
# gosu postgres psql -d docker -f /tmp/schema.sql
# gosu postgres psql -d docker -f /tmp/tutorial.sql
# gosu postgres pg_dump docker -f /tmp/backup.dump
# echo "Successful. Stopping postgres..."
# gosu postgres pg_ctl -w stop
# echo "Done."

echo "******GRANTING PRIVILEGES******"
gosu postgres postgres --single <<- EOSQL
    GRANT ALL PRIVILEGES ON DATABASE docker to docker;
EOSQL
