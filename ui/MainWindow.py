from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QLabel, QMenuBar, QMenu, QAction, QHBoxLayout

from resource import Constant
from util import QSSHelper
from .MenuBar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):
        self.resize(1280, 1000 - 40)
        self.setWindowTitle(Constant.app)
        self.setWindowIcon(QIcon("./resource/icon.png"))
        self.set_window_center()
        self.setMenuBar(MenuBar())
        self.set_stylesheet()

    def set_window_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width() >> 1),
                  (screen.height() - size.height() - 40 - 50) >> 1)

    def set_stylesheet(self):
        self.setStyleSheet(QSSHelper.read_qss("./qss/index.qss"))
