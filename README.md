Layout is a high-level Python package for laying out content, primarily for
print. It is well documented, tested and commented.

* Documentation is found in the "docs" directory.

* See LICENSE.txt for the terms under which you may use this package.


# Dependencies

The system requires ReportLab >= 2.0 to use the ReportLab specific
functionality (although the library can be used without this,
ReportLab is just the default renderer).

To compile the documentation, you'll need `make` on your system, and
the Python Sphinx package (which in turn has a few dependencies).

To test the system, I recommend you use Nose.

A full set of dependencies, including optional dependencies are in the
requirements.txt file. The docs and testing dependencies aren't
included in the setup.py file.


# Tests

You can run nosetests from the top level package directory to make
sure everything is working.

It is useful normally to install dependencies into a virtualenv, so
the workflow would be:

$ virtualenv ve
$ source ve/bin/activate
$ pip install -U -r requirements.txt
$ nosetests


# Installing

Once you've tested the system, deactivate the virtualenv

$ deactivate

Then active the virtualenv of the project you're working on (or don't
bother if you're installing globally), and do:

$ python setup.py install


# Compiling Documentation

The documentation is built with Sphinx, and is created with a Makefile
in the docs directory. For example

$ cd docs
$ make html
$ cd build/html
$ python -m SimpleHTTPServer 8080

Will serve the documentation at http://localhost:8000

You can also build HTML-help and Latex versions of the documentation,
though other software dependencies exist for them.
