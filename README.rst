PyQt Distutils
==============

A set of distutils extension to work with PyQt applications and UI files.

The goal of this tiny library is to help you write PyQt application in a
pythonic way, using setup.py to build the Qt designer Ui files.

This works with PyQt4, PyQt5 and PySide (tested with python3 only).


Usage
-----

Add the following lines to your setup.py:

.. code-block:: python

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


UI Files
--------

The compilation of ui files is driven by a pyuic.cfg file, which is a plain
json file with the following format:

.. code-block:: python

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


License
-------

This project is licensed under the MIT license.

Changelog
---------

0.1.1
+++++

- Fix description and examples when pyqt-distutils has not been installed.

0.1.0
+++++

- Initial release
