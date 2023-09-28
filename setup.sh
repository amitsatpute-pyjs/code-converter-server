#!/bin/bash

sudo apt update
sudo apt install python3-venv
pip3 install huggingface-hub==0.17.2
envnm=.venv
python3 -m venv $envnm
. $envnm/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
mkdir models
sudo apt install redis-server


