from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint, QAbstractItemModel
from PyQt5.QtGui import QColor, QPalette, QPainter, QResizeEvent
from PyQt5.QtWidgets import (qApp, QWidget, QMainWindow,
                             QToolButton, QSizePolicy, QButtonGroup,
                             QVBoxLayout, QHBoxLayout, QFrame, QTableView,
                             QListView, QTreeView, QHeaderView)

from ui.CustomModelView.ui_horizontalHeaderView import Ui_CustomHeaderView


class HorizontalHeaderView(QHeaderView):
    """ 水平表头 """
    sorted_up = QtCore.pyqtSignal(int)
    sorted_down = QtCore.pyqtSignal(int)
    filter = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(HorizontalHeaderView, self).__init__(Qt.Horizontal, parent)
        self.setupUi(self)
        self._filterList = list()

    def paintSection(self, painter: QPainter,  rect: QRect, logical_index: int):
        pass

    def resizeEvent(self, event: QResizeEvent):
        pass

    def handleSectionMoved(self, logical: int , old_visual_index: int, new_visual_index: int ):
        pass

    def handleSectionResized(self, i: int, old_size: int , new_size: int ):
        pass

    def setModel(self, model: QAbstractItemModel):
        pass

    def headerDataChanged(self, orientation: Qt.Orientation, logicalFirst: int, logicalLast: int ):
        pass

    def fixSectionPositions(self):
        pass