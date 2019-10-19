import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
import fitz
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfhandoutcrop.mainwindow import MainWindow
from pdfhandoutcrop import pdf

def commandline(args):
    document=fitz.open(args.fileInput)
    image=pdf.renderPage(document, 0)
    cropbox=pdf.autodetect(image)
    pdf.save_pypdf2(args.fileInput, args.output, cropbox.toList(0, image.height()), cropbox.width, cropbox.height)

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
    parser.add_argument("-a", "--auto", action='store_true', help='auto detect')
    args=parser.parse_args()

    if args.auto:
        commandline(args)
        return
    else:
        w = MainWindow(args)
        w.showMaximized()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
