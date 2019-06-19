#!/usr/bin/env python
"""
    Setup script for part_builder python library
    custom module for use with our synth.py file
    run the following to uninstall:
        pip3 uninstall part_builder
"""
from setuptools import setup

setup(
    name='synth_part_builder',
    version='1.1',
    licence='MIT',
    description='Synth: a docker bootstrapping CLI tool (part builder)',
    author='Bennett Dixon, Jack Gindi',
    author_email='bennettdixon16@gmail.com, jmgindi@gmail.com',
    packages=['synth_part_builder'],
    include_package_data=True,
)
