#!/usr/bin/python3

"""
Setup.py

APP: Trumpatron
DESC: 
CREATION_DATE: 2017-03-02

"""

import setuptools

setuptools.setup(
    name='TrumpaTron',
    version='1.0.0',
    description='Donald Trump bot',
    author='Joshua Carlson-Purcell',
    author_email='josh@carlson.ninja',
    url='https://github.com/magneticstain/TrumpaTron'
    packages=setuptools.find_packages(exclude=['build', 'conf']),
)