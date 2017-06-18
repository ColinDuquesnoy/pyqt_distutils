PyQt Distutils
==============

.. image:: https://img.shields.io/pypi/v/pyqt-distutils.svg
   :target: https://pypi.python.org/pypi/pyqt-distutils/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/pyqt-distutils.svg
   :target: https://pypi.python.org/pypi/pyqt-distutils/
   :alt: Number of PyPI downloads

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
        from pyqt_distutils.build_ui import build_ui
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

If you want to require the user to have ``pyqt-distutils`` installed, and
always have the ``build_ui`` command run as part of the ``build_py`` command
(and all dependent commands), you can do so with a custom command class:

.. code-block:: python

    from setuptools import setup
    from setuptools.command.build_py import build_py

    from pyqt_distutils.build_ui import build_ui

    class custom_build_py(build_py):
        def run(self):
            self.run_command('build_ui')
            build_py.run(self)

    setup(...,
        cmdclass={
            'build_ui': build_ui,
            'build_py': custom_build_py,
        }
    )

UI Files
--------

The compilation of ui files is driven by a pyuic.json file, which is a plain
json file with the following format:

.. code-block:: json

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
write the following pyuic.json:

.. code-block:: json

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

Hooks
-----

A pyqt-distutils hook is a python function that is called after the
compilation of a ui/rc script to let you customise its content.

E.g. you might want to write a hook to change the translate function used or
replace the PyQt imports by your owns if you're using a shim,...

The hook function is a simple python function which must take a single
argument: the path to the generated python script.

Hooks are exposed as setuptools entrypoint using ``pyqt_distutils_hooks`` as
the entrypoint key. Add the following code to your setup.py to register your
onw hooks:

.. code-block:: python

    setup(
        ...,
        entry_points={
            'pyqt_distutils_hooks': [
                'hook_name = package_name.module_name:function_name']
        },
        ...)



To actually use the hook, you must add a "hooks" key to your pyuic.json. This
property lists the name of the hooks you'd like to run. E.g:


.. code-block:: json

    {
        "files": [
            ["forms/*.ui", "foo_gui/forms/"],
            ["resources/*.qrc", "foo_gui/forms/"]
        ],
        "pyrcc": "pyrcc5",
        "pyrcc_options": "",
        "pyuic": "pyuic5",
        "pyuic_options": "--from-imports",
        "hooks": ["gettext", "spam", "eggs"]
    }

At the moment, we provide one builtin hook: **gettext**. This hook let you
use a ``gettext.gettext`` wrapper instead of ``QCoreApplication.translate``.

Command line tool
-----------------

Starting from version 0.2, you can use the ``pyuicfg`` command line tool
to manage your ``pyuic.json`` file:

.. code-block:: bash

    # generate pyuic.json in the current directory, for use with PyQt4
    pyuicfg -g

    # generate pyuic.json in the current directory, for use with PyQt5
    pyuicfg -g --pyqt5

    # generate pyuic.json in the current directory, for use with PySide
    pyuicfg -g --pyside

    # add files
    pyuicfg -a forms/main_window.ui foo_package/forms
    pyuicfg -a resources/foo.qrc foo_package/forms

    # remove file
    pyuicfg -r resources/foo.qrc

Requirements
------------

The following packages are required:

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

0.7.3
+++++

Handle path with spaces (thanks @amacd31 and @benoit-pierre see PR `9`_)

.. _9: https://github.com/ColinDuquesnoy/pyqt_distutils/pull/9

0.7.2
+++++

Fix unhandled exception: TypeError when there is a CalledProcessError (see issue `7`_)

.. _7: https://github.com/ColinDuquesnoy/pyqt_distutils/issues/7

0.7.1
+++++

Improve subprocess command handling: write failing commands in yellow and their error message in red.

0.7.0
+++++

Add optional support for colorama.

If colorama can be imported, the build_ui output will be colored as follow:

- pyuic/pyrcc commands in GREEN
- skipped targets with the DEFAULT FORE COLOR
- warning message in YELLOW
- error messages in RED

0.6.2
+++++

- gettext hook: don't replace ``_`` function. Now the hook works well for
  translating ``*.ui`` files with gettext or babel.

0.6.1
+++++

- improbe gettext hook implementation to work with xgettext and babel

0.6.0
+++++

- add support for running custom hooks

0.5.2
+++++

- remove enum34 dependency and make the wheel truly universal

0.5.1
+++++

- fix installation issue on python 3.5

0.5.0
+++++

- allow the use of .json extension instead of .cfg (both are supported, .json
  become the default extension)

0.4.2
++++++

- fix python 2 compatibility (#2)

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
