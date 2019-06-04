#!/usr/bin/env sh
# install script for synth!

# startup install
echo 'Python 3.4+ is required to run synth!'

echo 'Installing Python Dependencies...'
# python3 dependencies
pip3 install click
# build our part_builder dependency, removing any old versions first
pip3 uninstall -y part_builder
python3 setup.py install

# setup content in /etc
if [ -d  "/etc/synth" ]; then
    echo 'Prior installation detected, removing old /etc/synth directory...'
    rm -rf /etc/synth
fi
echo 'Installing bootstrap projects in /etc/synth...'
mkdir -p /etc/synth
cp -R ./projects_master/ /etc/synth/projects_master

# setup executable in /usr/local/bin
echo 'Creating executable in /usr/local/bin...'
cp ./synth.py /usr/local/bin/synth
chmod +x /usr/local/bin/synth
