"""
Contains the config class (pyuic.cfg or pyuic.json)

"""
import json

from enum import IntEnum, unique
from dataclasses import dataclass
from typing import List, Tuple

from .utils import write_message

@unique
class QtApi(IntEnum):
    pyqt4 = 0
    pyqt5 = 1
    pyqt6 = 2
    pyside = 3
    pyside2 = 4
    pyside6 = 5


@dataclass
class ApiConfig:
    pyrcc: str
    pyrcc_options: str
    pyuic: str
    pyuic_options: str


apiConfigs = [
    ApiConfig(
        pyrcc = 'pyrcc4',
        pyrcc_options = '-py3',
        pyuic = 'pyuic4',
        pyuic_options = '--from-import',
    ),
    ApiConfig(
        pyrcc = 'pyrcc5',
        pyrcc_options = '',
        pyuic = 'pyuic5',
        pyuic_options = '--from-import',
    ),
    ApiConfig(
        pyrcc = 'pyrcc6',
        pyrcc_options = '',
        pyuic = 'pyuic6',
        pyuic_options = '--from-import',
    ),
    ApiConfig(
        pyrcc = 'pyside-rcc',
        pyrcc_options = '-py3',
        pyuic = 'pyside-uic',
        pyuic_options = '--from-import',
    ),
    ApiConfig(
        pyrcc = 'pyside2-rcc',
        pyrcc_options = '-py3',
        pyuic = 'pyside2-uic',
        pyuic_options = '--from-import',
    ),
    ApiConfig(
        pyrcc = 'pyside6-rcc',
        pyrcc_options = '-py3',
        pyuic = 'pyside6-uic',
        pyuic_options = '--from-import',
    ),
]


class Config:
    def __init__(self):
        self.files = []
        self.pyuic = ''
        self.pyuic_options = ''
        self.pyrcc = ''
        self.pyrcc_options = ''
        self.hooks = []

    def uic_command(self):
        return self.pyuic + ' ' + self.pyuic_options + ' %s -o %s'

    def rcc_command(self):
        return self.pyrcc + ' ' + self.pyrcc_options + ' %s -o %s'

    def load(self):
        for ext in ['.cfg', '.json']:
            try:
                with open('pyuic' + ext, 'r') as f:
                    self.__dict__ = json.load(f)
            except (IOError, OSError):
                pass
            else:
                break
        else:
            write_message('failed to open configuration file', 'yellow')
        if not hasattr(self, 'hooks'):
            self.hooks = []

    def save(self):
        with open('pyuic.json', 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def generate(self, api):
        try:
            config = apiConfigs[api]
        except IndexError:
            write_message('failed to generate pyuic.json. api not supported', 'red')
            return
        self.pyrcc = config.pyrcc
        self.pyrcc_options = config.pyrcc_options
        self.pyuic = config.pyuic
        self.pyuic_options = config.pyuic_options
        self.files[:] = []
        self.save()
        write_message('pyuic.json generated', 'green')

    def add(self, src, dst):
        self.load()
        for fn, _ in self.files:
            if fn == src:
                write_message('ui file already added: %s' % src)
                return
        self.files.append((src, dst))
        self.save()
        write_message('file added to pyuic.json: %s -> %s' % (src, dst), 'green')

    def remove(self, filename):
        self.load()
        to_remove = None
        for i, files in enumerate(self.files):
            src, dest = files
            if filename == src:
                to_remove = i
                break
        if to_remove is not None:
            self.files.pop(to_remove)
        self.save()
        write_message('file removed from pyuic.json: %s' % filename, 'green')
