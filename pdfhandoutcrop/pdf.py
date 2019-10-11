import copy
import os
import fitz
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage

class Cropbox():
    def __init__(self, width=0, height=0, columns=[], rows=[]):
        self.width=width
        self.height=height
        self.columns=columns
        self.rows=rows
        self.length=len(rows)*len(columns)

def renderPage(document, pageNum):
    scaling=2.0
    page = document.loadPage(pageNum)
    pix = page.getPixmap(fitz.Matrix(scaling, 0, 0, scaling, 0, 0), alpha = False)
    samples = pix.samples
    image=QImage(samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888);
    return image

def autodetect(image):
    #find the upperleft point of the first page
    pointUpperLeft=findFirstPoint(image)
    if pointUpperLeft.x()==-1:  #Page can not be found
        return

    #find width
    width=100
    while pointUpperLeft.x()+width<image.width():
        if image.pixel(pointUpperLeft.x()+width, pointUpperLeft.y())==4294967295:
            break
        width+=1

    #find height
    height=100
    while pointUpperLeft.y()+height<image.height():
        if image.pixel(pointUpperLeft.x(), pointUpperLeft.y()+height)==4294967295:
            break
        height+=1

    #find columns
    columns=[pointUpperLeft.x()]
    iter=pointUpperLeft.x()+width
    while iter<image.width()-100:
        if image.pixel(iter, pointUpperLeft.y())!=4294967295:
            columns.append(iter)
            iter+=width
        iter+=1

    #find rows
    rows=[pointUpperLeft.y()]
    iter=pointUpperLeft.y()+height
    while iter<image.height()-100:
        if image.pixel(pointUpperLeft.x(), iter)!=4294967295:
            rows.append(iter)
            iter+=height
        iter+=1
    cropbox=Cropbox(width, height, columns, rows)
    return cropbox

def findFirstPoint(image):
    for yOffset in range(image.height()-100):
        for xOffset in range(image.width()-100):
            pixel=image.pixel(xOffset, yOffset)
            #4294967295 is white
            if pixel!=4294967295:
                for length in range(1, 101):
                    if (image.pixel(xOffset+length, yOffset)==4294967295
                        or image.pixel(xOffset, yOffset+length)==4294967295):
                        #not a page
                        break
                    if length==100:
                        #page found
                        return QPoint(xOffset, yOffset)
    #cannot find a page
    return QPoint(-1, -1)

def save_pypdf2(fileInput, fileOutput, cropboxList, width, height):
    scaling=2.0
    pdfInput=PdfFileReader(fileInput)
    pdfOutput=PdfFileWriter()
    numPages=pdfInput.getNumPages()
    #Getting mediaBox of page 0 directly makes output pages of first sheet
    #have same mediaBox, so I use copy.copy() to workaround this problem.
    page0=copy.copy(pdfInput.getPage(0))
    pagesPerSheet=len(cropboxList)
    width=width/scaling
    height=height/scaling

    rotation=page0.get('/Rotate')
    #make rotation 0, 90, 180 or 270
    if rotation is None:
        rotation=0
    elif rotation<0:
        rotation=rotation%360+360
    #operation above might change rotation to 360,
    #so "if" is used instead of "elif"
    if rotation>=360:
        rotation=rotation%360

    if rotation==90 or rotation==270: #mediaBox is [0,0,height,width]
        sheetWidth=page0.mediaBox[3].as_numeric()
        sheetHeight=page0.mediaBox[2].as_numeric()
    else: #mediaBox is [0,0,width,height]
        sheetWidth=page0.mediaBox[2]
        sheetHeight=page0.mediaBox[3]

    #if lowerLeft of original mediaBox is not [0,0],
    #new mediaBox should be adjusted according to that.
    #FIXME: only fixed when page is not rotated currently.
    mediaBox_old=page0.mediaBox
    lowerLeftX_old=mediaBox_old.lowerLeft[0].as_numeric()
    lowerLeftY_old=mediaBox_old.lowerLeft[1].as_numeric()

    for i in range(numPages):
        page=pdfInput.getPage(i)
        for j in range(pagesPerSheet):
            page_crop=copy.copy(page)
            if rotation==90:
                page_crop.mediaBox.lowerLeft=(sheetHeight-cropboxList[j][1]/scaling-height,
                    cropboxList[j][0]/scaling+width)
                page_crop.mediaBox.upperRight=(sheetHeight-cropboxList[j][1]/scaling,
                    cropboxList[j][0]/scaling)
            elif rotation==180:
                page_crop.mediaBox.lowerLeft=(sheetWidth-cropboxList[j][0]/scaling-width,
                    sheetHeight-cropboxList[j][1]/scaling)
                page_crop.mediaBox.upperRight=(sheetWidth-cropboxList[j][0]/scaling,
                    sheetHeight-cropboxList[j][1]/scaling-height)
            elif rotation==270:
                page_crop.mediaBox.lowerLeft=(cropboxList[j][1]/scaling,
                    sheetWidth-cropboxList[j][0]/scaling)
                page_crop.mediaBox.upperRight=(cropboxList[j][1]/scaling+height,
                    sheetWidth-cropboxList[j][0]/scaling-width)
            else: #not rotated
                page_crop.mediaBox.lowerLeft=(cropboxList[j][0]/scaling+lowerLeftX_old,
                    cropboxList[j][1]/scaling+height+lowerLeftY_old)
                page_crop.mediaBox.upperRight=(cropboxList[j][0]/scaling+width+lowerLeftX_old,
                    cropboxList[j][1]/scaling+lowerLeftY_old)
            pdfOutput.addPage(page_crop)
    outputStream = open(fileOutput, "wb")
    pdfOutput.write(outputStream)
    outputStream.close()

def save_pymupdf(fileInput, fileOutput, cropboxList, width, height):
    scaling=2.0
    document=fitz.open(fileInput)
    pdfOutput=fitz.open()
    numPages=document.pageCount
    page0=document.loadPage(0)
    pagesPerSheet=len(cropboxList)
    width=width/scaling
    height=height/scaling
    rotation=page0.rotation
    if rotation==90 or rotation==270: #MediaBox is [0,0,height,width]
        sheetWidth=page0.MediaBox[3]
        sheetHeight=page0.MediaBox[2]
    else : #MediaBox is [0,0,height,width]
        sheetWidth=page0.MediaBox[2]
        sheetHeight=page0.MediaBox[3]

    #if lowerLeft of original mediaBox is not [0,0],
    #new mediaBox should be adjusted according to that.
    #FIXME: only fixed when page is not rotated currently.
    mat = page0._getTransformation()
    shift=mat.e

    for i in range(numPages):
        for j in range(pagesPerSheet):
            # original cropbox not considered yet
            pdfOutput.insertPDF(document, i, i)
            insertedPage = i * pagesPerSheet + j
            page_crop = pdfOutput.loadPage(insertedPage)
            if rotation==90:
                page_crop.setCropBox(fitz.Rect(
                    sheetHeight-cropboxList[j][1]/scaling-height,
                    sheetWidth-cropboxList[j][0]/scaling-width,
                    sheetHeight-cropboxList[j][1]/scaling,
                    sheetWidth-cropboxList[j][0]/scaling))
            elif rotation==180:
                page_crop.setCropBox(fitz.Rect(
                    sheetWidth-cropboxList[j][0]/scaling-width,
                    cropboxList[j][1]/scaling,
                    sheetWidth-cropboxList[j][0]/scaling,
                    cropboxList[j][1]/scaling+height))
            elif rotation==270:
                page_crop.setCropBox(fitz.Rect(
                    cropboxList[j][1]/scaling,
                    cropboxList[j][0]/scaling,
                    cropboxList[j][1]/scaling+height,
                    cropboxList[j][0]/scaling+width))
            else: #not rotated
                page_crop.setCropBox(fitz.Rect(
                    cropboxList[j][0]/scaling-shift,
                    sheetHeight-cropboxList[j][1]/scaling-height,
                    cropboxList[j][0]/scaling+width-shift,
                    sheetHeight-cropboxList[j][1]/scaling))
    pdfOutput.save(fileOutput, 4)
    pdfOutput.close()

# fileInput="2pages.pdf"
# document=fitz.open(fileInput)
# image=loadPage(document)
# cropbox=autodetect(image)
# save_pypdf2(fileInput,"out2.pdf",cropbox)
# save_pymupdf(fileInput,"outm.pdf",cropbox)
