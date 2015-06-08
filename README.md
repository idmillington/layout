Layout is a high-level Python package for laying out content,
primarily for print. It is well documented, tested and commented and
has been used in anger for several years.

* Documentation is found in the "docs" directory.

* The package is MIT licensed. See `LICENSE.txt` for the terms.


# Dependencies

The system requires [ReportLab](http://www.reportlab.com/) >= 2.0 to use the
ReportLab specific functionality (although the layout parts of the library
can be used without it).

To compile the documentation, you'll need `make` on your system, and the
Python [Sphinx](http://sphinx-doc.org/) package (which in turn has a few
dependencies).

To test the system, I recommend you use
[Nose](https://nose.readthedocs.org/en/latest/).

A full set of dependencies, including optional dependencies are in the
`requirements.txt` file. Please note that this was created by doing a `pip
freeze` and then editing the == to >= for each requirement, which encodes
the versions of libraries I happened to have, earlier versions of the same
libraries may also work, I haven't systematically searched for the earliest
version of each library that passes the tests.

The docs and testing dependencies are included in the `setup.py` file. If you
are installing the package into your own application, you may not need
these.


# Tests

You can run `nosetests` from the top level package directory to make
sure everything is working.

It is normally useful to install dependencies into a virtualenv, so
the workflow would be:

    $ virtualenv ve
    $ source ve/bin/activate
    $ pip install -U -r requirements.txt
    $ nosetests


# Installing

Once you've tested the system, deactivate the virtualenv

    $ deactivate

Then activate the virtualenv of the project you're working on (or don't
bother if you're installing globally), and do:

    $ python setup.py install


# Compiling Documentation

The documentation is built with Sphinx, and is created with a `Makefile`
in the `docs` directory. For example

    $ cd docs
    $ make html
    $ cd build/html
    $ python -m SimpleHTTPServer 8080

This will serve the documentation at http://localhost:8000

You can also build HTML-help and LaTeX versions of the documentation,
though other software dependencies exist for them.
