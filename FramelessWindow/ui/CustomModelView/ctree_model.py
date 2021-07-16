"""
树形结构的模型
"""

class NodeIndex:
    """ 树形结构节点类 """

    def __init__(self, path:str, parent=None):
        self._path = path
        self._name = ''
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

    def data(self, key, default_data):
        return self._data.get(key, '')

    def parent(self):
        return self._parent

    def child_from_index(self, index):
        if 0 <= index < len(self._children_node):
            return self._children_node[index]

    def child_from_name(self, name):
        for node in self._children_node:
            if node.name() == name:
                return node
        finally:
            return None

    def children_count(self):
        return len(self._children_node)

    def remove_child(index):
        del self._children_node[index]

    def add_child(node):
        self._children_node.append(node)
