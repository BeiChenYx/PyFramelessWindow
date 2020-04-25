import platform
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtWidgets import qApp, QWidget, QHBoxLayout

from ui.FrameLessWidget.ui_framelesswidget import Ui_FramelessWidget


class FrameLessWidget(QtWidgets.QWidget, Ui_FramelessWidget):
    """无边框界面, PyQt5中无法使用窗口提升功能，所以移动和窗口放大缩小要坐在一个类中"""
    CONST_DRAG_BORDER_SIZE = 15

    def __init__(self, is_max=True, is_full=True, parent=None):
        super(FrameLessWidget, self).__init__(parent)
        self.setupUi(self)
        self._is_max = is_max
        self._is_full = is_full if self._is_max else False
        self._full_point = QtCore.QPoint()
        self._full_size = QtCore.QSize()
        self._start_geometry = QRect()
        self._mouse_pressed = False
        self._mouse_pressed_title = False
        self._drag_top = False
        self._drag_left = False
        self._drag_right = False
        self._drag_bottom = False
        self._mouse_pos = QPoint()
        self._wnd_pos = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_qss()
        self.init_ui()
        self.init_connections()
        self.setWindowIcon(QtGui.QIcon(":/images/logo.png"))
        QtWidgets.QApplication.instance().installEventFilter(self)

    def init_qss(self):
        """ 初始化样式 """
        with open("./ui/FrameLessWidget/sheet.css", 'r', encoding="utf-8") as fi:
            sheet = fi.read()
            self.setStyleSheet(sheet)

    def init_ui(self):
        """ 初始化UI """
        self.toolButton_restore.setVisible(False)
        self.toolButton_full.setVisible(False)
        self.toolButton_full_exit.setVisible(False)
        self.toolButton_max.setVisible(self._is_max)
        text_shadow = QGraphicsDropShadowEffect()
        text_shadow.setBlurRadius(4.0)
        text_shadow.setColor(QColor(0, 0, 0))
        text_shadow.setOffset(0.0)
        self.label_title.setGraphicsEffect(text_shadow)
        self.style_window(True, True)

    def init_connections(self):
        """ 初始化信号槽 """
        qApp.applicationStateChanged.connect(self.on_application_state_changed)
        self.toolButton_close.clicked.connect(self.close)
        self.toolButton_max.clicked.connect(self.on_tool_button_max_clicked)
        self.toolButton_restore.clicked.connect(self.on_tool_button_restore_clicked)
        self.toolButton_min.clicked.connect(self.on_tool_button_min_clicked)
        self.toolButton_full.clicked.connect(self.on_tool_button_full_clicked)
        self.toolButton_full_exit.clicked.connect(self.on_tool_button_full_exit_clicked)

    def set_window_title(self, title):
        self.label_title.setText(title)
        self.setWindowTitle(title)

    def set_window_icon(self, ico: QIcon):
        self.label_icon.setPixmap(ico.pixmap(24, 24))
        self.setWindowIcon(ico)

    def set_content(self, w: QtWidgets.QWidget):
        h_layout = QHBoxLayout()
        h_layout.addWidget(w)
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.windowContent.setLayout(h_layout)

    def style_window(self, active, no_state):
        """ 设置UI风格 """
        color = self.palette().color(QPalette.Highlight if active else QPalette.Shadow)
        if no_state:
            if platform.system() == "Windows":
                self.layout().setContentsMargins(15, 15, 15, 15)
            else:
                self.layout().setContentsMargins(0, 0, 0, 0)
            text_shadow = QGraphicsDropShadowEffect()
            text_shadow.setBlurRadius(9.0)
            text_shadow.setColor(color)
            text_shadow.setOffset(0.0)
            self.windowFrame.setGraphicsEffect(text_shadow)
        else:
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.windowFrame.setGraphicsEffect(None)

    def on_application_state_changed(self, state):
        if self.windowState() == Qt.WindowNoState:
            self.style_window(state == Qt.ApplicationActive, True)
        elif self.windowState() == Qt.WindowFullScreen:
            self.style_window(state == Qt.ApplicationActive, False)

    def on_tool_button_max_clicked(self):
        self.toolButton_restore.setVisible(True)
        self.toolButton_max.setVisible(False)
        if self._is_full:
            self.toolButton_full.setVisible(True)
        self.showMaximized()
        self.style_window(True, False)
        self.update()

    def on_tool_button_restore_clicked(self):
        self.toolButton_restore.setVisible(False)
        self.toolButton_max.setVisible(True)
        self.toolButton_full.setVisible(False)
        self.setWindowState(Qt.WindowNoState)
        self.style_window(True, True)
        self.update()

    def on_tool_button_min_clicked(self):
        self.showMinimized()
        self.update()

    def on_tool_button_full_clicked(self):
        self.toolButton_restore.setVisible(False)
        self.toolButton_max.setVisible(False)
        self.toolButton_full.setVisible(False)
        self.toolButton_min.setVisible(False)
        self.toolButton_close.setVisible(False)
        self.toolButton_full_exit.setVisible(True)
        self._full_point = self.geometry().topLeft()
        self._full_size = self.geometry().size()
        desktop = QtWidgets.QApplication.desktop()
        self.move(0, 0)
        self.resize(desktop.width(), desktop.height())
        self.setWindowState(Qt.WindowFullScreen)
        self.update()

    def on_tool_button_full_exit_clicked(self):
        self.toolButton_restore.setVisible(True)
        self.toolButton_max.setVisible(False)
        self.toolButton_full.setVisible(True)
        self.toolButton_min.setVisible(True)
        self.toolButton_close.setVisible(True)
        self.toolButton_full_exit.setVisible(False)
        self.move(self._full_point)
        self.resize(self._full_size)
        self.setWindowState(Qt.WindowMaximized)
        self.update()

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QEvent.MouseMove:
            if self.isMaximized() or self.isFullScreen():
                return QWidget.eventFilter(self, obj, event)
            mouse = QtGui.QMouseEvent(event)
            if mouse is not None:
                self.check_border_dragging(mouse)
                if obj == self.windowTitlebar and self._mouse_pressed_title:
                    self.move(self._wnd_pos + (mouse.globalPos() - self._mouse_pos))
        elif event.type() == QEvent.MouseButtonPress and obj == self:
            mouse = QtGui.QMouseEvent(event)
            if mouse:
                self.mousePressEvent(mouse)
        elif event.type() == QEvent.MouseButtonPress and obj == self.windowTitlebar:
            mouse = QtGui.QMouseEvent(event)
            if mouse:
                self._mouse_pressed_title = True
                self._mouse_pos = mouse.globalPos()
                self._wnd_pos = self.pos()
        elif event.type() == QEvent.MouseButtonRelease and obj == self:
            if self._mouse_pressed:
                mouse = QtGui.QMouseEvent(event)
                if mouse:
                    self.mouseReleaseEvent(mouse)
        elif event.type() == QEvent.MouseButtonRelease and obj == self.windowTitlebar:
            self._mouse_pressed_title = False
        elif event.type() == QEvent.MouseButtonDblClick and obj == self.windowTitlebar:
            if self.windowState() == Qt.WindowNoState and self._is_max:
                self.on_tool_button_max_clicked()
            elif self.windowState() == Qt.WindowFullScreen:
                self.on_tool_button_full_exit_clicked()
            elif self.windowState() == Qt.WindowMaximized:
                self.on_tool_button_restore_clicked()

        return QWidget.eventFilter(self, obj, event)

    def left_border_hit(self, pos: QPoint) -> bool:
        rect = self.geometry()
        if pos.x() >= rect.x() and (pos.x() <= (rect.x() + self.CONST_DRAG_BORDER_SIZE)):
            return True
        return False

    def right_border_hit(self, pos: QPoint) -> bool:
        rect = self.geometry()
        tmp = rect.x() + rect.width()
        if pos.x() <= tmp and (pos.x() >= (tmp - self.CONST_DRAG_BORDER_SIZE)):
            return True
        return False

    def top_border_hit(self, pos: QPoint) -> bool:
        rect = self.geometry()
        if pos.y() >= rect.y() and (pos.y() <= (rect.y() + self.CONST_DRAG_BORDER_SIZE)):
            return True
        return False

    def bottom_border_hit(self, pos: QPoint) -> bool:
        rect = self.geometry()
        tmp = rect.y() + rect.height()
        if pos.y() <= tmp and (pos.y() >= (tmp - self.CONST_DRAG_BORDER_SIZE)):
            return True
        return False

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.isMaximized():
            return

        self._mouse_pressed = True
        self._start_geometry = self.geometry()
        global_mouse_pos = self.mapToGlobal(QPoint(event.x(), event.y()))
        if self.left_border_hit(global_mouse_pos) and self.top_border_hit(global_mouse_pos):
            self._drag_top = True
            self._drag_left = True
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.right_border_hit(global_mouse_pos) and self.top_border_hit(global_mouse_pos):
            self._drag_right = True
            self._drag_top = True
            self.setCursor(Qt.SizeBDiagCursor)
        elif self.left_border_hit(global_mouse_pos) and self.bottom_border_hit(global_mouse_pos):
            self._drag_left = True
            self._drag_bottom = True
            self.setCursor(Qt.SizeBDiagCursor)
        elif self.right_border_hit(global_mouse_pos) and self.bottom_border_hit(global_mouse_pos):
            self._drag_bottom = True
            self._drag_right = True
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            if self.top_border_hit(global_mouse_pos):
                self._drag_top = True
                self.setCursor(Qt.SizeVerCursor)
            elif self.left_border_hit(global_mouse_pos):
                self._drag_left = True
                self.setCursor(Qt.SizeHorCursor)
            elif self.right_border_hit(global_mouse_pos):
                self._drag_right = True
                self.setCursor(Qt.SizeHorCursor)
            elif self.bottom_border_hit(global_mouse_pos):
                self._drag_bottom = True
                self.setCursor(Qt.SizeVerCursor)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.isMaximized():
            return

        self._mouse_pressed = False
        switch_back_cursor_needed = self._drag_top or self._drag_left or self._drag_right or self._drag_bottom
        self._drag_right = False
        self._drag_bottom = False
        self._drag_left = False
        self._drag_top = False
        if switch_back_cursor_needed:
            self.setCursor(Qt.ArrowCursor)

    def check_border_dragging(self, event: QtGui.QMouseEvent):
        if self.isMaximized() or self.isFullScreen():
            return

        global_mouse_pos = event.globalPos()
        if self._mouse_pressed:
            if self._drag_top and self._drag_right:
                new_height = self._start_geometry.height() + self._start_geometry.y() - global_mouse_pos.y()
                new_width = global_mouse_pos.x() - self._start_geometry.x()
                if new_height > self.minimumHeight() and new_width > self.minimumWidth():
                    self.setGeometry(self._start_geometry.x(), global_mouse_pos.y(), new_width, new_height)
            elif self._drag_top and self._drag_left:
                new_height = self._start_geometry.height() + self._start_geometry.y() - global_mouse_pos.y()
                new_width = self._start_geometry.width() + self._start_geometry.x() - global_mouse_pos.x()
                if new_height > self.minimumHeight() and new_width > self.minimumWidth():
                    self.setGeometry(global_mouse_pos.x(), global_mouse_pos.y(), new_width, new_height)
            elif self._drag_top and self._drag_left:
                new_height = global_mouse_pos.y() - self._start_geometry.y()
                new_width = self._start_geometry.width() + self._start_geometry.x() - global_mouse_pos.x()
                if new_width > self.minimumHeight() and new_width > self.minimumWidth():
                    self.setGeometry(global_mouse_pos.x(), global_mouse_pos.y(), new_width, new_height)
            elif self._drag_bottom and self._drag_left:
                new_height = global_mouse_pos.y() - self._start_geometry.y()
                new_width = self._start_geometry.width() + self._start_geometry.x() - global_mouse_pos.x()
                if new_height > self.minimumHeight() and new_width > self.minimumWidth():
                    self.setGeometry(global_mouse_pos.x(), self._start_geometry.y(), new_width, new_height)
            elif self._drag_bottom and self._drag_right:
                new_height = global_mouse_pos.y() - self._start_geometry.y()
                new_width = global_mouse_pos.x() - self._start_geometry.x()
                if new_height > self.minimumHeight() and new_width > self.minimumWidth():
                    self.resize(new_width, new_height)
            elif self._drag_top:
                new_height = self._start_geometry.height() + self._start_geometry.y() - global_mouse_pos.y()
                if new_height > self.minimumHeight():
                    self.setGeometry(self._start_geometry.x(), global_mouse_pos.y(), self._start_geometry.width(), new_height)
            elif self._drag_left:
                new_width = self._start_geometry.width() + self._start_geometry.x() - global_mouse_pos.x()
                if new_width > self.minimumWidth():
                    self.setGeometry(global_mouse_pos.x(), self._start_geometry.y(), new_width, self._start_geometry.height())
            elif self._drag_right:
                new_width = global_mouse_pos.x() - self._start_geometry.x()
                if new_width > self.minimumWidth():
                    self.resize(new_width, self._start_geometry.height())
            elif self._drag_bottom:
                new_height = global_mouse_pos.y() - self._start_geometry.y()
                if new_height > self.minimumHeight():
                    self.resize(self._start_geometry.width(), new_height)
        else:
            if self.left_border_hit(global_mouse_pos) and self.top_border_hit(global_mouse_pos):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.right_border_hit(global_mouse_pos) and self.top_border_hit(global_mouse_pos):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.left_border_hit(global_mouse_pos) and self.bottom_border_hit(global_mouse_pos):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.right_border_hit(global_mouse_pos) and self.bottom_border_hit(global_mouse_pos):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                if self.top_border_hit(global_mouse_pos):
                    self.setCursor(Qt.SizeVerCursor)
                elif self.left_border_hit(global_mouse_pos):
                    self.setCursor(Qt.SizeHorCursor)
                elif self.right_border_hit(global_mouse_pos):
                    self.setCursor(Qt.SizeHorCursor)
                elif self.bottom_border_hit(global_mouse_pos):
                    self.setCursor(Qt.SizeVerCursor)
                else:
                    self._drag_top = False
                    self._drag_left = False
                    self._drag_right = False
                    self._drag_bottom = False
                    self.setCursor(Qt.ArrowCursor)
