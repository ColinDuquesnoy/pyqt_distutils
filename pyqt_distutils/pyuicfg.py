"""Help you manage your pyuic.json file (pyqt-distutils)

Usage:
    pyuicfg -g
    pyuicfg -f -g
    pyuicfg -g --pyqt5
    pyuicfg -f -g --pyqt5
    pyuicfg -g --pyside
    pyuicfg -f -g --pyside
    pyuicfg -g --pyside2
    pyuicfg -f -g --pyside2
    pyuicfg -a SOURCE_FILE DESTINATION_PACKAGE
    pyuicfg -r SOURCE_FILE
    pyuicfg (-h | --help)
    pyuicfg --version

Options:
    -h, --help                            Show help
    --version                             Show version
    -f                                    Ask no question
    -g                                    Generate pyuic.json
    -a SOURCE_FILE DESTINATION_PACKAGE    Add file to pyuic.json
    -r SOURCE_FILE                        Remove file from pyuic.json
    --pyqt5                               Generate a pyuic.json file for PyQt5 instead of PyQt4
    --pyside                              Generate a pyuic.json file for PySide instead of PyQt4
    --pyside2                             Generate a pyuic.json file for PySide2 instead of PyQt4

"""
import os
from docopt import docopt
from pyqt_distutils import __version__
from pyqt_distutils.config import Config, QtApi


def qt_api_from_args(arguments):
    if arguments['--pyqt5']:
        return QtApi.pyqt5
    elif arguments['--pyside']:
        return QtApi.pyside
    elif arguments['--pyside2']:
        return QtApi.pyside2
    return QtApi.pyqt4


def main():
    arguments = docopt(__doc__, version=__version__)
    force = arguments['-f']
    generate = arguments['-g']
    file_to_add = arguments['-a']
    destination_package = arguments['DESTINATION_PACKAGE']
    file_to_remove = arguments['-r']
    api = qt_api_from_args(arguments)
    cfg = Config()
    if generate:
        if not force and os.path.exists('pyuic.json'):
            choice = input('pyuic.json already exists. Do you want to replace '
                           'it? (y/N) ').lower()
            if choice != 'y':
                return
        cfg.generate(api)
    elif file_to_add:
        cfg.add(file_to_add, destination_package)
    elif file_to_remove:
        cfg.remove(file_to_remove)


if __name__ == '__main__':
    main()