from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QSizePolicy
from ui.RightWindow import RightWindow
from .dialog import FileDialog
from .popupWindow import MorePopup



class MenuButton(QPushButton):
    def init_menubutton(self):
        pass


class MenuBar(QWidget):
    menubar_height = 60  # Fixed height
    min_optimal_width = 800
    __image_icon_url = "./resource/image_icon.png"
    __save_icon_url = "./resource/save_icon.png"
    __magnifier_plus_url = "./resource/magnifier_plus_icon.png"
    __undo_icon_url = "./resource/undo_icon.png"
    __redo_icon_url = "./resource/redo_icon.png"
    __cut_icon_url = "./resource/cut_icon.png"
    __rotate_icon_url = "./resource/rotate_icon.png"
    __more_icon_url = "./resource/more_icon.png"
    __edit_icon_url = "./resource/edit_icon.png"
    file_dialog = None
    more_popup = None
    image_btn = None
    save_btn = None
    magnifier_btn = None
    undo_btn = None
    redo_btn = None
    cut_btn = None
    rotate_btn = None

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.file_dialog = FileDialog(self.parent())
        self.more_popup = MorePopup(self.parent())
        self.draw_menubar()

    def draw_menubar(self):
        self.setGeometry(0, 0, self.parent().width(), self.menubar_height)  # Fixed origin
        layout = QHBoxLayout()
        left_layout = QHBoxLayout()
        middle_layout = QHBoxLayout()
        right_layout = QHBoxLayout()

        self.draw_left_layout(left_layout)

        self.draw_middle_layout(middle_layout)
        self.draw_right_layout(right_layout)
        layout.addLayout(left_layout)
        layout.addStretch(1)
        layout.addLayout(middle_layout)
        layout.addStretch(1)
        layout.addLayout(right_layout)
        self.setLayout(layout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def draw_left_layout(self, layout):
        layout.setSpacing(0)
        image_btn = MenuButton(QIcon(self.__image_icon_url), " 打开图片", self)
        layout.addWidget(image_btn)
        image_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        image_btn.setShortcut("Ctrl+O")
        image_btn.clicked.connect(self.file_dialog.open_image)
        image_btn.setStyleSheet("QPushButton{\
                                    background-color: rgb(0,120,215); \
                                    color: #fff; \
                                    width: 130px; \
                                } \
                                QPushButton:hover{\
                                background-color: rgb(66,156,227)}")
        save_btn = MenuButton(QIcon(self.__save_icon_url), " 保存", self)
        layout.addWidget(save_btn)
        save_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        save_btn.setShortcut("Ctrl+S")
        save_btn.clicked.connect(self.file_dialog.save_image)
        save_btn.setStyleSheet("QPushButton{ \
                                    width: 96px; \
                                }")

    def draw_middle_layout(self, layout):
        layout.setSpacing(0)
        magnifier_btn = MenuButton(self)
        magnifier_btn.setIcon(QIcon(self.__magnifier_plus_url))
        magnifier_btn.setIconSize(QSize(30, 30))
        magnifier_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(magnifier_btn)
        undo_btn = MenuButton(self)
        undo_btn.setIcon(QIcon(self.__undo_icon_url))
        layout.addWidget(undo_btn)
        redo_btn = MenuButton(self)
        redo_btn.setIcon(QIcon(self.__redo_icon_url))
        layout.addWidget(redo_btn)
        cut_btn = MenuButton(self)
        cut_btn.setIcon(QIcon(self.__cut_icon_url))
        layout.addWidget(cut_btn)
        rotate_btn = MenuButton(self)
        rotate_btn.setIcon(QIcon(self.__rotate_icon_url))
        layout.addWidget(rotate_btn)

    def draw_right_layout(self, layout):
        layout.setSpacing(0)
        edit_btn = MenuButton(self)
        edit_btn.setIcon(QIcon(self.__edit_icon_url))
        edit_btn.setText(" 编辑")
        edit_btn.setStyleSheet("QPushButton{  \
                                            width: 90px\
                                        }")
        edit_btn.clicked.connect(self.parent().right_window.toggle)
        layout.addWidget(edit_btn)

        more_btn = MenuButton(self)
        more_btn.setIcon(QIcon(self.__more_icon_url))
        more_btn.clicked.connect(self.more_popup.toggle)
        layout.addWidget(more_btn)

    def on_window_resize(self, width, height):
        self.setGeometry(0, 0, width, self.menubar_height)
        if width < self.min_optimal_width:
            self.children()[0].setText("")
            self.children()[0].setStyleSheet("QPushButton{\
                                    background-color: rgb(0,120,215); \
                                    color: #fff; \
                                    width: 85px; \
                                } \
                                QPushButton:hover{\
                                background-color: rgb(66,156,227)}")
            self.children()[1].setText("")
            self.children()[1].setStyleSheet("QPushButton{  \
                                    width: 85px\
                                }")
            self.children()[7].setText("")
            self.children()[7].setStyleSheet("QPushButton{  \
                                                width: 85px\
                                            }")
        else:
            self.children()[0].setText(" 打开图片")
            self.children()[0].setStyleSheet("QPushButton{\
                                    background-color: rgb(0,120,215); \
                                    color: #fff; \
                                    width: 130px; \
                                } \
                                QPushButton:hover{\
                                background-color: rgb(66,156,227)}")
            self.children()[1].setText(" 保存")
            self.children()[1].setStyleSheet("QPushButton{  \
                                                width: 96px\
                                            }")
            self.children()[7].setText(" 编辑")
            self.children()[7].setStyleSheet("QPushButton{  \
                                                            width: 96px\
                                                        }")
