Thoth Python
------------

This library provides routines for Python specific operations for project Thoth. An example of routines present in this library:

* manipulating with project (see Project abstraction)
* operations on top of requirements.txt files and/or Pipfile and Pipfile.lock files
* operations for operating with Python package source indexes (`PEP-0503 <https://www.python.org/dev/peps/pep-0503/>`_ compatible simple repository API)
* operations for Python packages (default and the development ones) and their in memory hierarchical structures


Running the testsuite
=====================

You can use Pipenv for managing this project and execute testsuite using ``setup.py``'s ``test`` command:

.. code-block:: console

  pipenv install --dev
  pipenv run python3 setup.py test

