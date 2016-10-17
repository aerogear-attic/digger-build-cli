#!/usr/bin/env python                                                                                                                               
from setuptools import setup, find_packages


VERSION = '0.3.0'


setup(
  name='AeroGear build cli for Digger',
  version=VERSION,
  description='AeroGear build cli for Digger',
  author='AeroGear',
  author_email = 'aerogear-dev@lists.jboss.org',
  url = 'https://github.com/aerogear/digger-build-cli',
  download_url = 'https://github.com/aerogear/digger-build-cli/tarball/%s' % VERSION,
  keywords = [
    'application builds',
    'gradle',
    'ant',
    'cordova',
    'cli'
  ],
  classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Environment :: Console',
    'Topic :: Software Development :: Build Tools'
  ],
  packages=find_packages(),
  install_requires=[
    'addict==1.0.0',
    'six==1.10.0'
  ],
  setup_requires=['pytest-runner'],
  tests_require=['pytest', 'pytest-sugar'],
  scripts=['scripts/abcd']
)
