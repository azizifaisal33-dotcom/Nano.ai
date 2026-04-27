#!/bin/bash
pkg update -y
pkg install python git termux-api -y
pip install rich flask
git clone https://github.com/azizifaisal33-dotcom/Nano.ai
cd Nano.ai
./brain.py