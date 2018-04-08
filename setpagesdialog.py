from ui_setpagesdialog import Ui_SetPagesDialog
from PyQt5.QtWidgets import QDialog

class SetPagesDialog(QDialog, Ui_SetPagesDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
    
    def on_pushButton_clicked(self):
        self.accept()
