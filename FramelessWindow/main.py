"""
无边框的自定义框架
"""
import sys
import qt_ui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator
from ui.FrameLessWidget.frameLessWidget import FrameLessWidget
from  ui.mainwindow import MainWindow


def main():
    """ """
    app = QtWidgets.QApplication(sys.argv)

    translator = QTranslator()
    translator.load(":/images/qt_zh_CN.qm")
    QtWidgets.QApplication.installTranslator(translator)
    ui = FrameLessWidget()
    widow = MainWindow()
    ui.set_content(widow)
    ui.set_window_title('Polaris')
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()