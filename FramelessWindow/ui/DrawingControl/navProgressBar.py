import sys
import enum

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import pyqtProperty, Qt, QPoint, QRect, QSize


class NavStyle(enum.Enum):
    # 京东订单流程样式
    NavStyle_JD = 0
    # 淘宝订单流程样式
    NavStyle_TB = 1
    # 支付宝订单流程样式
    NavStyle_ZFB = 2


class NavProgressBar(QtWidgets.QWidget):
    """ 流程导航自定义控件 """

    def __init__(self, parent=None):
        super(NavProgressBar, self).__init__(parent)
        # 导航顶部标签数据
        self._top_info = ['step1', 'step2', 'step3', 'step4', 'step5']
        # 导航底部标签数据
        self._bottom_info = ['2020-05-09 20:00:00', '2020-05-09 21:00:00']
        # 最大步数
        self._max_step = 5
        # 当前第几步
        self._current_step = 1
        # 导航样式
        self._nav_style = NavStyle.NavStyle_JD
        # 背景色
        self._background = QColor(100, 100, 100)
        # 前景色
        self._foreground = QColor(255, 255, 255)
        # 当前背景色
        self._current_background = QColor(100, 184, 255)
        # 当前前景色
        self._current_foreground = QColor(255, 255, 255)
        # 图形字体
        # self._icon_font = QFont()

    # 获取属性, 注意要传入属性的类型
    @pyqtProperty(int)
    def max_step(self):
        return self._max_step

    # Python设置属性的装饰器
    @max_step.setter
    def max_step(self, max_step: int):
        """ 设置最大步数 """
        if self._max_step != max_step and max_step <= len(self._top_info):
            self._max_step = max_step
            self.update()

    @pyqtProperty(int)
    def current_step(self):
        return self._current_step

    @current_step.setter
    def current_step(self, current_step: int):
        """ 设置当前第几步 """
        if self._current_step != current_step and 0 < current_step < self._max_step:
            self._current_step = current_step
            self.update()

    @pyqtProperty(NavStyle)
    def nav_style(self):
        return self._nav_style

    @nav_style.setter
    def nav_style(self, nav_style: NavStyle):
        """ 设置导航样式 """
        if self._nav_style != nav_style:
            self._nav_style = nav_style
            self.update()

    @pyqtProperty(QColor)
    def background(self):
        return self._background

    @background.setter
    def background(self, background: QColor):
        """ 设置背景色"""
        if self._background != background:
            self._background = background
            self.update()

    @pyqtProperty(QColor)
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, foreground: QColor):
        """ 设置前景色 """
        if self._foreground!= foreground:
            self._foreground= foreground
            self.update()

    @pyqtProperty(QColor)
    def current_background(self):
        return self._current_background

    @current_background.setter
    def current_background(self, current_background: QColor):
        """ 设置当前背景色 """
        if self._current_background != current_background:
            self._current_background = current_background
            self.update()

    @pyqtProperty(QColor)
    def current_foreground(self):
        return self._current_foreground

    @current_foreground.setter
    def current_foreground(self, current_foreground: QColor):
        """ 设置当前前景色 """
        if self._current_foreground != current_foreground:
            self._current_foreground = current_foreground
            self.update()

    @classmethod
    def size_hint(self):
        return QSize(500, 80)

    @classmethod
    def minimum_size_hint(self):
        return QSize(50, 20)

    def get_top_info(self):
        return self._top_info

    def get_bottom_info(self):
        return self._bottom_info

    def set_top_info(self, top_info: list):
        """ 设置导航顶部标签数据 """
        if self._top_info != top_info:
            self._top_info = top_info
            self.update()

    def set_bottom_info(self, bottom_info: list):
        """ 设置导航底部标签数据 """
        if self._bottom_info != bottom_info:
            self._bottom_info = bottom_info
            self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # 绘制准备工作, 启用反锯齿
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        if self._nav_style == NavStyle.NavStyle_JD:
            self.draw_bg_jd(painter)
            self.draw_text_jd(painter)
            self.draw_current_bg_jd(painter)
            self.draw_current_text_jd(painter)
        elif self._nav_style == NavStyle.NavStyle_TB:
            self.draw_bg_tb(painter)
            self.draw_text_tb(painter)
            self.draw_current_bg_tb(painter)
            self.draw_current_text_tb(painter)
        elif self._nav_style == NavStyle.NavStyle_ZFB:
            self.draw_bg_zfb(painter)
            self.draw_text_zfb(painter)
            self.draw_current_bg_zfb(painter)
            self.draw_current_text_zfb(painter)

    def draw_bg_jd(self, painter: QPainter):
        painter.save()
        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width = self.width() / self._max_step
        height = self.height() / 2
        radius = height / 2
        init_x = width / 2
        init_y = height / 2 + radius / 5

        # 逐个绘制连接线条
        pen = QPen()
        pen.setWidthF(radius / 4.0)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self._background)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        for i in range(self._max_step - 1):
            painter.drawLine(QPoint(init_x, init_y), QPoint(init_x + width, init_y))
            init_x += width

        # 逐个绘制圆
        init_x = width / 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background)
        for i in range(self._max_step):
            painter.drawEllipse(QPoint(init_x, init_y), radius, radius)
            init_x += width

        # 逐个绘制圆中的数字
        init_x = width / 2
        font = QFont()
        font.setPixelSize(radius)
        painter.setFont(font)
        painter.setPen(self._foreground)
        painter.setBrush(Qt.NoBrush)
        for i in range(self._max_step):
            text_rect = QRect(init_x - radius, init_y - radius, radius * 2, radius * 2)
            painter.drawText(text_rect, Qt.AlignCenter, str(i+1))
            init_x += width

        painter.restore()

    def draw_text_jd(self, painter: QPainter):
        width = self.width() / self._max_step
        height = self.height() / 2
        init_x = 0
        init_y = height

        painter.save()
        font = QFont()
        font.setPixelSize(height / 3)
        painter.setFont(font)
        painter.setPen(self._background)
        painter.setBrush(Qt.NoBrush)
        for i in range(self._max_step):
            text_rect = QRect(init_x, init_y, width, height)
            painter.drawText(text_rect, Qt.AlignCenter, self._top_info[i])
            init_x += width
        painter.restore()

    def draw_current_bg_jd(self, painter: QPainter):
        painter.save()
        # 圆半径为高度一定比例,计算宽度,将宽度等分
        width = self.width() / self._max_step
        height = self.height() / 2
        radius = height / 2
        init_x = width / 2
        init_y = height / 2 + radius / 5
        radius -= radius / 5

        # 逐个绘制连接线条
        pen = QPen()
        pen.setWidthF(radius / 7.0)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self._current_background)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        for i in range(self._current_step - 1):
            painter.drawLine(QPoint(init_x, init_y), QPoint(init_x + width, init_y))
            init_x += width
        # 如果当前进度超过一个步数且小于最大步数则增加半个线条
        if 0 < self._current_step < self._max_step:
            painter.drawLine(QPoint(init_x, init_y), QPoint(init_x + width / 2, init_y));

        # 逐个绘制圆
        init_x = width / 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._current_background)
        for i in range(self._current_step):
            painter.drawEllipse(QPoint(init_x, init_y), radius, radius)
            init_x += width

        # 逐个绘制圆中的数字
        init_x = width / 2
        font = QFont()
        font.setPixelSize(radius)
        painter.setFont(font)
        painter.setPen(self._current_foreground)
        painter.setBrush(Qt.NoBrush)
        for i in range(self._current_step):
            text_rect = QRect(init_x - radius, init_y - radius, radius * 2, radius * 2)
            painter.drawText(text_rect, Qt.AlignCenter, str(i+1))
            init_x += width

        painter.restore()

    def draw_current_text_jd(self, painter: QPainter):
        width = self.width() / self._max_step
        height = self.height() / 2
        init_x = 0
        init_y = height

        painter.save()
        font = QFont()
        font.setPixelSize(height / 3)
        painter.setFont(font)
        painter.setPen(self._current_background)
        painter.setBrush(Qt.NoBrush)
        for i in range(self._current_step):
            text_rect = QRect(init_x, init_y, width, height)
            painter.drawText(text_rect, Qt.AlignCenter, self._top_info[i])
            init_x += width

        painter.restore()

    def draw_bg_tb(self, painter: QPainter):
        pass

    def draw_text_tb(self, painter: QPainter):
        pass

    def draw_current_bg_tb(self, painter: QPainter):
        pass

    def draw_current_text_tb(self, painter: QPainter):
        pass

    def draw_bg_zfb(self, painter: QPainter):
        pass

    def draw_text_zfb(self, painter: QPainter):
        pass

    def draw_current_bg_zfb(self, painter: QPainter):
        pass

    def draw_current_text_zfb(self, painter: QPainter):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = QtWidgets.QWidget()
    top_info = ['创建订单', '审核订单', '生产', '配送', '签收']
    nav_progress = NavProgressBar()
    nav_progress.set_top_info(top_info)
    nav_progress.max_step = len(top_info)
    nav_progress.current_step = 4
    nav_progress.current_background = QColor(24, 189, 155)
    h_layout = QtWidgets.QHBoxLayout()
    h_layout.addWidget(nav_progress)
    ui.setLayout(h_layout)
    ui.resize(500, 100)
    ui.show()
    sys.exit(app.exec_())
