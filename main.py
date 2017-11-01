#!/usr/bin/python3
from PyQt5 import QtWidgets
import sys
from main_form import polynomial_window
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = polynomial_window()
    sys.exit(app.exec())


