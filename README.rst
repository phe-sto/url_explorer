============
URL EXPLORER
============

This script make it easy to research the existence of URL(s) based on a regular expression.
Thank to the exrex package that can compute every possibilities based on a regular expression.
The package is installed if necessary at the beginning of this script. Once started the script launch many thread to
check for the existence of the URL. The Default number of thread in 1000 but can be passed as argument. It make the process
faster than a sequential processing.

Platforms
---------

All platforms that run Python 3 (tested on Mac OS and Ubuntu).

Dependency
----------

An unique dependency with `Python 3.6`_, the script needs the interpreter.


Usage
-----

Simple starting without argument to use the CLI:

   .. code-block:: bat

      python3 url_explorer.py

Pass the URL regex pattern as argument (don't forget the quotes for the regex):

   .. code-block:: bat

      python3 url_explorer.py -re 'http://www\.g..gle\.com'

Pass the CSV output file name, otherwise the result of the URL(s) found is printed:

   .. code-block:: bat

      python3 url_explorer.py -re 'http://www\.g..gle\.com' -of google.csv

Pass the maximum thread number (limit to 500):

   .. code-block:: bat

      python3 url_explorer.py -re 'http://www\.g..gle\.com' -mt 500

   .. warning:: Dot '.' is a regular expression symbol. Don't forgot to escape it if it is not
      meant to be a regular expression. For instance to search for google.com subdomain https://www\...\.google\.com .
      First and third dot are escaped but not the second.

   .. warning:: Depend on exrex python package to generate all the URL(s) based on a regex. Therefore a pip install is
      performance at the beginning of the script. This pip command might force you to sudo or log as administrator,
      root, etc.

.. _Python 3.6: https://www.python.org/downloads/