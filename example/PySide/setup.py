#!/usr/bin/env python
from setuptools import setup, find_packages
try:
    from pyqt_distutils.build_ui import build_ui
except ImportError:
    build_ui = None


setup(
    name='foo',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='Example of use of pyqt',
    cmdclass={'build_ui': build_ui},
)

