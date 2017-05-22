#!/bin/bash

sudo apt-get update

sudo apt-get upgrade python3

apt install python3-pip

cd bot

pip3 install -r requirements.txt

python3 bot.py
