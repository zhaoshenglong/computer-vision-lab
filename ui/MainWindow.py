from PyQt5 import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QLabel, QMenuBar, QMenu, QAction, QHBoxLayout, \
    QWidget, QPushButton
from resource import Constant
from util import QSSHelper
from .MenuBar import MenuBar


class MainWindow(QMainWindow):
    __menubar = None
    __statusbar = None
    __width = 1280
    __height = 960
    __icon_url = "./resource/icon.png"
    __qss_url = "./qss/index.qss"
    __open_image = ""
    __window_title = "PhotoShark"

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):
        self.resize(self.__width, self.__height)
        self.setWindowTitle("%s - %s" % (self.__window_title, self.__open_image))
        self.setWindowIcon(QIcon(self.__icon_url))
        self.set_window_center()
        self.set_stylesheet()
        self.draw_menubar()

    def set_window_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - self.__width >> 1),
                  # hard code [-50], represents height of status bar on windows system
                  (screen.height() - self.__height - 40 - 50) >> 1)

    def set_stylesheet(self):
        self.setStyleSheet(QSSHelper.read_qss(self.__qss_url))

    def draw_menubar(self):
        menubar = MenuBar(self)
        self.__menubar = menubar
