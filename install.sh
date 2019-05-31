#!/usr/bin/env sh
# install script for synth!

# startup install
echo 'Python 3.4+ is required to run synth!'

# python3 dependencies
pip3 install click

echo 'Installing bootstrap projects...'
# setup content in /etc
mkdir -p /etc/synth/projects_master
cp -R ./projects_master/ /etc/synth/projects_master/

echo 'Creating executable in /usr/bin...'
# setup executable in /usr/bin
cp ./synth.py /usr/local/bin/synth
chmod +x /usr/local/bin/synth