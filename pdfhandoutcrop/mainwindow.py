import os
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog
from PyQt6.QtCore import pyqtSlot, Qt, QEvent, QUrl
from PyQt6.QtGui import QColorConstants, QPixmap, QPainter, QPainterPath, QIcon, QDesktopServices
import fitz
from pdfhandoutcrop.ui_mainwindow import Ui_MainWindow
from pdfhandoutcrop.setlayoutdialog import SetLayoutDialog
from pdfhandoutcrop import pdf


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, args):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.abspath(__file__)) + '/pdfhandoutcrop.png'))
        self.page_position = [[0, 0]] * self.spbPagesPerSheet.value()
        for i in range(self.spbPagesPerSheet.value()):
            self.comboPosition.addItem(self.tr("Page {0}").format(i + 1))
        self.scaling = 2.0
        self.current_page = 0
        # self.fileInput and self.fileOutput need to be defined first
        # because QFileDialog needs them
        self.fileInput = args.fileInput
        self.fileOutput = ""
        self.set = 0
        self.needPaint = False
        self.labelSelectPoint.installEventFilter(self)
        if self.fileInput:
            self.open(self.fileInput)

    @pyqtSlot()
    def on_action_Open_triggered(self):
        filename = QFileDialog.getOpenFileName(self, "", self.fileInput,
                                               self.tr("PDF documents (*.pdf)"))[0]
        if filename:
            self.fileInput = filename
            self.open(filename)

    def open(self, filename):
        try:
            self.document = fitz.open(filename)
        except (RuntimeError, ValueError) as e:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Cannot open input file: ") + str(e))
            self.labelSelectPoint.setText("")
            return
        self.btnAutoDetect.setEnabled(True)
        self.btnReload.setEnabled(True)
        self.setWindowTitle(self.tr("{0} - PdfHandoutCrop").format(os.path.basename(self.fileInput)))
        self.current_page = 0
        self.loadPdf()

    @pyqtSlot()
    def on_action_Save_triggered(self):
        filename = QFileDialog.getSaveFileName(self, "", self.fileOutput,
                                               self.tr("PDF documents (*.pdf)"))[0]
        if filename != "":
            self.fileOutput = filename
            pdf.save_pymupdf(self.fileInput, self.fileOutput,
                             [[x[0] / self.scaling, x[1] / self.scaling] for x in self.page_position],
                             self.spbWidth.value() / self.scaling, self.spbHeight.value() / self.scaling)
            QMessageBox.information(self, self.tr("Finished"), self.tr("Cropped PDF saved"))

    @pyqtSlot()
    def on_action_Website_triggered(self):
        QDesktopServices.openUrl(QUrl("https://cges30901.github.io/pdfhandoutcrop/"))

    @pyqtSlot()
    def on_action_Project_page_triggered(self):
        QDesktopServices.openUrl(QUrl("https://github.com/cges30901/pdfhandoutcrop"))

    @pyqtSlot()
    def on_action_Donate_triggered(self):
        QDesktopServices.openUrl(QUrl("https://cges30901.github.io/pdfhandoutcrop/donate.html"))

    @pyqtSlot()
    def on_action_Blog_triggered(self):
        QDesktopServices.openUrl(QUrl("https://hsiu-ming.blogspot.com/"))

    @pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        QMessageBox.aboutQt(self)

    @pyqtSlot()
    def on_action_About_triggered(self):
        version = "0.99.3"
        QMessageBox.about(self, self.tr("About"), self.tr(
            '''<h3>PdfHandoutCrop {0}</h3><br>
Author: Hsiu-Ming Chang<br>
e-mail: cges30901@gmail.com<br>
License: GPL v3''').format(version))

    @pyqtSlot(int)
    def on_spbPagesPerSheet_valueChanged(self, num):
        while num > len(self.page_position):
            self.comboPosition.addItem(self.tr("Page {0}").format(len(self.page_position) + 1))
            self.page_position.append([0, 0])
        while num < len(self.page_position):
            self.comboPosition.removeItem(len(self.page_position) - 1)
            self.page_position.pop()
        self.needPaint = True
        self.update()

    def loadPdf(self):
        self.labelSelectPoint.setText(self.tr("Loading..."))
        self.labelSelectPoint.repaint()
        if self.current_page == 0:
            self.btnPrevious.setEnabled(False)
        else:
            self.btnPrevious.setEnabled(True)
        if self.current_page == self.document.page_count - 1:
            self.btnNext.setEnabled(False)
        else:
            self.btnNext.setEnabled(True)
        try:
            self.image = pdf.renderPage(self.document, self.current_page, self.scaling)
        except ValueError as e:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Cannot render page: ") + str(e))
            self.labelSelectPoint.clear()
            return
        self.pixmap = QPixmap.fromImage(self.image)
        self.needPaint = True
        self.labelSelectPoint.setPixmap(self.pixmap)
        self.labelPageNum.setText(str(self.current_page + 1) + " / " + str(self.document.page_count))

    @pyqtSlot(bool)
    def on_btnAutoDetect_clicked(self):
        cropbox = pdf.autodetect(self.image)
        if cropbox is None:  # Page can not be found
            QMessageBox.warning(self, self.tr("Page can not be found"),
                                self.tr("Page can not be found. Auto detect only works if pages have border."))
            return

        dlgSetLayout = SetLayoutDialog(self)
        if cropbox.length != 1:
            dlgSetLayout.label.hide()
            dlgSetLayout.spbColumns.setValue(len(cropbox.columns))
            dlgSetLayout.spbRows.setValue(len(cropbox.rows))
            dlgSetLayout.spbColumns.setEnabled(False)
            dlgSetLayout.spbRows.setEnabled(False)
        if dlgSetLayout.exec() == QDialog.accepted:
            # ask columns and rows when only one page is detected (shared border)
            if cropbox.length == 1:
                numColumns = dlgSetLayout.spbColumns.value()
                numRows = dlgSetLayout.spbRows.value()
                cropbox.height /= numRows
                cropbox.width /= numColumns
                cropbox.length = numRows * numColumns
                for i in range(1, numColumns):
                    cropbox.columns.append(cropbox.columns[i - 1] + cropbox.width)
                for i in range(1, numRows):
                    cropbox.rows.append(cropbox.rows[i - 1] + cropbox.height)

        self.spbPagesPerSheet.setValue(cropbox.length)
        self.spbWidth.setValue(cropbox.width)
        self.spbHeight.setValue(cropbox.height)

        self.page_position = cropbox.toList(dlgSetLayout.comboOrder.currentIndex(), self.image.height())
        # update value of spbPositionX and spbPositionY
        self.spbPositionX.setValue(self.page_position[self.comboPosition.currentIndex()][0])
        self.spbPositionY.setValue(self.page_position[self.comboPosition.currentIndex()][1])
        self.needPaint = True
        self.update()
        self.statusBar.showMessage(self.tr("Found {0} pages").format(cropbox.length), 2000)

    @pyqtSlot(int)
    def on_comboPosition_currentIndexChanged(self, num):
        self.spbPositionX.setValue(self.page_position[num][0])
        self.spbPositionY.setValue(self.page_position[num][1])

    @pyqtSlot(int)
    def on_spbPositionX_valueChanged(self, num):
        self.page_position[self.comboPosition.currentIndex()][0] = num

    @pyqtSlot(int)
    def on_spbPositionY_valueChanged(self, num):
        self.page_position[self.comboPosition.currentIndex()][1] = num

    @pyqtSlot(bool)
    def on_btnPosition_clicked(self):
        self.set = 1
        self.statusBar.showMessage(self.tr(
            "Please click the upper left point of page {0}").format(self.comboPosition.currentIndex() + 1))

    @pyqtSlot(bool)
    def on_btnWidthHeight_clicked(self):
        self.set = 2
        self.statusBar.showMessage(self.tr("Please click the upper left point of any page"))

    def labelSelectPoint_mousePressed(self, x, y):
        if self.set == 1:
            # self.spbHeight.value() should be set first for y coordinate
            if self.spbHeight.value() == 0:
                QMessageBox.warning(self, self.tr("Warning"), self.tr("Height should be set first"))

            # set x coordinate
            self.spbPositionX.setValue(x)

            # point (0,0) is in lowerLeft, so y coordinate need to be changed
            sheetHeight = self.image.height()
            pageHeight = self.spbHeight.value()
            self.spbPositionY.setValue(sheetHeight - pageHeight - y)
            self.needPaint = True
            self.set = 0
            self.statusBar.clearMessage()
        elif self.set == 2:
            # set Width and Height - step one
            # store coordinate of upper left point
            self.upperleftX = x
            self.upperleftY = y
            # set lower right point if pressed again
            self.set = 3
            self.statusBar.showMessage(self.tr("Please click the lower right point of the page you clicked"))
        elif self.set == 3:
            # set Width and Height - step two
            # get coordinate of lower right point (x,y)
            # and calculate width and height
            self.spbWidth.setValue(x - self.upperleftX)
            self.spbHeight.setValue(y - self.upperleftY)
            self.needPaint = True
            self.set = 0
            self.statusBar.clearMessage()
        self.update()

    def paintEvent(self, e):
        if self.needPaint:
            pixmap_draw = QPixmap(self.pixmap)
            painter = QPainter()
            painter.begin(pixmap_draw)
            painter.setPen(QColorConstants.Red)
            path = [QPainterPath()] * self.spbPagesPerSheet.value()
            for i in range(self.spbPagesPerSheet.value()):
                sheetHeight = self.image.height()
                pageHeight = self.spbHeight.value()
                path[i].moveTo(self.page_position[i][0],
                               sheetHeight - pageHeight - self.page_position[i][1])
                path[i].lineTo(self.page_position[i][0] + self.spbWidth.value(),
                               sheetHeight - pageHeight - self.page_position[i][1])
                path[i].lineTo(self.page_position[i][0] + self.spbWidth.value(),
                               sheetHeight - pageHeight - self.page_position[i][1] + self.spbHeight.value())
                path[i].lineTo(self.page_position[i][0],
                               sheetHeight - pageHeight - self.page_position[i][1] + self.spbHeight.value())
                path[i].lineTo(self.page_position[i][0],
                               sheetHeight - pageHeight - self.page_position[i][1])
                painter.drawPath(path[i])
            painter.end()
            self.labelSelectPoint.setPixmap(pixmap_draw)
            self.needPaint = False

    @pyqtSlot(bool)
    def on_btnReload_clicked(self):
        self.needPaint = True
        self.update()

    @pyqtSlot(bool)
    def on_btnPrevious_clicked(self):
        self.current_page -= 1
        self.loadPdf()
        self.needPaint = True
        self.update()

    @pyqtSlot(bool)
    def on_btnNext_clicked(self):
        self.current_page += 1
        self.loadPdf()
        self.needPaint = True
        self.update()

    def on_btnZoomIn_clicked(self):
        self.scaling *= 1.2
        self.needPaint = True
        self.loadPdf()

    def on_btnZoomOut_clicked(self):
        self.scaling /= 1.2
        self.needPaint = True
        self.loadPdf()

    def eventFilter(self, watched, event):
        if watched == self.labelSelectPoint and event.type() == QEvent.Type.MouseButtonPress:
            self.labelSelectPoint_mousePressed(int(event.position().x()), int(event.position().y()))
        return False
