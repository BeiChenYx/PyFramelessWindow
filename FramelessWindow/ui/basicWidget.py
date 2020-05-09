from PyQt5.QtWidgets import QWidget
from ui.ui_basicwidget import Ui_BasicWidget


class BasicWidget(QWidget, Ui_BasicWidget):
    """ 基本控件页面 """

    def __init__(self, parent=None):
        super(BasicWidget, self).__init__(parent)
        self.setupUi(self)
