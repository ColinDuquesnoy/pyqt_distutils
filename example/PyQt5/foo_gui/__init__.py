import sys
from PyQt5 import QtWidgets
from .forms import main_window_ui


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = main_window_ui.Ui_MainWindow()
    ui.setupUi(window)
    ui.label.setText(str(window))
    window.show()
    app.exec_()
