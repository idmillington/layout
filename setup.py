#!/usr/bin/env python

from distutils.core import setup

version = __import__('layout').__version__

setup(
    name='Layout',
    version=version,
    description='Content Layout Engine',
    author='Ian Millington',
    author_email='idmillington@googlemail.com',
    packages=[
        'layout', 'layout.datatypes', 'layout.elements',
        'layout.managers', 'layout.pages'
        ],
    requires=['reportlab(>=2.0)']
    )
