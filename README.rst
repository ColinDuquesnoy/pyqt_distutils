PyQt Distutils
==============

A set of distutils extension to work with PyQt applications and UI files.

The goal of this tiny library is to help you write PyQt application in a
pythonic way, using setup.py to build the Qt designer Ui files.

This works with PyQt4, PyQt5 and PySide (tested with python3 only).


Usage
-----

Add the following lines to your setup.py::

    # import build_ui
    try:
        from pyqt_distutils import build_ui
        cmdclass = {'build_ui': build_ui}
    except ImportError:
        build_ui = None  # user won't have pyqt_distutils when deploying
        cmdclass = {}

    ...

    setup(...,
          cmdclass=cmdclass)

To build the ui/qrc files, run::

    python setup.py build_ui

To forcibly rebuilt every files, use the ``--force`` option::

    python setup.py build_ui --force

UI Files
--------

The compilation of ui files is driven by a pyuic.cfg file, which is a plain
json file with the following format::

    {
        "files": [
            [
                "forms/main_window.ui",
                "package/forms"
            ]
        ],
        "pyrcc": "pyrcc5",
        "pyrcc_options": "",
        "pyuic": "pyuic5",
        "pyuic_options": "--from-imports"
    }

Here is a brief description of the fields:

- files: list of file pairs made up of the source ui file and the
  destination package
- pyrcc: the name of the pyrcc tool to use (e.g: 'pyrcc4' or 'pyside-rcc')
- pyrcc_options: pyrcc options (optional)
- pyuic: the name of the pyuic tool to use (e.g: 'pyrcc4' or 'pyside-rcc')


Starting from version 3.0, you can use a *glob expression* instead of a file path.
E.g., to compile all ui files under the ``forms`` directory in ``package/forms``, you could
write the following pyuic.cfg::

    {
        "files": [
            [
                "forms/*.ui",
                "package/forms"
            ]
        ],
        "pyrcc": "pyrcc5",
        "pyrcc_options": "",
        "pyuic": "pyuic5",
        "pyuic_options": "--from-imports"
    }


Command line tool
-----------------

Starting from version 0.2, you can use the ``pyuicfg`` command line tool
to manage your ``pyuic.cfg`` file::

    # generate pyuic.cfg in the current directory, for use with PyQt4
    pyuicfg -g

    # generate pyuic.cfg in the current directory, for use with PyQt5
    pyuicfg -g --pyqt5

    # generate pyuic.cfg in the current directory, for use with PySide
    pyuicfg -g --pyside

    # add files
    pyuicfg -a forms/main_window.ui foo_package/forms
    pyuicfg -a resources/foo.qrc foo_package/forms

    # remove file
    pyuicfg -r resources/foo.qrc

Requirements
------------
The following packages are required:

    - enum34 (python enums)
    - docopt

Install
-------

You can either install from pypi::

    (sudo) pip install pyqt-distutils

Or from source::

    pip install .

License
-------

This project is licensed under the MIT license.

Changelog
---------
0.4.1
+++++

- remove useless and confusing print statement

0.4.0
+++++

- add a ``--force`` flag
- always force compilation ``*.qrc`` files

0.3.0
+++++
- allow glob expression in files lists.

0.2.1
+++++

- fix missing install requirements (docopt and enum34).

0.2.0
+++++

- add ``pyuicfg`` command line tool to administrate your ``pyuic.cfg`` file.

0.1.2
+++++

- Improve readme

0.1.1
+++++

- Fix description and examples when pyqt-distutils has not been installed.

0.1.0
+++++

- Initial release
