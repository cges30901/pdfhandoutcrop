import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from pdfhandoutcrop.mainwindow import MainWindow

def main():
    
    app = QApplication(sys.argv)

    translator=QTranslator()
    translator.load(QLocale(), "pdfhandoutcrop", "_",
        os.path.dirname(os.path.abspath(__file__))+"/language")
    app.installTranslator(translator)

    #load Qt translation
    qtTranslator=QTranslator()
    qtTranslator.load(QLocale(), "qt", "_",
        QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    w = MainWindow()
    w.showMaximized()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
