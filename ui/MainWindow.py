import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QFileDialog, QStatusBar, \
    QMessageBox

from ui.ImageWindow import ImageWindow
from ui.RightWindow import RightWindow
from ui.dialog import FileDialog, StructElementDialog
from ui.dialog.FilterDialog import FilterDialog
from ui.popupWindow import MorePopup
from util import QSSHelper, Actions
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

    menubar: QWidget
    statusbar: QStatusBar
    right_window: QWidget
    image_window: QWidget
    file_dialog: QFileDialog
    more_popup: QWidget

    __ls_click_sig = QtCore.pyqtSignal(int, int)
    __resize_sig = QtCore.pyqtSignal(int, int)
    saved = True

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
        self.menubar = MenuBar(self)

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
        self.__resize_sig.connect(self.menubar.on_window_resize)
        self.__resize_sig.connect(self.more_popup.on_window_resize)
        self.__resize_sig.connect(self.right_window.on_window_resize)
        self.__resize_sig.connect(self.image_window.on_window_resize)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.__ls_click_sig.emit(ev.x(), ev.y())

    def resizeEvent(self, ev: QtGui.QResizeEvent) -> None:
        self.__resize_sig.emit(ev.size().width(), ev.size().height())

    def update_open_image(self, open_image_url: str):
        self.__open_image_url = open_image_url
        self.set_window_title()
        self.saved = True

    def closeEvent(self, ev: QtGui.QCloseEvent) -> None:
        if not self.saved:
            confirm = QMessageBox.question(self, "是否退出", "当前所做的修改将会丢失", QMessageBox.Yes | QMessageBox.Cancel)
            if confirm == QMessageBox.Yes:
                ev.accept()
            else:
                print(confirm)
                ev.ignore()

    def imageEditEvent(self):
        self.saved = False

    def imageSaveEvent(self):
        self.saved = True

    def openFilterEvent(self, action: int):
        filter_dialog = FilterDialog(self, action)
        if filter_dialog.exec_() == 1:
            print("modify image")
        else:
            print("canceled")

    def openSeDialogEvent(self, action: int):
        se_dialog = StructElementDialog(self, action)
        if se_dialog.exec_() == 1:
            print("click ok se")
        else:
            print("canceled")

    def on_se_dialog_ok(self, action: int, grid_mat: np.ndarray, origin: tuple):
        print(action, grid_mat, origin)
        self.image_window.on_image_edit(action, {"se": grid_mat, "origin": origin})

    def on_filter_dialog_ok(self, action: int, kernel: str, sigma: str = ""):
        print(action, kernel, sigma)
        ks: int = int(kernel) if kernel != "" else 0
        sig: float = float(sigma) if sigma != "" else 0.0
        self.image_window.on_image_edit(action, {"ks": ks, "sigma": sig})
