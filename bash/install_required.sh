#!/bin/bash

# cd .. # go to job-seeker folder
# sudo apt-get install python python3-tk

if command -v apt-get &> /dev/null; then
    sudo apt-get install python python3-tk
    pip install selenium
    # install ghecko driver too
    # check latest in https://github.com/mozilla/geckodriver/releases
    ghecko_version="v0.32.0"
    wget https://github.com/mozilla/geckodriver/releases/download/$ghecko_version/geckodriver-$ghecko_version-linux64.tar.gz
    tar -xvzf geckodriver-v*
    rm geckodriver-v*
    chmod +x geckodriver
    export PATH=$PATH:$PWD/.
elif command -v pacman &> /dev/null; then
    sudo pacman -S python python-pip geckodriver tk
    # use this if having issues
    pip install selenium cryptography --break-system-packages
    # pipx
    # python -m venv myenv
    # source myenv/bin/activate
    # pip install selenium
    # pipx install selenium
else
    echo "Unsupported package manager."
fi

# pip install tkinter
