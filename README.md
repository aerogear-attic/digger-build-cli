# abcd - AeroGear build cli for Digger

[![Build Status](https://travis-ci.org/aerogear/digger-build-cli.png)](https://travis-ci.org/aerogear/digger-build-cli)
[![License](https://img.shields.io/:license-Apache2-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)


## Usage

Full documentation at [http://digger-build-cli.readthedocs.io](http://digger-build-cli.readthedocs.io/en/latest/).

### Requirements

If running outside a container:

Download and install conda: http://conda.pydata.org/miniconda.html

After cloning the repository run:

```sh
conda env create -f env.yaml python=3.5.1
```

To activate the environment run (might need a new terminal window or reload bashrc/bash_profile):

```
source activate digger
```

You will also need Node 4.x, NPM, Cordova >=6 and Java 8 on your machine.


Some requirements are needed to run it outside of a container:


### Installation

```sh
python setup.py install
```

### Tests

#### Requirements

Installing development dependencies:

```sh
pip install -r requirements.txt
```

Tests will download all templates from their Github repository (master branch) and will try to build it.

### If running outside of the container

#### Prepare

```sh
# create a folder for Gradle cache
mkdir /gradle-cache
# make sure you have write permissions
chown -R ${USER} /gradle-cache
```

Also, make sure you have Android SDK on your machine and `$ANDROID_HOME` is set.

#### setup.py

```sh
python setup.py test
```

####  using py.test directly (from digger project root folder)

```sh
py.test -s
```

#### Running an individual test

For example:

```sh
py.test -s tests/test_build.py
```