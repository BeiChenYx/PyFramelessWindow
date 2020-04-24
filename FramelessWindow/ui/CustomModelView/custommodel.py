from random import randint

from PyQt5.QtCore import Qt, QEvent, QRect, QPoint, QDateTime, QVariant
from PyQt5.QtCore import QAbstractItemModel, QModelIndex


class CustomModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(CustomModel, self).__init__(parent)
        self._names = ["code", "no1", "no2", "no3", "name", "datetime"]
        now = QDateTime.currentDateTime()
        self._stocks = [[i, i*100, randint(0, 100), randint(0, 300), "name%d" % randint(0, 100), now.addSecs(i)]
                        for i in range(10)]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._stocks)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._names)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if index.row() > len(self._stocks) or index.column() > len(self._names):
            return QVariant()
        if role == Qt.DisplayRole:
            stock = self._stocks[index.row()]
            return stock[index.column()]
        elif role == Qt.EditRole:
            stock = self._stocks[index.row()]
            return stock[index.column()]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QVariant()

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            self._stocks[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            _flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemNeverHasChildren | Qt.ItemIsEditable
            return _flags
        return QAbstractItemModel.flags(index)

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if row < 0 or column < 0 or column >= self.columnCount(parent) or column > len(self._names):
            return QModelIndex()
        return self.createIndex(row, column)

    def parent(self, child: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(self._names[section])
        else:
            return QVariant(section)

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value, role: int = Qt.EditRole) -> bool:
        if role != Qt.EditRole:
            return False
        if orientation == Qt.Horizontal:
            # self._names[section] = value
            # self.headerDataChanged.emit(Qt.Horizontal, section, section)
            return False
        else:
            return False
