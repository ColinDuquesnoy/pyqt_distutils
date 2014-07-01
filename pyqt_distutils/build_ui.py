# -*- coding: utf-8 -*-
"""
Distutils extension for PyQt/PySide applications
"""
import os
from setuptools import Command

from .config import Config


class build_ui(Command):
    """
    Builds the Qt ui files as described in pyuic.cfg.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        try:
            self.cfg = Config()
            self.cfg.load()
        except (IOError, OSError):
            print('cannot open pyuic.cfg')
            self.cfg = None

    def is_outdated(self, src, dst, ui):
        outdated = (not os.path.exists(dst) or
                    (os.path.getmtime(src) > os.path.getmtime(dst)))
        if not outdated and not ui:
            # for qrc files, we need to check each individual resources.
            # If one of them is newer than the dst file, the qrc file must be
            # considered as outdated
            # file paths are relative to the qrc file path
            qrc_dirname = os.path.dirname(src)
            with open(src, 'r') as f:
                lines = f.read().splitlines()
                lines = [l for l in lines if '<file>' in l]
            cwd = os.getcwd()
            os.chdir(qrc_dirname)
            for line in lines:
                filename = line.replace('<file>', '').replace(
                    '</file>', '').strip()
                filename = os.path.abspath(filename)
                if os.path.getmtime(filename) > os.path.getmtime(dst):
                    outdated = True
                    break
            os.chdir(cwd)
        return outdated

    def run(self):
        if not self.cfg:
            return
        for src, dst in self.cfg.files:
            if not os.path.exists(src):
                print('skipping target %s, file not found' % src)
                continue
            src = os.path.join(os.getcwd(), src)
            dst = os.path.join(os.getcwd(), dst)
            ui = True
            if src.endswith('.ui'):
                ext = '_ui.py'
                cmd = self.cfg.uic_command()
            elif src.endswith('.qrc'):
                ui = False
                ext = '_rc.py'
                cmd = self.cfg.rcc_command()
            else:
                continue
            filename = os.path.split(src)[1]
            filename = os.path.splitext(filename)[0]
            dst = os.path.join(dst, filename + ext)
            cmd = cmd % (src, dst)
            try:
                os.makedirs(os.path.split(dst)[0])
            except FileExistsError:
                pass

            if self.is_outdated(src, dst, ui):
                print(cmd)
                os.system(cmd)
            else:
                print('skipping %s, up to date' % src)
