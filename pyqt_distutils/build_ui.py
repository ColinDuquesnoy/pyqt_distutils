# -*- coding: utf-8 -*-
"""
Distutils extension for PyQt/PySide applications
"""
import glob
import os
from setuptools import Command

from .config import Config
from .hooks import load_hooks

class build_ui(Command):
    """
    Builds the Qt ui files as described in pyuic.json (or pyuic.cfg).
    """
    user_options = [
        ('force', None,
         'Force flag, will force recompilation of every ui/qrc file'),
    ]

    def initialize_options(self):
        self.force = False
        self._hooks = load_hooks()

    def finalize_options(self):
        try:
            self.cfg = Config()
            self.cfg.load()
        except (IOError, OSError):
            print('cannot open pyuic.json (or pyuic.cfg)')
            self.cfg = None

    def is_outdated(self, src, dst, ui):
        if src.endswith('.qrc') or self.force:
            return True
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
        for glob_exp, dest in self.cfg.files:
            for src in glob.glob(glob_exp):
                if not os.path.exists(src):
                    print('skipping target %s, file not found' % src)
                    continue
                src = os.path.join(os.getcwd(), src)
                dst = os.path.join(os.getcwd(), dest)
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
                except OSError:
                    pass

                if self.is_outdated(src, dst, ui):
                    print(cmd)
                    os.system(cmd)
                    for hookname in self.cfg.hooks:
                        try:
                            hook = self._hooks[hookname]
                        except KeyError:
                            print('warning, unknonw hook: %r' % hookname)
                        else:
                            print('running hook %r' % hookname)
                            hook(dst)
                else:
                    print('skipping %s, up to date' % src)
