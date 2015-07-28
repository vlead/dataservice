#!/bin/bash
# Shell script to install deb package dependencies as well as python package
# dependencies for dataservice.

if [[ `id -u` -ne 0 ]]; then
  echo "You have to execute this script as super user!"
  exit 1;
fi
# Update the packages
echo "Installing pre-requisite dependencies.."
apt-get update
apt-get install mysql-server python-dev libmysqld-dev
echo "Installing dependencies.."
# Installing dependencies
python setup.py install
if [[ $? -ne 0 ]]; then
  echo "Installation failed!"
  exit 1;
fi
exit 0
