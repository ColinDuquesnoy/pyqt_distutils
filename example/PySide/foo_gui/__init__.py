import sys
from PySide import QtGui
from .forms import main_window_ui


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = main_window_ui.Ui_MainWindow()
    ui.setupUi(window)
    ui.label.setText(str(window))
    window.show()
    app.exec_()
