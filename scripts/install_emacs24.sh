#!/bin/bash

if [[ `id -u` -ne 0 ]]; then
  echo "You have to execute this script as super user!"
  exit 1;
fi

apt-get update
apt-get install -y build-essential
apt-get build-dep emacs24
wget http://ftp.gnu.org/gnu/emacs/emacs-24.4.tar.gz
tar -xzvf emacs-24.4.tar.gz
rm emacs-24.4.tar.gz
cd emacs-24.4
./configure --prefix=/opt/emacs
make
make install
export PATH=/opt/emacs/bin:$PATH
echo "export PATH=/opt/emacs/bin:\$PATH" >> ~/.bashrc
mkdir -p ~/emacs/lisp
cd emacs/lisp
wget http://orgmode.org/org-8.2.10.tar.gz
tar zxvf org-8.2.10.tar.gz