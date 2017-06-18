import unittest

from pyqt_distutils.utils import build_args

class CreateDatabaseTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_args(self):
        """
            Basic argument building test with build_args method.
        """
        cmd = 'python -m PyQt5.uic.pyuic --from-import %s -o %s'
        src = '/path/a'
        dst = '/path/b'

        args = build_args(cmd, src, dst)
        expected = ['python', '-m', 'PyQt5.uic.pyuic', '--from-import', '/path/a', '-o', '/path/b']
        self.assertListEqual(args, expected)

    def test_build_args_empty_token_removal(self):
        """
            Argument building test for removal of empty tokens with build_args method.

            Test for regression of: https://github.com/ColinDuquesnoy/pyqt_distutils/issues/7
        """
        cmd = 'pyrcc5  %s -o %s'
        src = '/path/a'
        dst = '/path/b'

        args = build_args(cmd, src, dst)
        expected = ['pyrcc5', '/path/a', '-o', '/path/b']
        self.assertListEqual(args, expected)

    def test_build_args_paths_with_spaces(self):
        """
            Argument building test for paths with spaces using build_args method.

            Test for regression of: https://github.com/ColinDuquesnoy/pyqt_distutils/pull/9
        """
        cmd = 'python -m PyQt5.uic.pyuic --from-import %s -o %s'
        src = '/path/a space/path'
        dst = '/path/b space/path'

        args = build_args(cmd, src, dst)
        expected = ['python', '-m', 'PyQt5.uic.pyuic', '--from-import', '/path/a space/path', '-o', '/path/b space/path']
        self.assertListEqual(args, expected)
