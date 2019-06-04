#!/usr/bin/env python
"""
    Setup script for part_builder python library
    custom module for use with our synth.py file
    run the following to uninstall:
        pip3 uninstall part_builder
"""
from distutils.core import setup
from setuptools import setup

setup(name='part_builder',
  version='1.0',
  description='PartBuilder for use with Synth ',
  author='Bennett Dixon, Jack Gindi',
  author_email='bennettdixon16@gmail.com, jmgindi@gmail.com',
  packages=['part_builder'],
 ) 
