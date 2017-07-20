#!/bin/bash

if [ -z "$1" ] ; then
    echo Usage: $0 [NEW_USER]
    exit 1
fi

NEW_USER=$1
echo Creating $NEW_USER

sudo adduser $NEW_USER
sudo mkdir /home/$NEW_USER/ftp
sudo chown nobody:nogroup /home/$NEW_USER/ftp
sudo chmod a-w /home/$NEW_USER/ftp
sudo mkdir /home/$NEW_USER/ftp/files
sudo chown $NEW_USER:$NEW_USER /home/$NEW_USER/ftp/files/
history | grep $NEW_USER
