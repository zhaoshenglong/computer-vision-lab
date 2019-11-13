import os

from PyQt5.QtWidgets import QFileDialog


class FileDialog(QFileDialog):
    FileDialogTitle = "选择图片"

    def __init__(self, parent):
        super(QFileDialog, self).__init__(parent)

    def open_image(self):
        image, image_t = QFileDialog.getOpenFileName(self.parent(), self.FileDialogTitle, os.getcwd(),
                                                     "Image Files(*.jpg *.jpeg *.png)")
        if image != "":
            print(image, image_t)
            return image
        else:
            print("You haven't choose a picture")

    def save_image(self):
        print("You are saving image")
