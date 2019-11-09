from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMenu, QAction, QMenuBar
from resource import Constant
from util import QSSHelper


class MenuBar(QMenuBar):
    def __init__(self):
        super(MenuBar, self).__init__()
        self.init_menu_bar()

    def init_menu_bar(self):
        for i in Constant.menu:
            item: QMenu = self.addMenu(i.text)
            for ac in i.actions:
                action = QAction(ac.text, self)
                action.setShortcut(ac.shortcut)
                item.addAction(action)
            item.triggered[QAction].connect(lambda a: print(a.text()))
