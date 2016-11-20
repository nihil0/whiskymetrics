#!/usr/bin/env bash

#Install required programs
sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev python-pip python3-pip git

# Set up virtualenv
sudo pip install virtualenv

mkdir ~/.virtualenv

virtualenv -p python3 ~/.virtualenv/whiskymetrics

# Clone repo
git clone https://github.com/nihil0/WhiskyMetrics.git
