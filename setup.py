#!/usr/bin/env python                                                                                                                               
from setuptools import setup, find_packages


setup(
  name='AeroGear build cli for Digger',
  version='0.3.0',
  description='AeroGear build cli for Digger',
  author='AeroGear',
  packages=find_packages(),
  install_requires=[
    'addict==1.0.0',
    'six==1.10.0'
  ],
  setup_requires=['pytest-runner'],
  tests_require=['pytest', 'pytest-sugar'],
  scripts=['scripts/abcd']                      
)
