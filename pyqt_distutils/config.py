"""
Contains the config class (pyuic.cfg or pyuic.json)

"""
import json


class QtApi:
    pyqt4 = 0
    pyqt5 = 1
    pyside = 2


class Config:
    def __init__(self):
        self.files = []
        self.pyuic = ''
        self.pyuic_options = ''
        self.pyrcc = ''
        self.pyrcc_options = ''

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
            print('failed to open configuration file')

    def save(self):
        with open('pyuic.json', 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def generate(self, api):
        if api == QtApi.pyqt4:
            self.pyrcc = 'pyrcc4'
            self.pyrcc_options = '-py3'
            self.pyuic = 'pyuic4'
            self.pyuic_options = '--from-import'
            self.files[:] = []
        elif api == QtApi.pyqt5:
            self.pyrcc = 'pyrcc5'
            self.pyrcc_options = ''
            self.pyuic = 'pyuic5'
            self.pyuic_options = '--from-import'
            self.files[:] = []
        elif api == QtApi.pyside:
            self.pyrcc = 'pyside-rcc'
            self.pyrcc_options = '-py3'
            self.pyuic = 'pyside-uic'
            self.pyuic_options = '--from-import'
            self.files[:] = []
        self.save()
        print('pyuic.json generated')

    def add(self, src, dst):
        self.load()
        for fn, _ in self.files:
            if fn == src:
                print('ui file already added: %s' % src)
                return
        self.files.append((src, dst))
        self.save()
        print('file added to pyuic.json: %s -> %s' % (src, dst))

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
        print('file removed from pyuic.json: %s' % filename)
