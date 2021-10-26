import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
import fitz
from pdfhandoutcrop.mainwindow import MainWindow
from pdfhandoutcrop import pdf


def commandline(args):
    try:
        document = fitz.open(args.fileInput)
    except (RuntimeError, ValueError) as e:
        print("Cannot open input file:", e)
        return 1
    scaling = 2.0
    image = pdf.renderPage(document, 0)
    cropbox = pdf.autodetect(image)
    if cropbox is None:  # Page can not be found
        print("Page can not be found. Auto detect only works if pages have border.")
        return 2
    pdf.save_pymupdf(args.fileInput, args.output,
                     [[x[0] / scaling, x[1] / scaling] for x in cropbox.toList(0, image.height())],
                     cropbox.width / scaling, cropbox.height / scaling)
    return 0


def main():
    parser = argparse.ArgumentParser(description='A tool to crop pdf handout with multiple pages per sheet.')
    parser.add_argument("fileInput", metavar='FILE', nargs='?', default="", help='input file')
    parser.add_argument("-o", "--output", default="", help='auto detect and save to OUTPUT file without showing GUI')
    args = parser.parse_args()

    if args.output:
        return commandline(args)
    else:
        app = QApplication(sys.argv)

        translator = QTranslator()
        translator.load(QLocale(), "pdfhandoutcrop", "_",
                        os.path.dirname(os.path.abspath(__file__)) + "/language")
        app.installTranslator(translator)

        # load Qt translation
        qtTranslator = QTranslator()
        qtTranslator.load(QLocale(), "qt", "_",
                          QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        app.installTranslator(qtTranslator)
        w = MainWindow(args)
        w.showMaximized()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
