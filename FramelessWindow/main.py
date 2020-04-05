"""
无边框的自定义框架
"""
import sys
import qt_ui as qui
from PyQt5 import QtWidgets, QtGui, QtCore
from ui.frameLessWidget import FrameLessWidget


def main():
    """ """
    app = QtWidgets.QApplication(sys.argv)
    ui = FrameLessWidget()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()