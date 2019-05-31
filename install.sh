#!/usr/bin/env sh
# install script for synth!

# startup install
echo 'Python 3.4+ is required to run synth!'

# python3 dependencies
pip3 install click

# setup content in /etc
echo 'Installing bootstrap projects in /etc/synth...'
mkdir -p /etc/synth
cp -R ./projects_master/ /etc/synth/projects_master/

# setup executable in /usr/local/bin
echo 'Creating executable in /usr/local/bin...'
cp ./synth.py /usr/local/bin/synth
chmod +x /usr/local/bin/synth
