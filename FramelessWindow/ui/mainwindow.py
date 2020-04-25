from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint, QModelIndex, QSortFilterProxyModel
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (qApp, QWidget, QMainWindow,
                             QToolButton, QSizePolicy, QButtonGroup,
                             QVBoxLayout, QHBoxLayout, QFrame, QTableView,
                             QListView, QTreeView, QAbstractItemView)

from ui.ui_mainwindow import Ui_MainWindow
from ui.CustomModelView.custommodel import CustomModel
from ui.CustomModelView.horizontalHeaderView import HorizontalHeaderView


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._left_nav_btn_list = list()
        self._nav_v_layout = QVBoxLayout()
        self._nav_v_layout.setContentsMargins(0, 0, 0, 0)
        self._button_group_nav = QButtonGroup(self)
        self._widget_base = QWidget(self)
        self._table_view = QTableView(self)
        self._list_view = QListView(self)
        self._tree_view = QTreeView(self)
        self._model = CustomModel(self)
        self._sort_filter_model = QSortFilterProxyModel()
        self._h_table_header = HorizontalHeaderView(self._table_view)
        self.init_ui()
        self.init_connect()
        self.init_qss()

    def init_ui(self):
        h_layout = QVBoxLayout()
        h_layout.addLayout(self._nav_v_layout)
        h_layout.addStretch()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_left_nav.setLayout(h_layout)
        self.add_nav_stack_widget('', '控件', self._widget_base)
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
        self.add_nav_stack_widget("", "自绘控件", QWidget(self))

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
