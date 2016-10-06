############
Installation
############


Source code located at: https://github.com/aerogear/digger-build-cli


************
Requirements
************

Conda is recommended for environment setup: https://www.continuum.io/downloads

If running tests outside a container, `ANDROID_HOME` needs to be set as well.


*******************
Installing with pip
*******************

.. code-block:: bash
  
  pip install git+ssh://git@github.com/aerogear/digger-build-cli.git


This will install a CLI script "abcd" together with the module itself.


*****************
Build from source
*****************

Clone the repository then run:


.. code-block:: bash

  python setup.py install


***********
Development
***********

You can clone it and then run (considering conda is already installed):

.. code-block:: bash

  conda env create -f env.yaml

To activate the dev environment run:

.. code-block:: bash
  
  source activate digger

To run tests:

.. code-block:: bash

  py.test -s

