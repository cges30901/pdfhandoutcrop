import fitz
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QImage


class Cropbox:
    def __init__(self, width, height, columns, rows):
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.length = len(rows) * len(columns)

    def toList(self, sequence, sheetHeight):
        # point (0,0) is in lowerLeft, so coordinate need to be changed
        pageHeight = self.height
        li = []
        if sequence == 0:
            for i in range(self.length):
                li.append([self.columns[i % len(self.columns)],
                           sheetHeight - pageHeight - self.rows[i // len(self.columns)]])
        elif sequence == 1:
            for i in range(self.length):
                li.append([self.columns[len(self.columns) - 1 - i % len(self.columns)],
                           sheetHeight - pageHeight - self.rows[i // len(self.columns)]])
        elif sequence == 2:
            for i in range(self.length):
                li.append([self.columns[i // len(self.rows)],
                           sheetHeight - pageHeight - self.rows[i % len(self.rows)]])
        elif sequence == 3:
            for i in range(self.length):
                li.append([self.columns[len(self.columns) - 1 - i // len(self.rows)],
                           sheetHeight - pageHeight - self.rows[i % len(self.rows)]])
        return li


def renderPage(document, pageNum, scaling=2.0):
    page = document.load_page(pageNum)
    pix = page.get_pixmap(matrix=fitz.Matrix(scaling, 0, 0, scaling, 0, 0))
    samples = pix.samples
    image = QImage(samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
    return image


def autodetect(image):
    # find the upperleft point of the first page
    pointUpperLeft = findFirstPoint(image)
    if pointUpperLeft.x() == -1:  # Page can not be found
        return

    # find width
    width = 100
    while pointUpperLeft.x() + width < image.width():
        if image.pixel(pointUpperLeft.x() + width, pointUpperLeft.y()) == 4294967295:
            break
        width += 1

    # find height
    height = 100
    while pointUpperLeft.y() + height < image.height():
        if image.pixel(pointUpperLeft.x(), pointUpperLeft.y() + height) == 4294967295:
            break
        height += 1

    # find columns
    columns = [pointUpperLeft.x()]
    iter = pointUpperLeft.x() + width
    while iter < image.width() - 100:
        if image.pixel(iter, pointUpperLeft.y()) != 4294967295:
            columns.append(iter)
            iter += width
        iter += 1

    # find rows
    rows = [pointUpperLeft.y()]
    iter = pointUpperLeft.y() + height
    while iter < image.height() - 100:
        if image.pixel(pointUpperLeft.x(), iter) != 4294967295:
            rows.append(iter)
            iter += height
        iter += 1
    cropbox = Cropbox(width, height, columns, rows)
    return cropbox


def findFirstPoint(image):
    for yOffset in range(image.height() - 100):
        for xOffset in range(image.width() - 100):
            pixel = image.pixel(xOffset, yOffset)
            # 4294967295 is white
            if pixel != 4294967295:
                for length in range(1, 101):
                    if (image.pixel(xOffset + length, yOffset) == 4294967295
                            or image.pixel(xOffset, yOffset + length) == 4294967295):
                        # not a page
                        break
                    if length == 100:
                        # page found
                        return QPoint(xOffset, yOffset)
    # cannot find a page
    return QPoint(-1, -1)


def save_pymupdf(fileInput, fileOutput, cropboxList, width, height):
    document = fitz.open(fileInput)
    pdfOutput = fitz.open()
    numPages = document.page_count
    page0 = document.load_page(0)
    pagesPerSheet = len(cropboxList)
    rotation = page0.rotation
    if rotation == 90 or rotation == 270:  # MediaBox is [0,0,height,width]
        sheetHeight = page0.mediabox[2]
    else:  # MediaBox is [0,0,height,width]
        sheetHeight = page0.mediabox[3]

    for i in range(numPages):
        for j in range(pagesPerSheet):
            if rotation == 90 or rotation == 270:
                page = pdfOutput.new_page(-1, height, width)
            else:  # rotation is 0 or 180
                page = pdfOutput.new_page(-1, width, height)

            page.set_rotation(rotation)
            page.show_pdf_page(page.rect, document, i, clip=fitz.Rect(
                cropboxList[j][0],
                sheetHeight - cropboxList[j][1] - height,
                cropboxList[j][0] + width,
                sheetHeight - cropboxList[j][1]))

    pdfOutput.save(fileOutput, 3)
    pdfOutput.close()
