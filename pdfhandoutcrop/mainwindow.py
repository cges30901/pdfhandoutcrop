import copy
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, QEvent
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QIcon
import popplerqt5
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfhandoutcrop.ui_mainwindow import Ui_MainWindow
from pdfhandoutcrop.setpagesdialog import SetPagesDialog

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('pdfhandoutcrop.png'))
        self.spbPage=[[self.spbPage1X, self.spbPage1Y],
            [self.spbPage2X, self.spbPage2Y],
            [self.spbPage3X, self.spbPage3Y],
            [self.spbPage4X, self.spbPage4Y],
            [self.spbPage5X, self.spbPage5Y],
            [self.spbPage6X, self.spbPage6Y]]
        self.density_render=150.0
        self.current_page=0
        #self.fileInput and self.fileOutput need to be defined first
        #because QFileDialog needs them
        self.fileInput=""
        self.fileOutput=""
        self.set=0
        self.needPaint=False
        self.labelSelectPoint.installEventFilter(self)

    @pyqtSlot()
    def on_action_Open_triggered(self):
        filename=QFileDialog.getOpenFileName(self, "", self.fileInput,
            self.tr("PDF documents (*.pdf)"))[0]
        if filename!="":
            self.fileInput=filename
            self.btnAutoDetect.setEnabled(True)
            self.btnUpdate.setEnabled(True)
            self.setWindowTitle(self.tr("{0} - PdfHandoutCrop").format(self.fileInput))
            self.loadPdf()

    @pyqtSlot()
    def on_action_Convert_triggered(self):
        filename=QFileDialog.getSaveFileName(self, "", self.fileOutput,
            self.tr("PDF documents (*.pdf)"))[0]
        if filename!="":
            self.fileOutput=filename
            self.convert()

    @pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        QMessageBox.aboutQt(self)

    @pyqtSlot()
    def on_action_About_triggered(self):
        QMessageBox.about(self, self.tr("About"), self.tr('''
        <h3>PdfHandoutCrop</h3><br>
        Author: Hsiu-Ming Chang<br>
        e-mail: cges30901@gmail.com<br>
        License: GPL v3'''))

    def loadPdf(self):
        self.labelSelectPoint.setText(self.tr("Loading..."))
        self.labelSelectPoint.repaint()
        self.document=popplerqt5.Poppler.Document.load(self.fileInput)
        if self.document is None:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot open input file"))
            self.labelSelectPoint.setText("")
            return
        if self.current_page==0:
            self.btnPrevious.setEnabled(False)
        else:
            self.btnPrevious.setEnabled(True)
        if self.current_page==self.document.numPages()-1:
            self.btnNext.setEnabled(False)
        else:
            self.btnNext.setEnabled(True)
        self.pdfPage = self.document.page(self.current_page)
        self.image=self.pdfPage.renderToImage(self.density_render, self.density_render)
        self.pixmap=QPixmap.fromImage(self.image)
        self.needPaint=True
        self.labelSelectPoint.setPixmap(self.pixmap)
        self.labelPageNum.setText(str(self.current_page+1)+" / "+str(self.document.numPages()))

    def convert(self):
        pdfInput=PdfFileReader(self.fileInput)
        pdfOutput=PdfFileWriter()
        numPages=pdfInput.getNumPages()
        pagesPerSheet=self.spbPagesPerSheet.value()
        factor=72/self.density_render
        width=self.spbWidth.value()*factor
        height=self.spbHeight.value()*factor
        for i in range(numPages):
            page=pdfInput.getPage(i)
            for j in range(pagesPerSheet):
                page_crop=copy.copy(page)
                page_crop.mediaBox.lowerLeft=(self.spbPage[j][0].value()*factor,
                    self.spbPage[j][1].value()*factor+height)
                page_crop.mediaBox.upperRight=(self.spbPage[j][0].value()*factor+width,
                    self.spbPage[j][1].value()*factor)
                pdfOutput.addPage(page_crop)
        outputStream = open(self.fileOutput, "wb")
        pdfOutput.write(outputStream)
        outputStream.close()
        QMessageBox.information(self, "Finish", "Convert finished")

    @pyqtSlot(bool)
    def on_btnAutoDetect_clicked(self):
        #find the upperleft point of the first page
        pointUpperLeft=self.findFirstPoint()
        if pointUpperLeft.x()==-1:  #cannot find a page
            QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot find a page"))
            return

        #find width
        width=0
        while pointUpperLeft.x()+width<self.image.width():
            if self.image.pixel(pointUpperLeft.x()+width, pointUpperLeft.y())==4294967295:
                break
            width+=1

        #find height
        height=0
        while pointUpperLeft.y()+height<self.image.height():
            if self.image.pixel(pointUpperLeft.x(), pointUpperLeft.y()+height)==4294967295:
                break
            height+=1

        #find columns
        columns=[pointUpperLeft.x()]
        iter=pointUpperLeft.x()+width
        while iter<self.image.width():
            if self.image.pixel(iter, pointUpperLeft.y())!=4294967295:
                columns.append(iter)
                iter+=width
            iter+=1

        #find rows
        rows=[pointUpperLeft.y()]
        iter=pointUpperLeft.y()+height
        while iter<self.image.height():
            if self.image.pixel(pointUpperLeft.x(), iter)!=4294967295:
                rows.append(iter)
                iter+=height
            iter+=1

        #ask when only one page is detected (shared border)
        if len(columns)==1 and len(rows)==1:
            dlgSetPages=SetPagesDialog(self)
            if dlgSetPages.exec_()==QDialog.Accepted:
                numColumns=dlgSetPages.spbColumns.value()
                numRows=dlgSetPages.spbRows.value()
                height/=numRows
                width/=numColumns
                for i in range(1, numColumns):
                    columns.append(columns[i-1]+width)
                for i in range(1, numRows):
                    rows.append(rows[i-1]+height)

        self.spbPagesPerSheet.setValue(len(rows)*len(columns))
        self.spbWidth.setValue(width)
        self.spbHeight.setValue(height)
        #point (0,0) is in lowerLeft, so coordinate need to be changed
        sheetHeight=self.pdfPage.pageSizeF().height()*self.density_render/72
        pageHeight=self.spbHeight.value()
        for i in range(len(rows)*len(columns)):
            self.spbPage[i][0].setValue(columns[i%len(columns)])
            self.spbPage[i][1].setValue(sheetHeight-pageHeight-rows[i//len(columns)])
        self.needPaint=True
        self.update()
        self.statusBar.showMessage(self.tr("Found {0} pages").format(len(rows)*len(columns)), 2000)

    def findFirstPoint(self):
        for yOffset in range(self.image.height()):
            for xOffset in range(self.image.width()):
                pixel=self.image.pixel(xOffset, yOffset)
                #4294967295 is white
                if pixel!=4294967295:
                    for length in range(1, 101):
                        if (self.image.pixel(xOffset+length, yOffset)==4294967295
                            or self.image.pixel(xOffset, yOffset+length)==4294967295):
                            #not a page
                            break
                        if length==100:
                            #page found
                            return QPoint(xOffset, yOffset)
        #cannot find a page
        return QPoint(-1, -1)

    @pyqtSlot(bool)
    def on_btnPageOne_clicked(self):
        self.set=1
        self.statusBar.showMessage(self.tr("Please click the upper left point of the first page"))

    @pyqtSlot(bool)
    def on_btnPageTwo_clicked(self):
        self.set=2
        self.statusBar.showMessage(self.tr("Please click the upper left point of the second page"))

    @pyqtSlot(bool)
    def on_btnPageThree_clicked(self):
        self.set=3
        self.statusBar.showMessage(self.tr("Please click the upper left point of the third page"))

    @pyqtSlot(bool)
    def on_btnPageFour_clicked(self):
        self.set=4
        self.statusBar.showMessage(self.tr("Please click the upper left point of the fourth page"))

    @pyqtSlot(bool)
    def on_btnPageFive_clicked(self):
        self.set=5
        self.statusBar.showMessage(self.tr("Please click the upper left point of the fifth page"))

    @pyqtSlot(bool)
    def on_btnPageSix_clicked(self):
        self.set=6
        self.statusBar.showMessage(self.tr("Please click the upper left point of the sixth page"))

    @pyqtSlot(bool)
    def on_btnWidthHeight_clicked(self):
        self.set=7
        self.statusBar.showMessage(self.tr("Please click the upper left point of any page"))

    def labelSelectPoint_mousePressed(self, x, y):
        if self.set>=1 and self.set <=6:
            #store coordinate in spbPage[self.set-1]
            self.spbPage[self.set-1][0].setValue(x)

            #point (0,0) is in lowerLeft, so coordinate need to be changed
            sheetHeight=self.pdfPage.pageSizeF().height()*self.density_render/72
            pageHeight=self.spbHeight.value()
            self.spbPage[self.set-1][1].setValue(sheetHeight-pageHeight-y)
            self.needPaint=True
            self.set=0
            self.statusBar.clearMessage()
        elif self.set==7:
            #set Width and Height - step one
            #store coordinate of upper left point
            self.upperleftX=x
            self.upperleftY=y
            #set lower right point if pressed again
            self.set=8
            self.statusBar.showMessage(self.tr("Please click the lower right point of the page you clicked"))
        elif self.set==8:
            #set Width and Height - step two
            #get coordinate of lower right point (x,y)
            #and calculate width and height
            self.spbWidth.setValue(x-self.upperleftX)
            self.spbHeight.setValue(y-self.upperleftY)
            self.needPaint=True
            self.set=0
            self.statusBar.clearMessage()
        self.update()

    def paintEvent(self, e):
        if self.needPaint:
            pixmap_draw=QPixmap(self.pixmap)
            painter=QPainter()
            painter.begin(pixmap_draw)
            painter.setPen(Qt.red)
            path=[QPainterPath() for i in range(self.spbPagesPerSheet.value())]
            for i in range(self.spbPagesPerSheet.value()):
                sheetHeight=self.pdfPage.pageSizeF().height()*self.density_render/72
                pageHeight=self.spbHeight.value()
                path[i].moveTo(self.spbPage[i][0].value(),
                    sheetHeight-pageHeight-self.spbPage[i][1].value())
                path[i].lineTo(self.spbPage[i][0].value()+self.spbWidth.value(),
                    sheetHeight-pageHeight-self.spbPage[i][1].value())
                path[i].lineTo(self.spbPage[i][0].value()+self.spbWidth.value(),
                    sheetHeight-pageHeight-self.spbPage[i][1].value()+self.spbHeight.value())
                path[i].lineTo(self.spbPage[i][0].value(),
                    sheetHeight-pageHeight-self.spbPage[i][1].value()+self.spbHeight.value())
                path[i].lineTo(self.spbPage[i][0].value(),
                    sheetHeight-pageHeight-self.spbPage[i][1].value())
                painter.drawPath(path[i])
            painter.end()
            self.labelSelectPoint.setPixmap(pixmap_draw)
            self.needPaint=False

    @pyqtSlot(bool)
    def on_btnUpdate_clicked(self):
        self.needPaint=True
        self.update()

    @pyqtSlot(bool)
    def on_btnPrevious_clicked(self):
        self.current_page-=1
        self.loadPdf()
        self.needPaint=True
        self.update()

    @pyqtSlot(bool)
    def on_btnNext_clicked(self):
        self.current_page+=1
        self.loadPdf()
        self.needPaint=True
        self.update()

    def on_btnZoomIn_clicked(self):
        self.density_render*=1.2
        self.needPaint=True
        self.loadPdf()

    def on_btnZoomOut_clicked(self):
        self.density_render/=1.2
        self.needPaint=True
        self.loadPdf()

    def eventFilter(self, watched, event):
        if watched==self.labelSelectPoint and event.type()==QEvent.MouseButtonPress:
            self.labelSelectPoint_mousePressed(event.x(), event.y())
        return False
