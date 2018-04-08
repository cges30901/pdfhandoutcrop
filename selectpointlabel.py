from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal

class SelectPointLabel(QLabel):
    mousePressed=pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__()
    
    def mousePressEvent(self, e):
        self.mousePressed.emit(e.pos().x(), e.pos().y())
