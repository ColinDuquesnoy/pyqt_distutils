#!/usr/bin/env python
from setuptools import setup, find_packages

from pyqt_distutils import __version__


setup(
    name='pyqt-distutils',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/ColinDuquesnoy/pyqt_distutils',
    license='MIT',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='A set of distutils extension for building Qt ui files',
    install_requires=['docopt'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Setuptools Plugin',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Software Distribution',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)'
    ],
    entry_points={
        'console_scripts': ['pyuicfg = pyqt_distutils.pyuicfg:main'],
        'pyqt_distutils_hooks': ['gettext = pyqt_distutils.hooks:gettext']
    }
)
