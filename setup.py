#!/usr/bin/env python
"""
    Setup script for part_builder python library
    custom module for use with our synth.py file
    run the following to uninstall:
        pip3 uninstall part_builder
"""
from setuptools import setup

with open('README.md') as readme:
    long_desc = readme.read()

setup(
    name='boot-synth',
    entry_points={
        'console_scripts': ['synth=synth:cli'],
    },
    install_requires=[
        'click'
    ],
    version='1.1',
    licence='MIT',
    description='Synth: a docker bootstrapping CLI tool',
    author='Bennett Dixon, Jack Gindi',
    author_email='bennettdixon16@gmail.com, jmgindi@gmail.com',
    packages=['synth'],
    long_description=long_desc,
    include_package_data=True,
)
