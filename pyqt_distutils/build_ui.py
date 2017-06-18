# -*- coding: utf-8 -*-
"""
Distutils extension for PyQt/PySide applications
"""
import glob
import os
import subprocess
import sys

from setuptools import Command

from .config import Config
from .hooks import load_hooks
from .utils import build_args, write_message


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
            write_message('cannot open pyuic.json (or pyuic.cfg)', 'red')
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
                    write_message('skipping target %s, file not found' % src, 'yellow')
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
                try:
                    os.makedirs(os.path.split(dst)[0])
                except OSError:
                    pass

                if self.is_outdated(src, dst, ui):
                    try:
                        cmd = build_args(cmd, src, dst)
                        subprocess.check_call(cmd)
                        cmd = ' '.join(cmd)
                    except subprocess.CalledProcessError as e:
                        if e.output:
                            write_message(cmd, 'yellow')
                            write_message(e.output.decode(sys.stdout.encoding), 'red')
                        else:
                            write_message(cmd, 'red')
                    except OSError as e:
                        write_message(cmd, 'yellow')
                        write_message(str(e), 'red')
                    else:
                        write_message(cmd, 'green')
                    for hookname in self.cfg.hooks:
                        try:
                            hook = self._hooks[hookname]
                        except KeyError:
                            write_message('warning, unknonw hook: %r' % hookname, 'yellow')
                        else:
                            write_message('running hook %r' % hookname, 'blue')
                            hook(dst)
                else:
                    write_message('skipping %s, up to date' % src)
