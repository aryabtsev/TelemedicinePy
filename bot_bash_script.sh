#!/bin/bash

sudo apt-get update

sudo apt-get upgrade python3

apt install python3-pip

sudo apt-get install python3-tk

cd bot

pip3 install -r requirements.txt

python3 bot.py
