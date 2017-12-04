#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <vector>
#include <QMessageBox>
#include <poppler/qt5/poppler-qt5.h>
#include <podofo/podofo.h>
#include <QFileDialog>
#include <QPdfWriter>
#include "setpagesdialog.h"

#define IMAGE_DENSITY 300

using namespace PoDoFo;
using namespace std;

void crop_page( PdfPage* pPage, const PdfRect & rCropBox )
{
    PdfVariant var;
    rCropBox.ToVariant( var );
    pPage->GetObject()->GetDictionary().AddKey( PdfName("MediaBox"), var );
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    set=0;
    current_page=0;
    spbPage[1][0]=ui->spbPage1X;
    spbPage[1][1]=ui->spbPage1Y;
    spbPage[2][0]=ui->spbPage2X;
    spbPage[2][1]=ui->spbPage2Y;
    spbPage[3][0]=ui->spbPage3X;
    spbPage[3][1]=ui->spbPage3Y;
    spbPage[4][0]=ui->spbPage4X;
    spbPage[4][1]=ui->spbPage4Y;
    spbPage[5][0]=ui->spbPage5X;
    spbPage[5][1]=ui->spbPage5Y;
    spbPage[6][0]=ui->spbPage6X;
    spbPage[6][1]=ui->spbPage6Y;
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_btnWidthHeight_clicked()
{
    set=7;
}

void MainWindow::on_lneInput_returnPressed()
{
    loadPdf();
}

void MainWindow::loadPdf()
{
    ui->labelSelectPoint->setText(tr("Loading..."));
    ui->labelSelectPoint->repaint();
    Poppler::Document* document=Poppler::Document::load(ui->lneInput->text());
    if (!document || document->isLocked()) {
        QMessageBox::warning(this,tr("warning"),tr("can not open input file"));
        ui->labelSelectPoint->setText(tr(""));
        delete document;
        return;
    }
    if(current_page==0){
        ui->btnPrevious->setEnabled(false);
    }
    else{
        ui->btnPrevious->setEnabled(true);
    }
    if(current_page==document->numPages()-1){
        ui->btnNext->setEnabled(false);
    }
    else{
        ui->btnNext->setEnabled(true);
    }
    Poppler::Page* pdfPage = document->page(current_page);
    image=pdfPage->renderToImage(IMAGE_DENSITY,IMAGE_DENSITY);
    pixmap=QPixmap::fromImage(image);
    ui->labelSelectPoint->setPixmap(pixmap);
    delete pdfPage;
    delete document;
}

void MainWindow::on_btnPageOne_clicked()
{
    set=1;
}

void MainWindow::on_btnPageTwo_clicked()
{
    set=2;
}

void MainWindow::on_btnPageThree_clicked()
{
    set=3;
}

void MainWindow::on_btnPageFour_clicked()
{
    set=4;
}

void MainWindow::on_btnPageFive_clicked()
{
    set=5;
}

void MainWindow::on_btnPageSix_clicked()
{
    set=6;
}

void MainWindow::on_labelSelectPoint_mousePressed(int x, int y)
{
    if(set>=1 and set <=6){
        spbPage[set][0]->setValue(x);
        spbPage[set][1]->setValue(y);
        set=0;
    }
    else if(set==7){//set Width and Height - step one
        upperleftX=x;
        upperleftY=y;
        set=8;
    }
    else if(set==8){//set Width and Height - step two
        ui->spbWidth->setValue(x-upperleftX);
        ui->spbHeight->setValue(y-upperleftY);
        set=0;
    }
    drawPixmap();
}

void MainWindow::on_btnConvert_clicked()
{
#ifndef CONVERT_PODOFO
    Poppler::Document* document=Poppler::Document::load(ui->lneInput->text());
    int pages=document->numPages();

    double width=ui->spbWidth->value();
    double height=ui->spbHeight->value();

    QPdfWriter pdfWriter(ui->lneOutput->text());
    pdfWriter.setPageSize(QPageSize(QPageSize::A4));
    pdfWriter.setPageOrientation(QPageLayout::Landscape); //width>height in slide
    pdfWriter.setPageMargins(QMarginsF(0,0,0,0)); //remove margin
    int dpi=max(width*2/11.69,height*2/8.27); //make image fit page
    dpi+=1; //prevent round down
    pdfWriter.setResolution(dpi);
    QPainter painter(&pdfWriter);

    int xOffset[ui->spbPagesPerSheet->value()];
    int yOffset[ui->spbPagesPerSheet->value()];
    for(int i=0;i<ui->spbPagesPerSheet->value();i++){
        xOffset[i]=spbPage[i+1][0]->value();
        yOffset[i]=spbPage[i+1][1]->value();
    }

    QImage cropped;
    for(int i=0;i<pages;i++){
        Poppler::Page* pdfPage = document->page(i);
        QImage image=pdfPage->renderToImage(IMAGE_DENSITY*2,IMAGE_DENSITY*2);
        for(int j=0;j<ui->spbPagesPerSheet->value();j++){
            cropped=image.copy(xOffset[j]*2,yOffset[j]*2,width*2,height*2);
            painter.drawImage(0,0, cropped);
            pdfWriter.newPage();
        }
    }
    delete document;
#else
    PdfError::EnableDebug( true );
    PdfError::EnableLogging(false);
    PdfMemDocument pdfInput;
    if(ui->lneInput->text().isEmpty()){
        QMessageBox::warning(this,tr("warning"),tr("Please set input file"));
        return;
    }
    if(ui->lneOutput->text().isEmpty()){
        QMessageBox::warning(this,tr("warning"),tr("Please set output file"));
        return;
    }
    pdfInput.Load(ui->lneInput->text().toLocal8Bit().constData());
    int pagesPerSheet=ui->spbPagesPerSheet->value();
    PdfMemDocument pdfOutput;
    int xOffset[pagesPerSheet];
    int yOffset[pagesPerSheet];
    for(int i=0;i<pagesPerSheet;i++){
        xOffset[i]=spbPage[i+1][0]->value();
        yOffset[i]=spbPage[i+1][1]->value();
    }
    double width=ui->spbWidth->value()*72/IMAGE_DENSITY;
    double height=ui->spbHeight->value()*72/IMAGE_DENSITY;
    PdfRect cropbox[pagesPerSheet];

    //detect rotation
    PdfPage* pageRotation=pdfInput.GetPage(0);
    int rotation=pageRotation->GetRotation();

    for(int i=0;i<pagesPerSheet;i++){

        //if page is rotated, change offset and size
        switch (rotation) {
        case 0:
            cropbox[i]=PdfRect((double)xOffset[i]*72/IMAGE_DENSITY,
                                    pdfInput.GetPage(0)->GetPageSize().GetHeight()-(double)yOffset[i]*72/IMAGE_DENSITY-height,
                                    width,height);
            break;
        case 90:
            cropbox[i]=PdfRect((double)yOffset[i]*72/IMAGE_DENSITY,
                                    (double)xOffset[i]*72/IMAGE_DENSITY,
                                    height,width);
            break;
        case 180:
            cropbox[i]=PdfRect(pdfInput.GetPage(0)->GetPageSize().GetWidth()-(double)xOffset[i]*72/IMAGE_DENSITY-width,
                                    (double)yOffset[i]*72/IMAGE_DENSITY,
                                    width,height);
            break;
        case 270:
            cropbox[i]=PdfRect(pdfInput.GetPage(0)->GetPageSize().GetHeight()-(double)yOffset[i]*72/IMAGE_DENSITY-height,
                                    pdfInput.GetPage(0)->GetPageSize().GetHeight()-(double)xOffset[i]*72/IMAGE_DENSITY-height,
                                    height,width);
            break;
        default:
            break;
        }
    }
    for(int pageInput=0;pageInput<pdfInput.GetPageCount();pageInput++){
        for(int pageCount=0;pageCount<pagesPerSheet;pageCount++){
            pdfOutput.InsertExistingPageAt(pdfInput,pageInput,pageInput*pagesPerSheet+pageCount);
            PdfPage* pPage = pdfOutput.GetPage(pageInput*pagesPerSheet+pageCount);
            crop_page(pPage,cropbox[pageCount]);
        }
    }
    pdfOutput.Write(ui->lneOutput->text().toLocal8Bit().constData());
#endif

    QMessageBox::information(this,"finished","convert finished");
}

void MainWindow::on_btnInput_clicked()
{
    QString filename=QFileDialog::getOpenFileName(this,QString(),ui->lneInput->text());
    if(filename.length()!=0){
        ui->lneInput->setText(filename);
        emit on_lneInput_returnPressed();
    }
}

void MainWindow::on_btnOutput_clicked()
{
    QString filename=QFileDialog::getSaveFileName(this,QString(),ui->lneOutput->text());
    if(filename.length()!=0){
        ui->lneOutput->setText(filename);
    }
}

void MainWindow::drawPixmap()
{
    QPixmap pixmap_draw=pixmap;
    QPainter painter(&pixmap_draw);
    painter.setPen(Qt::red);
    QPainterPath path[ui->spbPagesPerSheet->value()];
    for(int i=0;i<ui->spbPagesPerSheet->value();i++){
        path[i].moveTo(spbPage[i+1][0]->value(),spbPage[i+1][1]->value());
        path[i].lineTo(spbPage[i+1][0]->value()+ui->spbWidth->value(),spbPage[i+1][1]->value());
        path[i].lineTo(spbPage[i+1][0]->value()+ui->spbWidth->value(),spbPage[i+1][1]->value()+ui->spbHeight->value());
        path[i].lineTo(spbPage[i+1][0]->value(),spbPage[i+1][1]->value()+ui->spbHeight->value());
        path[i].lineTo(spbPage[i+1][0]->value(),spbPage[i+1][1]->value());
    }
    for(int i=0;i<ui->spbPagesPerSheet->value();i++){
        painter.drawPath(path[i]);
    }
    ui->labelSelectPoint->setPixmap(pixmap_draw);
}

void MainWindow::on_btnAutoDetect_clicked()
{
    //find the upperleft point of the first page
    QPoint point[ui->spbPagesPerSheet->value()];
    point[0]=findFirstPoint();
    if(point[0].x()==-1){
        QMessageBox::warning(this,tr("warning"),tr("page not found"));
        return;
    }

    //find the height and width
    int height,width;
    findSize(point[0],width,height);

    //find columns
    std::vector<int> columns(1);
    findColumns(point[0],width,columns);

    //find rows
    std::vector<int> rows(1);
    findRows(point[0],height,rows);

    //ask if only one page is detected
    if(columns.size()==1 and rows.size()==1){
        int numColumns;
        int numRows;
        SetPagesDialog *dlgSetPages=new SetPagesDialog(numColumns,numRows,this);
        dlgSetPages->exec();

        height/=numRows;
        width/=numColumns;
        for(int i=1;i<numColumns;i++){
            columns.push_back(columns[i-1]+width);
        }
        for(int i=1;i<numRows;i++){
            rows.push_back(rows[i-1]+height);
        }
        delete dlgSetPages;
    }

    ui->spbPagesPerSheet->setValue(rows.size()*columns.size());
    ui->spbWidth->setValue(width);
    ui->spbHeight->setValue(height);
    for(int i=1;i<=ui->spbPagesPerSheet->value() and i<=rows.size()*columns.size();i++){
        spbPage[i][0]->setValue(columns[(i-1)%columns.size()]);
        spbPage[i][1]->setValue(rows[(i-1)/columns.size()]);
    }
    drawPixmap();
}

QPoint MainWindow::findFirstPoint(int xOffset, int yOffset)
{
    QPoint point;
    for(;yOffset<image.height();yOffset++){
        const QRgb *pixel=reinterpret_cast< const QRgb* >(image.constScanLine(yOffset));
        for(;xOffset<image.width();xOffset++){
            if(*(pixel+xOffset)!=4294967295){
                point.setX(xOffset);
                point.setY(yOffset);
                //if white in 100, find the next point
                int length;
                for(length=0;length<100 and point.y()+length<image.height() and point.x()+length<image.width();length++){
                    if(image.pixel(point.x(),point.y()+length)==4294967295 or image.pixel(point.x()+length,point.y())==4294967295){
                        length=101;//not a page
                        break;
                    }
                }
                if(length!=101){
                    return point;
                }
            }
        }
        xOffset=0;
    }
    return QPoint(-1,-1);
}

void MainWindow::findSize(QPoint first, int &width, int &height){
    //find width
    for(int i=0;i+first.x()<image.width();i++){
        if(image.pixel(first.x()+i,first.y())==4294967295){
            width=i;
            break;
        }
    }
    for(int i=0;i+first.y()<image.height();i++){
        if(image.pixel(first.x(),first.y()+i)==4294967295){
            height=i;
            break;
        }
    }
}

void MainWindow::findColumns(QPoint first, int width, std::vector<int>& columns)
{
    columns[0]=first.x();
    const QRgb *pixel=reinterpret_cast< const QRgb* >(image.constScanLine(first.y()));
    for(int xOffset=first.x()+width;xOffset<image.width();xOffset++){
        if(*(pixel+xOffset)!=4294967295){
            columns.push_back(xOffset);
            xOffset+=width;
        }
    }
}

void MainWindow::findRows(QPoint first, int height, std::vector<int>& rows)
{
    rows[0]=first.y();
    for(int yOffset=first.y()+height;yOffset<image.height();yOffset++){
        if(image.pixel(first.x(),yOffset)!=4294967295){
            rows.push_back(yOffset);
            yOffset+=height;
        }
    }
}

void MainWindow::on_btnUpdate_clicked()
{
    drawPixmap();
}

void MainWindow::on_btnPrevious_clicked()
{
    current_page-=1;
    loadPdf();
    drawPixmap();
}

void MainWindow::on_btnNext_clicked()
{
    current_page+=1;
    loadPdf();
    drawPixmap();
}
