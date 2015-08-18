#!/bin/bash
# Shell script to install deb package dependencies as well as python package
# dependencies for dataservice.

# Update the packages
echo "Installing pre-requisite dependencies.."
echo "To install system-wide packages, you have to enter sudo password.."
sudo apt-get update
sudo apt-get install mysql-server python-dev libmysqld-dev
echo "Installing dependencies.."
# Installing dependencies
python -c 'import sys; print sys.real_prefix' 2>/dev/null && INVENV=1 || INVENV=0
if [[ $INVENV -eq 0 ]]; then
  source venv/bin/activate
fi
python setup.py install
if [[ $? -ne 0 ]]; then
  echo "Installation failed!"
  exit 1;
fi
exit 0
