from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QHBoxLayout, QWidget, QFileDialog, QVBoxLayout, QStatusBar, \
    QSizePolicy, QLabel, QPushButton, QLayout

from EditHistoryCtrl import HistoryCtrl
from ui.ImageWindow import ImageWindow
from ui.RightWindow import RightWindow
from ui.dialog import FileDialog
from ui.popupWindow import MorePopup
from util import QSSHelper
from .MenuBar import MenuBar


class MainWindow(QMainWindow):
    __width = 1280
    __height = 960
    __min_width = 625
    __min_height = 625 - 40
    __icon_url = "./resource/icon.png"
    __qss_url = "./qss/index.qss"
    __open_image_url = ""
    __window_title = "PhotoShark"

    __menubar: QWidget
    __statusbar: QStatusBar
    right_window: QWidget
    image_window: QWidget
    file_dialog: QFileDialog
    more_popup: QWidget

    __ls_click_sig = QtCore.pyqtSignal(int, int)
    __resize_sig = QtCore.pyqtSignal(int, int)
    __image_change_sig = QtCore.pyqtSignal(str)

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

        self.right_window = RightWindow(self)
        self.image_window = ImageWindow(self)
        self.file_dialog = FileDialog(self)
        self.more_popup = MorePopup(self)
        self.__menubar = MenuBar(self)

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
        if self.__open_image_url == "":
            self.setWindowTitle(self.__window_title)
        else:
            self.setWindowTitle("%s - %s" % (self.__window_title,
                                             self.__open_image_url[self.__open_image_url.rfind("/")+1:]))

    def init_signal_connection(self):
        self.__ls_click_sig.connect(self.more_popup.on_window_clicked)
        self.__resize_sig.connect(self.__menubar.on_window_resize)
        self.__resize_sig.connect(self.more_popup.on_window_resize)
        self.__resize_sig.connect(self.right_window.on_window_resize)
        self.__resize_sig.connect(self.image_window.on_window_resize)
        self.__image_change_sig.connect(self.image_window.on_image_change)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.__ls_click_sig.emit(ev.x(), ev.y())

    def resizeEvent(self, ev: QtGui.QResizeEvent) -> None:
        self.__resize_sig.emit(ev.size().width(), ev.size().height())

    def update_open_image(self, open_image_url: str):
        self.__open_image_url = open_image_url
        self.set_window_title()
