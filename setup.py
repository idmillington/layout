#!/usr/bin/env python

from setuptools import setup

version = __import__('layout').__version__

setup(
    name='layout',
    packages=[
        'layout', 'layout.datatypes', 'layout.elements',
        'layout.managers', 'layout.pages'
        ],

    version=version,
    description='Content Layout Engine',
    author='Ian Millington',
    author_email='idmillington@googlemail.com',

    url='http://github.com/idmillington/layout',
    download_url='https://github.com/idmillington/layout/tarball/master',

    keywords=['pdf', 'layout', 'print', 'design'],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        ],

    zip_safe=False
    )
