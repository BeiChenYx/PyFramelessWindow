from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel

from ui.DrawingControl.navProgressBar import NavProgressBar


class DrawingControl(QWidget):
    """ 基本控件页面 """

    def __init__(self, parent=None):
        super(DrawingControl, self).__init__(parent)
        self.setObjectName('DrawingControl')
        self._nav_progress = NavProgressBar()
        # self._widget1 = QWidget(self)
        self.init_ui()

    def init_ui(self):
        top_info = ['创建订单', '审核订单', '生产', '配送', '签收']
        self._nav_progress.set_top_info(top_info)
        self._nav_progress.max_step = len(top_info)
        self._nav_progress.current_step = 4
        self._nav_progress.current_background = QColor(24, 189, 155)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self._nav_progress)
        v_layout.addStretch()
        # self._widget1.setLayout(v_layout)
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel('test'))
        self.setLayout(h_layout)


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    ui = DrawingControl()
    ui.resize(500, 100)
    ui.show()
    sys.exit(app.exec_())
