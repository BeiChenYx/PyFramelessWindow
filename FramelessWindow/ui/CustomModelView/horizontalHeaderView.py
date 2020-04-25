from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint, QAbstractItemModel, QSize
from PyQt5.QtGui import QColor, QPalette, QPainter, QResizeEvent
from PyQt5.QtWidgets import (qApp, QWidget, QMainWindow,
                             QToolButton, QSizePolicy, QButtonGroup,
                             QVBoxLayout, QHBoxLayout, QFrame, QTableView,
                             QListView, QTreeView, QHeaderView, QPushButton,
                             QLineEdit)

from ui.CustomModelView.ui_horizontalHeaderView import Ui_CustomHeaderView


class FilterDialog(QWidget):
    """ 过滤信息弹框 """
    filter_msg = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(FilterDialog, self).__init__(parent)
        self._btn = QPushButton(self)
        self._btn.setText('确定')
        self._line_edit = QLineEdit(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self._line_edit)
        h_layout.addWidget(self._btn)
        h_layout.setSpacing(3)
        h_layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(h_layout)
        self.setWindowModality(Qt.ApplicationModal)
        self._btn.clicked.connect(self.on_btn_clicked)

    def get_filter_msg(self):
        return self._line_edit.text().strip()

    def on_btn_clicked(self):
        self.filter_msg.emit(self.get_filter_msg())
        self.close()


class CustomHeaderView(QWidget, Ui_CustomHeaderView):
    """ 自定义表头的页面 """
    sorted_up = QtCore.pyqtSignal(int)
    sorted_down = QtCore.pyqtSignal(int)
    filter = QtCore.pyqtSignal(int, str)

    def __init__(self, index: int, parent=None):
        super(CustomHeaderView, self).__init__(parent)
        self.setupUi(self)
        self._index = index
        self._filter_dialog = FilterDialog()
        self._filter_dialog.hide()
        self.sort_up_visible(False)
        self.sort_down_visible(False)
        self.filter_visible(False)
        self.init_connect()

        self.label_title.installEventFilter(self)
        self.toolButton_filter.installEventFilter(self)
        self.toolButton_sortUp.installEventFilter(self)
        self.toolButton_sortDown.installEventFilter(self)
        self.widget_header.installEventFilter(self)

    def init_connect(self):
        def on_up():
            self.buttonGroup.setExclusive(True)
            self.toolButton_filter.setChecked(False)
            self.toolButton_sortUp.setChecked(True)
            self.toolButton_sortDown.setChecked(False)
            self.sorted_up.emit(self._index)

        def on_down():
            self.buttonGroup.setExclusive(True)
            self.toolButton_filter.setChecked(False)
            self.toolButton_sortUp.setChecked(False)
            self.toolButton_sortDown.setChecked(True)
            self.sorted_down.emit(self._index)

        def on_filter():
            self.buttonGroup.setExclusive(True)
            self.toolButton_filter.setChecked(True)
            self.toolButton_sortUp.setChecked(False)
            self.toolButton_sortDown.setChecked(False)
            zero = self.mapToGlobal(QPoint(self.label_title.pos().x(), self.label_title.pos().y()))
            self._filter_dialog.move(zero.x(), zero.y() + self.height())
            self._filter_dialog.resize(self.size() + QSize(5, 0))
            self._filter_dialog.show()

        def on_filter_dialog(msg: str):
            self.filter.emit(self._index, msg)

        self.toolButton_sortUp.clicked.connect(on_up)
        self.toolButton_sortDown.clicked.connect(on_down)
        self.toolButton_filter.clicked.connect(on_filter)
        self._filter_dialog.filter_msg.connect(on_filter_dialog)

    def set_title(self, text: str):
        self.label_title.setText(text)

    def title(self):
        return self.label_title.text()

    def set_alignment(self, align: Qt.Alignment):
        self.label_title.setAlignment(align)

    def sort_up_visible(self, status: bool):
        self.toolButton_sortUp.setVisible(status)

    def sort_down_visible(self, status: bool):
        self.toolButton_sortDown.setVisible(status)

    def filter_visible(self, status: bool):
        self.toolButton_filter.setVisible(status)

    def clear_status(self):
        self.buttonGroup.setExclusive(False)
        self.toolButton_filter.setChecked(False)
        self.toolButton_sortDown.setChecked(False)
        self.toolButton_sortUp.setChecked(False)

    def clear_filter_status(self):
        self.buttonGroup.setExclusive(False)
        self.toolButton_filter.setChecked(False)

    def get_filter_msg(self) -> str:
        return self._filter_dialog.get_filter_msg()

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent):
        if (obj == self.widget_header or obj == self.label_title
                or obj == self.toolButton_filter or obj == self.toolButton_sortUp
                or obj == self.toolButton_sortDown):
            self.setCursor(Qt.ArrowCursor)
        if event.type() == QEvent.Leave and obj == self.widget_header:
            self.toolButton_filter.setVisible(False)
            self.toolButton_sortUp.setVisible(False)
            self.toolButton_sortDown.setVisible(False)
        elif event.type() == QEvent.Enter and obj == self.widget_header:
            self.toolButton_filter.setVisible(True)
            self.toolButton_sortUp.setVisible(True)
            self.toolButton_sortDown.setVisible(True)
        return QWidget.eventFilter(self, obj, event)


class HorizontalHeaderView(QHeaderView):
    """ 水平表头 """
    sorted_up = QtCore.pyqtSignal(int)
    sorted_down = QtCore.pyqtSignal(int)
    filter = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        super(HorizontalHeaderView, self).__init__(Qt.Horizontal, parent)
        self.HEADER_RIGHT_BORDER = 1
        self._filterList = list()
        self.sectionResized.connect(self.handle_section_resized)
        self.sectionMoved.connect(self.handle_section_moved)

    def paintSection(self, painter: QPainter,  rect: QRect, logical_index: int):
        painter.save()
        super(HorizontalHeaderView, self).paintSection(painter, QRect(), logical_index)
        painter.restore()
        table_filter = self._filterList[logical_index]
        table_filter.setGeometry(self.sectionViewportPosition(logical_index), 0,
                                 self.sectionSize(logical_index) - self.HEADER_RIGHT_BORDER,
                                 self.height())
        table_filter.show()
        start_show_index = self.visualIndexAt(0)
        for i in range(start_show_index):
            self._filterList[i].hide()

    def resizeEvent(self, event: QResizeEvent):
        super(HorizontalHeaderView, self).resizeEvent(event)
        self.fix_section_positions()

    def handle_section_moved(self, logical: int , old_visual_index: int, new_visual_index: int ):
        self.fix_section_positions()

    def handle_section_resized(self, i: int, old_size: int, new_size: int ):
        self.fix_section_positions()

    def setModel(self, model: QAbstractItemModel):
        def on_up(index: int):
            self.sorted_up.emit(index)
            for row in range(len(self._filterList)):
                if row != index:
                    self._filterList[row].clear_status()

        def on_down(index: int):
            self.sorted_down.emit(index)
            for row in range(len(self._filterList)):
                if row != index:
                    self._filterList[row].clear_status()

        def on_filter(index: int, msg: str):
            if self._filterList[index].get_filter_msg().strip() == "":
                self._filterList[index].clear_status()
            self.filter.emit(index, msg)

        super(HorizontalHeaderView, self).setModel(model)
        for i in range(self.count()):
            table_filter = CustomHeaderView(i, self)
            table_filter.set_title(self.model().headerData(i, Qt.Horizontal))
            table_filter.show()
            self._filterList.append(table_filter)
            table_filter.sorted_up.connect(on_up)
            table_filter.sorted_down.connect(on_down)
            table_filter.filter.connect(on_filter)

    def headerDataChanged(self, orientation: Qt.Orientation, logicalFirst: int, logicalLast: int ):
        if logicalFirst < 0 or logicalLast > len(self._filterList):
            return
        if orientation == Qt.Horizontal:
            for i in range(logicalFirst, logicalLast):
                self._filterList[i].set_title(self.model().headerData(i, Qt.Horizontal))

    def fix_section_positions(self):
        for row in range(len(self._filterList)):
            self._filterList[row].setGeometry(self.sectionViewportPosition(row), 0,
                                              self.sectionSize(row) - self.HEADER_RIGHT_BORDER,
                                              self.height())
