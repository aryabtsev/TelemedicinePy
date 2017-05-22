#!/bin/bash

sudo apt-get update

sudo apt-get upgrade python3

apt install python3-pip

pip3 install -r requirements.txt

cd bot

python3 bot.py