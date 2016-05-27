#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='ycm-flags',
    version='1.0.0',
    url='https://github.com/mexus/ycm-flags',
    author='Denis Zaletaev',
    author_email='gilaldpellaeon@gmail.com',
    description='Flags generator for YouCompleteMe vim plugin',
    py_modules=['ycmflags']
)
