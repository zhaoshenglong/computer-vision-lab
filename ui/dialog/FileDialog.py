import os

from PyQt5.QtWidgets import QFileDialog


class FileDialog(QFileDialog):
    FileDialogTitle = "选择图片"

    def __init__(self, parent):
        super(QFileDialog, self).__init__(parent)
        self.fileSelected.connect(self.parent().update_open_image)
        self.fileSelected.connect(self.parent().image_window.on_image_open)

    def open_image(self):
        image, image_t = QFileDialog.getOpenFileName(self.parent(), self.FileDialogTitle, os.getcwd(),
                                                     "Image Files(*.jpg *.jpeg *.png)")
        if image != "":
            self.fileSelected.emit(image)

    def save_image(self):
        image, select_folder = QFileDialog.getSaveFileName(self.parent(), self.FileDialogTitle, os.getcwd(),
                                                           "Images (*.png *.bmp *.jpg  *.gif *.jpeg)",
                                                           options=QFileDialog.ShowDirsOnly
                                                           | QFileDialog.DontResolveSymlinks
                                                           )
        if image != "":
            print(image, select_folder)
