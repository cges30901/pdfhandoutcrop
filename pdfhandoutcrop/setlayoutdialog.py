from pdfhandoutcrop.ui_setlayoutdialog import Ui_SetLayoutDialog
from PyQt5.QtWidgets import QDialog

class SetLayoutDialog(QDialog, Ui_SetLayoutDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.comboOrder.addItem(self.tr("left to right, then down"))
        self.comboOrder.addItem(self.tr("right to left, then down"))
        self.comboOrder.addItem(self.tr("top to bottom, then right"))
        self.comboOrder.addItem(self.tr("top to bottom, then left"))

    def on_pushButton_clicked(self):
        self.accept()
