"""
A pyqt-distutils hook is a python function that is called after the
compilation of a ui script to let you customise its content. E.g. you
might want to write a hook to change the translate function used or replace
the PyQt imports by your owns if you're using a shim,...

The hook function is a simple python function which must take a single
argument: the path to the generated python script.

Hooks are exposed as setuptools entrypoint using :attr:`ENTRYPOINT` as the
entrypoint key. E.g., in your setup.py::

    setup(
        ...,
        entry_points={
            'pyqt_distutils_hooks': [
                'hook_name = package_name.module_name:function_name']
        },
        ...)



There is a "hooks" config key where you can list the hooks
that you want to run on all your ui/qrc scripts. E.g.::

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
use ``gettext.gettext`` instead of ``QCoreApplication.translate``.

"""
import pkg_resources
import traceback


#: Name of the entrypoint to use in setup.py
ENTRYPOINT = 'pyqt_distutils_hooks'


def load_hooks():
    """
    Load the exposed hooks.

    Returns a dict of hooks where the keys are the name of the hook and the
    values are the actual hook functions.
    """
    hooks = {}
    for entrypoint in pkg_resources.iter_entry_points(ENTRYPOINT):
        name = str(entrypoint).split('=')[0].strip()
        try:
            hook = entrypoint.load()
        except Exception:
            traceback.print_exc()
        else:
            hooks[name] = hook
    return hooks


def hook(ui_file_path):
    """
    This is the prototype of a hook function.
    """
    pass


GETTEXT_REPLACEMENT = '''        import gettext
        def _translate(_, string):
            return gettext.gettext(string)
'''


def gettext(ui_file_path):
    """
    Let you use gettext instead of the Qt tools for l18n
    """
    with open(ui_file_path, 'r') as fin:
        content = fin.read()
    with open(ui_file_path, 'w') as fout:
        fout.write(content.replace(
            '        _translate = QtCore.QCoreApplication.translate',
            GETTEXT_REPLACEMENT))
