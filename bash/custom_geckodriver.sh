#!/bin/bash

# install rust first
sudo apt-get install cargo

ghecko_version="0.32.2"
wget https://github.com/mozilla/geckodriver/archive/refs/tags/v$ghecko_version.zip
tar -xvzf geckodriver-v*
rm geckodriver-v*

cd geckodriver-$ghecko_version
cargo build
# now move the ghecko driver to the above directory
cp target/debug/geckodriver ../geckodriver
rm 
cd ..

sudo apt install xapp
sudo snap install firefox