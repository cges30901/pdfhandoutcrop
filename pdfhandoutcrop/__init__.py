import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale
from pdfhandoutcrop.mainwindow import MainWindow

def main():
    
    app = QApplication(sys.argv)

    translator=QTranslator()
    translator.load(QLocale(), "pdfhandoutcrop", "_",
        os.path.dirname(os.path.abspath(__file__))+"/language")
    app.installTranslator(translator)

    w = MainWindow()
    w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
