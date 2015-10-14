#!/bin/bash

if [[ `id -u` -ne 0 ]]; then
  echo "You have to execute this script as super user!"
  exit 1;
fi

apt-get update
apt-get install -y build-essential libncurses-dev git
apt-get build-dep emacs24
wget http://ftp.gnu.org/gnu/emacs/emacs-24.4.tar.gz
tar -xzvf emacs-24.4.tar.gz
rm emacs-24.4.tar.gz
cd emacs-24.4
./configure
make
make install
mkdir -p ~/emacs/lisp
cd emacs/lisp
wget http://orgmode.org/org-8.2.10.tar.gz
tar zxvf org-8.2.10.tar.gz
