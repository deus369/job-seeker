#!/bin/bash

cd .. # go to job-seeker folder
sudo apt-get install python
sudo apt install python3-tk
pip install selenium
# pip install tkinter

# install ghecko driver too
# check latest in https://github.com/mozilla/geckodriver/releases
ghecko_version="v0.32.0"
wget https://github.com/mozilla/geckodriver/releases/download/$ghecko_version/geckodriver-$ghecko_version-linux64.tar.gz
tar -xvzf geckodriver-v*
rm geckodriver-v*
chmod +x geckodriver
export PATH=$PATH:$PWD/.
