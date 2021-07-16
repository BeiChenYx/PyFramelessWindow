"""
树形结构的模型
"""
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint, QDateTime, QVariant
from PyQt5.QtCore import QAbstractItemModel, QModelIndex

class NodeIndex:
    """ 树形结构节点类 """

    def __init__(self, path:str, parent=None):
        self._path = path
        self._name = path[path.rindex('/')+1:]

        self._parent = parent
        self._children_node = list()
        self._row_number_in_parent = 0;
        self._data = dict()

    def row_number_in_parent(self) -> int:
        return self._row_number_in_parent

    def set_row_number(self, row_number):
        self._row_number_in_parent = row_number

    def name(self) -> str:
        return self._name

    def path(self) -> str:
        return self._path

    def set_data(self, key, value) -> bool:
        self._data[key] = value
        return True

    def data(self, key, default_data="**"):
        return self._data.get(key, default_data)

    def parent(self):
        return self._parent

    def child_from_index(self, index):
        if 0 <= index < len(self._children_node):
            return self._children_node[index]
        return NodeIndex('****', None)

    def child_from_name(self, name):
        for node in self._children_node:
            if node.name() == name:
                return node

        return NodeIndex('****', None)

    def children_count(self):
        return len(self._children_node)

    def remove_child(self, index):
        del self._children_node[index]

    def add_child(self, node):
        node.set_row_number(len(self._children_node) + 1)
        self._children_node.append(node)


class CTreeModel(QAbstractItemModel):
    """ 树形结构的模型类 """

    def __init__(self, parent=None):
        super(CTreeModel, self).__init__(parent)
        self._header_name = list("ABCDEF")
        self._root_item = NodeIndex("/root")
        
        self.init_data()

    def init_data(self):
        header_size = len(self._header_name)
        for i in range(10):
            path = '{0}/{1}'.format(self._root_item.path(), str(i))
            tmp = NodeIndex(path, self._root_item)
            for col in range(header_size):
                key = self._header_name[col]
                tmp.set_data(key, '{0}{1}{2}'.format(key, i, col))

            self._root_item.add_child(tmp)
            for j in range(5):
                child_path = '{0}{1}'.format(path, i*10+j+1)
                child_tmp = NodeIndex(child_path, tmp)
                tmp.add_child(child_tmp)
                for col in range(header_size):
                    key = self._header_name[col]
                    child_tmp.set_data(key, '{0}{1}{2}'.format(key, key, col))

    def item_from_index(self, index: QModelIndex):
        if index.isValid():
            return index.internalPointer()

        return self._root_item

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.column() > 0:
            return 0

        item = self.item_from_index(parent)
        return item.children_count()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._header_name)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            col = index.column()
            item = self.item_from_index(index)
            return item.data(self._header_name[col], "")
        elif role == Qt.EditRole:
            col = index.column()
            item = self.item_from_index(index)
            return item.data(self._header_name[col], "")
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QVariant()

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            return True

        return False

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_item = self.item_from_index(parent)
        item = parent_item.child_from_index(row)
        if item != None:
            return self.createIndex(row, column, item)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        item = self.item_from_index(index)
        parent_item = item.parent()
        if parent_item == self._root_item or parent_item == None:
            return QModelIndex()

        return self.createIndex(parent_item.row_number_in_parent(),
                                0, parent_item)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            _flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemNeverHasChildren | Qt.ItemIsEditable
            return _flags
        return QAbstractItemModel.flags(index)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section < 0 or section > len(self._header_name):
                return QVariant()

            return QVariant(self._header_name[section])
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


