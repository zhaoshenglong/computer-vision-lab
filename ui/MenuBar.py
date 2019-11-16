from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QSizePolicy


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
    __undo_icon_disable_url = "./resource/undo_icon_disable.png"
    __redo_icon_url = "./resource/redo_icon.png"
    __redo_icon_disable_url = "./resource/redo_icon_disable.png"
    __cut_icon_url = "./resource/cut_icon.png"
    __rotate_icon_url = "./resource/rotate_icon.png"
    __more_icon_url = "./resource/more_icon.png"
    __edit_icon_url = "./resource/edit_icon.png"
    image_btn: MenuButton
    save_btn: MenuButton
    magnifier_btn: MenuButton
    undo_btn: MenuButton
    redo_btn: MenuButton
    cut_btn: MenuButton
    rotate_btn: MenuButton
    edit_btn: MenuButton
    more_btn: MenuButton

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.draw_menubar()

    def draw_menubar(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedWidth(self.parent().width())
        self.setFixedHeight(self.menubar_height)
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
        self.image_btn = MenuButton(QIcon(self.__image_icon_url), " 打开图片", self)
        layout.addWidget(self.image_btn)
        self.image_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_btn.setShortcut("Ctrl+O")
        self.image_btn.clicked.connect(self.parent().file_dialog.open_image)
        self.image_btn.setStyleSheet("QPushButton{\
                                    background-color: rgb(0,120,215); \
                                    color: #fff; \
                                    width: 130px; \
                                } \
                                QPushButton:hover{\
                                background-color: rgb(66,156,227)}")
        self.save_btn = MenuButton(QIcon(self.__save_icon_url), " 保存", self)
        layout.addWidget(self.save_btn)
        self.save_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.save_btn.setShortcut("Ctrl+S")
        self.save_btn.clicked.connect(self.parent().image_window.save_image)
        self.save_btn.clicked.connect(self.parent().imageSaveEvent)
        self.save_btn.setStyleSheet("QPushButton{ \
                                    width: 96px; \
                                }")

    def draw_middle_layout(self, layout):
        layout.setSpacing(0)
        self.magnifier_btn = MenuButton(self)
        self.magnifier_btn.setIcon(QIcon(self.__magnifier_plus_url))
        self.magnifier_btn.setIconSize(QSize(30, 30))
        self.magnifier_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.magnifier_btn)
        self.undo_btn = MenuButton(self)
        self.undo_btn.setIcon(QIcon(self.__undo_icon_disable_url))
        self.undo_btn.setStyleSheet("QPushButton:hover{background-color: #fff}")
        self.undo_btn.setShortcut("Ctrl+Z")
        layout.addWidget(self.undo_btn)
        self.undo_btn.clicked.connect(self.parent().image_window.on_undo)

        self.redo_btn = MenuButton(self)
        self.redo_btn.setIcon(QIcon(self.__redo_icon_disable_url))
        self.redo_btn.setShortcut("Ctrl+Y")
        self.redo_btn.setStyleSheet("QPushButton:hover{background-color: #fff}")
        self.redo_btn.clicked.connect(self.parent().image_window.on_redo)
        layout.addWidget(self.redo_btn)
        self.cut_btn = MenuButton(self)
        self.cut_btn.setIcon(QIcon(self.__cut_icon_url))
        layout.addWidget(self.cut_btn)
        rotate_btn = MenuButton(self)
        rotate_btn.setIcon(QIcon(self.__rotate_icon_url))
        layout.addWidget(rotate_btn)

    def draw_right_layout(self, layout):
        layout.setSpacing(0)
        self.edit_btn = MenuButton(self)
        self.edit_btn.setIcon(QIcon(self.__edit_icon_url))
        self.edit_btn.setText(" 编辑")
        self.edit_btn.setStyleSheet("QPushButton{  \
                                            width: 90px\
                                        }")
        self.edit_btn.clicked.connect(self.parent().right_window.toggle)
        self.edit_btn.clicked.connect(self.parent().more_popup.on_menubar_clicked)
        self.edit_btn.clicked.connect(self.parent().image_window.on_right_window_toggle)
        layout.addWidget(self.edit_btn)
        self.more_btn = MenuButton(self)
        self.more_btn.setIcon(QIcon(self.__more_icon_url))
        self.more_btn.clicked.connect(self.parent().more_popup.toggle)
        layout.addWidget(self.more_btn)

    def on_window_resize(self, width, height):
        self.setFixedWidth(width)
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

    def toggle_redo_btn(self ):
        disable = self.parent().image_window.history_ctrl.redo_disable()
        if disable:
            self.redo_btn.setIcon(QIcon(self.__redo_icon_disable_url))
            self.redo_btn.setStyleSheet("QPushButton:hover{background-color: #fff}")
        else:
            self.redo_btn.setIcon(QIcon(self.__redo_icon_url))
            self.redo_btn.setStyleSheet("QPushButton:hover{background-color: #e6e6e6;}")

    def toggle_undo_btn(self):
        disable = self.parent().image_window.history_ctrl.undo_disable()
        if not disable:
            self.undo_btn.setIcon(QIcon(self.__undo_icon_url))
            self.undo_btn.setStyleSheet("QPushButton:hover{background-color: #e6e6e6;}")
        else:
            self.undo_btn.setIcon(QIcon(self.__undo_icon_disable_url))
            self.undo_btn.setStyleSheet("QPushButton:hover{background-color: #fff}")
