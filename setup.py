#!/usr/bin/env python
from setuptools import setup, find_packages


def read_version():
    """
    Reads the version without self importing
    """
    with open("pyqt_distutils/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                return l.split("=")[1].strip().replace(
                    '"', "").replace("'", '')


setup(
    name='pyqt-distutils',
    version=read_version(),
    packages=find_packages(),
    url='https://github.com/ColinDuquesnoy/pyqt_distutils',
    license='MIT',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='A set of distutils extension for building Qt ui files',
    entry_points={'console_scripts': ['pyuicfg = pyqt_distutils.pyuicfg:main']}
)
