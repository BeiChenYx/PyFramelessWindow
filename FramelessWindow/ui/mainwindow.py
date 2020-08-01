from PyQt5.QtCore import Qt, QEvent, QRect, QPoint, QModelIndex, QSortFilterProxyModel
from PyQt5.QtWidgets import (qApp, QWidget, QMainWindow, QLabel, QComboBox, QLineEdit,
                             QToolButton, QSizePolicy, QButtonGroup, QAbstractItemView,
                             QVBoxLayout, QHBoxLayout, QFrame, QTableView,
                             QListView, QTreeView, QTreeWidget, QTreeWidgetItem)

from ui.ui_mainwindow import Ui_MainWindow
from ui.CustomModelView.custommodel import CustomModel
from ui.CustomModelView.horizontalHeaderView import HorizontalHeaderView
from ui.basicWidget import BasicWidget
from ui.drawingControl import DrawingControl


class VersionInfoWidget(QWidget):

    def __init__(self, version='V1.0.0', parent=None):
        super(VersionInfoWidget, self).__init__(parent)
        self.setObjectName('customStatusBar')
        h_layout = QHBoxLayout()
        label = QLabel(version)
        h_layout.addWidget(label)
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h_layout)
        self.setStyleSheet("#customStatusBar QLabel{color: #FFFFFF;}")


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        # 框架 --start
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._left_nav_btn_list = list()
        # 顶级Item且没有子Item的不保存，子Item保存parent的属性，顶级Item的parent为空字符串, 每个Item维护QStackWidget索引
        # self._left_nav_tree_dict = {
        #     'QLabel': {
        #         'parent': '',
        #         'stack_index': 1
        #     },
        #     'QLineEdit1': {
        #         'parent': 'QLineEdit',
        #         'stack_index': 2
        #     },
        #     'QLineEdit2': {
        #         'parent': 'QLineEdit',
        #         'stack_index': 3
        #     },
        #     'QTreeWidget': {
        #         'parent': '',
        #         'stack_index': 4
        #     }
        # }
        self._left_nav_tree_dict = dict()
        self._nav_v_layout = QVBoxLayout()
        self._nav_v_layout.setContentsMargins(0, 0, 0, 0)
        self._button_group_nav = QButtonGroup(self)
        self._version_widget = VersionInfoWidget('版本号: V1.0.0')
        # 框架 --end

        self._nav_tree_widget = QTreeWidget(self)

        self._basic_widget = BasicWidget(self)
        self._table_view = QTableView(self)
        self._list_view = QListView(self)
        self._tree_view = QTreeView(self)
        self._model = CustomModel(self)
        self._sort_filter_model = QSortFilterProxyModel()
        self._h_table_header = HorizontalHeaderView(self._table_view)
        self._drawing_control = DrawingControl(self)

        # 框架 --start
        self.init_ui()
        self.init_connect()
        self.init_qss()
        # 框架 --end

    def init_ui(self):
        # 框架 --start
        h_layout = QVBoxLayout()
        h_layout.addLayout(self._nav_v_layout)
        h_layout.addStretch()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_left_nav.setLayout(h_layout)
        self.statusbar.addPermanentWidget(self._version_widget)
        for combo_box in self.findChildren(QComboBox):
            combo_box.setView(QListView())
        # 框架 --end

        self.add_nav_stack_widget('', '基本控件', self._basic_widget)
        self.add_nav_h_line()

        table_widget = QWidget(self);
        table_widget.setLayout(QHBoxLayout())
        table_widget.layout().addWidget(self._table_view)
        table_widget.setObjectName("tableWidget")
        self.add_nav_stack_widget("tableBtn", "tableView", table_widget)

        list_widget = QWidget(self)
        list_widget.setLayout(QHBoxLayout())
        list_widget.layout().addWidget(self._list_view)
        list_widget.setObjectName("listWidget")
        self.add_nav_stack_widget("listBtn", "listView", list_widget)

        tree_widget = QWidget(self)
        tree_widget.setLayout(QHBoxLayout())
        tree_widget.layout().addWidget(self._tree_view)
        tree_widget.setObjectName("treeWidget")
        self.add_nav_stack_widget("treeBtn", "treeView", tree_widget)

        self.add_nav_h_line()
        self.add_nav_stack_widget("", "自绘控件", self._drawing_control)

        self._nav_v_layout.addWidget(self._nav_tree_widget)
        self._nav_tree_widget.setColumnCount(1)
        self._nav_tree_widget.setHeaderHidden(True)
        self._nav_tree_widget.setIndentation(14)

        label = QLabel('QLable')
        self.add_nav_top_stack_widget('QLabel', label)
        self.add_nav_top_stack_widget('QLineEdit')
        edit1 = QLineEdit('QLineEdit1')
        edit2 = QLineEdit('QLineEdit2')
        self.add_nav_child_stack_widget('QLineEdit1', 'QLineEdit', edit1)
        self.add_nav_child_stack_widget('QLineEdit2', 'QLineEdit', edit2)

        tree_label = QLabel('QTreeWidget')
        self.add_nav_top_stack_widget('QTreeWidget', tree_label)

        self._table_view.setHorizontalHeader(self._h_table_header)
        self._sort_filter_model.setSourceModel(self._model)
        self._table_view.setModel(self._sort_filter_model)
        self._list_view.setModel(self._model)
        self._tree_view.setModel(self._model)
        self._table_view.setColumnWidth(1, 150)
        self._table_view.setAlternatingRowColors(True)
        self._table_view.horizontalHeader().setStretchLastSection(True)
        self._table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table_view.setSelectionMode(QAbstractItemView.SingleSelection)

    def init_connect(self):
        self._button_group_nav.buttonClicked.connect(self.on_btn_group_clicked)
        self._table_view.pressed.connect(self.on_table_view_pressed)
        self._h_table_header.sorted_up.connect(self.on_sort_up)
        self._h_table_header.sorted_down.connect(self.on_sort_down)
        self._h_table_header.filter.connect(self.on_filter)
        self._nav_tree_widget .itemClicked.connect(self.on_tree_widget_item_clicked)

    def on_tree_widget_item_clicked(self, item: QTreeWidgetItem, column: int):
        if column > 1:
            return
        if item.childCount():
            if item.isExpanded():
                self._nav_tree_widget.collapseItem(item)
            else:
                self._nav_tree_widget.expandItem(item)
        else:
            name = item.text(0)
            value = self._left_nav_tree_dict[name]
            self.stackedWidget.setCurrentIndex(value['stack_index'])
            print('name: ', name, '  value: ', value)

    def on_table_view_pressed(self, index: QModelIndex):
        print('selected: ', index.row(), ' data: ', self._table_view.model().data(index))

    def on_sort_up(self, index: int):
        self._sort_filter_model.setFilterKeyColumn(index)
        self._sort_filter_model.sort(index, Qt.AscendingOrder)

    def on_sort_down(self, index: int):
        self._sort_filter_model.setFilterKeyColumn(index)
        self._sort_filter_model.sort(index, Qt.DescendingOrder)

    def on_filter(self, index: int, msg: str):
        self._sort_filter_model.setFilterKeyColumn(index)
        self._sort_filter_model.setFilterFixedString(msg)

    def on_btn_group_clicked(self, obj):
        self.stackedWidget.setCurrentIndex(self._button_group_nav.id(obj))
        obj.setChecked(True)

    def init_qss(self):
        """ 初始化样式 """
        with open("./ui/mainWindow.css", 'r', encoding="utf-8") as fi:
            sheet = fi.read()
            self.setStyleSheet(sheet)

    def add_nav_stack_widget(self, name: str, text: str, widget: QWidget):
        """
        添加自定义的页面到QStackWidget中，并添加左导航栏按钮
        :name: 左导航按钮需要显示的名字
        :widget: 需要插入的页面
        """
        btn_id = len(self._left_nav_btn_list)
        tool_btn = QToolButton(self)
        self._left_nav_btn_list.append(tool_btn)
        tool_btn.setText(text);
        tool_btn.setToolButtonStyle(Qt.ToolButtonTextOnly);
        tool_btn.setCheckable(True);
        tool_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if not name.strip():
            tool_btn.setObjectName(name)
        self._button_group_nav.addButton(tool_btn, btn_id)
        self._nav_v_layout.addWidget(tool_btn)
        self.stackedWidget.addWidget(widget)

    def add_nav_h_line(self):
        """
        向导航栏中添加水平分割线
        """
        line = QFrame(self)
        line.setGeometry(QRect(40, 180, 400, 3))
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.raise_()
        line.setObjectName("HLine")
        self._nav_v_layout.addWidget(line)

    def add_nav_top_stack_widget(self, text: str, widget: QWidget = None):
        """
        QTreeWidget中插入顶级Item
        :param text: Item的名字
        :param widget: 对应在QStackWidget插入的页面，None表示该Item下面还有子Item，因此这个不插入QStackWidget
        :return: 无
        """
        if text.strip() in self._left_nav_tree_dict.keys():
            return

        item_id = len(self._left_nav_tree_dict.keys()) + len(self._left_nav_btn_list)
        item = QTreeWidgetItem(self._nav_tree_widget, [text, ])
        self._nav_tree_widget.addTopLevelItem(item)
        if widget:
            self._left_nav_tree_dict[text] = {'parent': '', 'stack_index': item_id}
            self.stackedWidget.addWidget(widget)

    def add_nav_child_stack_widget(self, text: str, parent_text: str, widget: QWidget):
        """
        QTreeWidget中插入子对象
        :param text: Item的名字
        :param parent_text: 父对象的名字
        :param widget: 要插入的页面
        :return: 无
        """
        if text.strip() in self._left_nav_tree_dict.keys() and parent_text.strip() == '':
            return

        items = self._nav_tree_widget.findItems(parent_text, Qt.MatchFixedString)
        if not len(items):
            return

        parent_item = items[0]
        child_item = QTreeWidgetItem(parent_item, [text, ])
        parent_item.addChild(child_item)
        item_id = len(self._left_nav_tree_dict.keys()) + len(self._left_nav_btn_list)
        self._left_nav_tree_dict[text] = {'parent': parent_text, 'stack_index': item_id}
        self.stackedWidget.addWidget(widget)


