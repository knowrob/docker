#!/bin/bash

MOUNT_DIRECTORY="/episodes"

FTP_HOST=$OPENEASE_FTP_HOST
FTP_NAME=$OPENEASE_FTP_USERNAME
FTP_PASSWORD=$OPENEASE_FTP_PASSWORD

FTP_URL="$FTP_NAME:$FTP_PASSWORD@$FTP_HOST"

# Loop until we succeeded to mount for the first time
echo "Trying to mount $FTP_URL..."
while true; do
    curlftpfs -d -v -o allow_other $FTP_URL $MOUNT_DIRECTORY;
    #curlftpfs -d -v -o allow_root $FTP_URL $MOUNT_DIRECTORY;
    if [ $? -eq 0 ]; then
        echo "Connected."
        break;
    else
        echo "Failed to connect. Re-trying in 2 seconds..."
        sleep 2;
    fi
done
while true; do
    sleep 2;
done
