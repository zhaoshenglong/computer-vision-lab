from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QPainter, QMouseEvent, QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QLabel, QMenuBar, QMenu, QAction, QHBoxLayout, \
    QWidget, QPushButton

from ui.ImageWindow import ImageWindow
from ui.RightWindow import RightWindow
from util import QSSHelper
from .MenuBar import MenuBar


class MainWindow(QMainWindow):
    __menubar = None
    __statusbar = None
    __width = 1280
    __height = 960
    __min_width = 625
    __min_height = 625 - 40
    __icon_url = "./resource/icon.png"
    __qss_url = "./qss/index.qss"
    __open_image = ""
    __window_title = "PhotoShark"
    __ls_click_sig = QtCore.pyqtSignal(int, int)
    __resize_sig = QtCore.pyqtSignal(int, int)
    right_window = None
    image_window = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):
        self.resize(self.__width, self.__height)
        self.setWindowIcon(QIcon(self.__icon_url))
        self.set_window_title()
        self.set_window_center()
        self.set_stylesheet()
        self.setMinimumWidth(self.__min_width)
        self.setMinimumHeight(self.__min_height)
        self.setFont(QFont("Microsoft YaHei UI"))
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.right_window = RightWindow(self)
        self.image_window = ImageWindow(self)
        self.__menubar = MenuBar(self)
        layout.addWidget(self.image_window)
        layout.addWidget(self.right_window)
        self.setLayout(layout)

        # Connect signal and slot
        self.init_signal_connection()

    def set_window_center(self):
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.__width >> 1),
                  # hard code [-50], represents height of status bar on windows system
                  (screen.height() - self.__height - 40 - 50) >> 1)

    def set_stylesheet(self):
        self.setStyleSheet(QSSHelper.read_qss(self.__qss_url))

    def set_window_title(self):
        if self.__open_image == "":
            self.setWindowTitle(self.__window_title)
        else:
            self.setWindowTitle("%s - %s" % (self.__window_title, self.__open_image))

    def init_signal_connection(self):
        self.__ls_click_sig.connect(self.__menubar.more_popup.on_window_clicked)
        self.__resize_sig.connect(self.__menubar.on_window_resize)
        self.__resize_sig.connect(self.__menubar.more_popup.on_window_resize)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.__ls_click_sig.emit(ev.x(), ev.y())

    def resizeEvent(self, ev: QtGui.QResizeEvent) -> None:
        self.__resize_sig.emit(ev.size().width(), ev.size().height())
