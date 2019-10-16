import sys
import os
import argparse
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

    parser = argparse.ArgumentParser(description='A tool to crop pdf handout with multiple pages per sheet.')
    parser.add_argument("fileInput", metavar='FILE', nargs='?', default="", help='input file')
    parser.add_argument("-o", "--output", default="", help='output file')

    w = MainWindow(parser.parse_args())
    w.showMaximized()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
