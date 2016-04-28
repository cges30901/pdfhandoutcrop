#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <vector>
#include <QMessageBox>
#include <poppler/qt5/poppler-qt5.h>
#include <podofo/podofo.h>
#include <QFileDialog>

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
    lneFrame[1][0]=ui->lneFrameOneX;
    lneFrame[1][1]=ui->lneFrameOneY;
    lneFrame[2][0]=ui->lneFrameTwoX;
    lneFrame[2][1]=ui->lneFrameTwoY;
    lneFrame[3][0]=ui->lneFrameThreeX;
    lneFrame[3][1]=ui->lneFrameThreeY;
    lneFrame[4][0]=ui->lneFrameFourX;
    lneFrame[4][1]=ui->lneFrameFourY;
    lneFrame[5][0]=ui->lneFrameFiveX;
    lneFrame[5][1]=ui->lneFrameFiveY;
    lneFrame[6][0]=ui->lneFrameSixX;
    lneFrame[6][1]=ui->lneFrameSixY;
    pixmap_draw=new QPixmap(*pixmap);
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
    if(ui->lneInput->text()!=0){
        ui->labelSelectPoint->setText(tr("Loading..."));
        ui->labelSelectPoint->repaint();

        Poppler::Document* document=Poppler::Document::load(ui->lneInput->text());
        if (!document || document->isLocked()) {
            QMessageBox::warning(this,tr("warning"),tr("can not open input file"));
            ui->labelSelectPoint->setText(tr(""));
            delete document;
            return;
        }
        Poppler::Page* pdfPage = document->page(0);
        image=new QImage(pdfPage->renderToImage(IMAGE_DENSITY,IMAGE_DENSITY));
        pixmap=new QPixmap(QPixmap::fromImage(*image));
        ui->labelSelectPoint->setPixmap(*pixmap);
        delete pdfPage;
        delete document;
    }
}
void MainWindow::on_btnFrameOne_clicked()
{
    set=1;
}

void MainWindow::on_btnFrameTwo_clicked()
{
    set=2;
}

void MainWindow::on_btnFrameThree_clicked()
{
    set=3;
}

void MainWindow::on_btnFrameFour_clicked()
{
    set=4;
}

void MainWindow::on_btnFrameFive_clicked()
{
    set=5;
}

void MainWindow::on_btnFrameSix_clicked()
{
    set=6;
}

void MainWindow::on_labelSelectPoint_mousePressed(int x, int y)
{
    if(set>=1 and set <=6){
        lneFrame[set][0]->setText(QString::number(x));
        lneFrame[set][1]->setText(QString::number(y));
        set=0;
    }
    else if(set==7){//set Width and Height - step one
        upperleftX=x;
        upperleftY=y;
        set=8;
    }
    else if(set==8){//set Width and Height - step two
        ui->lneWidth->setText(QString::number(x-upperleftX));
        ui->lneHeight->setText(QString::number(y-upperleftY));
        set=0;
    }
    drawPixmap();
}

void MainWindow::on_btnConvert_clicked()
{
    PdfError::EnableDebug( true );
    PdfError::EnableLogging(false);
    PdfMemDocument pdfInput;
    pdfInput.Load(ui->lneInput->text().toLocal8Bit().constData());
    int frames=ui->spbFrames->value();
    PdfMemDocument pdfOutput;
    int xOffset[frames];
    int yOffset[frames];
    for(int i=0;i<frames;i++){
        xOffset[i]=lneFrame[i+1][0]->text().toInt();
        yOffset[i]=lneFrame[i+1][1]->text().toInt();
    }
    int width=ui->lneWidth->text().toDouble()*72/IMAGE_DENSITY;
    int height=ui->lneHeight->text().toDouble()*72/IMAGE_DENSITY;
    PdfRect cropbox[frames];
    for(int i=0;i<frames;i++){
        cropbox[i]=PdfRect(double(xOffset[i]*72/IMAGE_DENSITY),
                                pdfInput.GetPage(0)->GetPageSize().GetHeight()-yOffset[i]*72/IMAGE_DENSITY-height,
                                width,height);
    }
    for(int pageInput=0;pageInput<pdfInput.GetPageCount();pageInput++){
        for(int frameCount=0;frameCount<frames;frameCount++){
            pdfOutput.InsertExistingPageAt(pdfInput,pageInput,pageInput*frames+frameCount);
            PdfPage* pPage = pdfOutput.GetPage(pageInput*frames+frameCount);
            crop_page(pPage,cropbox[frameCount]);
        }
    }
    pdfOutput.Write(ui->lneOutput->text().toLocal8Bit().constData());
    QMessageBox::information(this,"finished","finished");
}

void MainWindow::on_btnInput_clicked()
{
    QString filename=QFileDialog::getOpenFileName(this,QString(),ui->lneInput->text());
    if(filename.length()!=0){
        ui->lneInput->setText(filename);
    }
    emit on_lneInput_returnPressed();
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
    delete pixmap_draw;
    pixmap_draw=new QPixmap(*pixmap);
    QPainter painter(pixmap_draw);
    painter.setPen(Qt::red);
    QPainterPath path[ui->spbFrames->value()];
    for(int i=0;i<ui->spbFrames->value();i++){
        if(lneFrame[i+1][0]->text().isEmpty() or lneFrame[i+1][1]->text().isEmpty()) continue;
        path[i].moveTo(lneFrame[i+1][0]->text().toDouble(),lneFrame[i+1][1]->text().toDouble());
        path[i].lineTo(lneFrame[i+1][0]->text().toDouble()+ui->lneWidth->text().toDouble(),lneFrame[i+1][1]->text().toDouble());
        path[i].lineTo(lneFrame[i+1][0]->text().toDouble()+ui->lneWidth->text().toDouble(),lneFrame[i+1][1]->text().toDouble()+ui->lneHeight->text().toDouble());
        path[i].lineTo(lneFrame[i+1][0]->text().toDouble(),lneFrame[i+1][1]->text().toDouble()+ui->lneHeight->text().toDouble());
        path[i].lineTo(lneFrame[i+1][0]->text().toDouble(),lneFrame[i+1][1]->text().toDouble());
    }
    for(int i=0;i<ui->spbFrames->value();i++){
        painter.drawPath(path[i]);
    }
    ui->labelSelectPoint->setPixmap(*pixmap_draw);
}

void MainWindow::on_btnAutoDetect_clicked()
{
    //find the upperleft point of the first frame
    QPoint point[ui->spbFrames->text().toInt()];
    point[0]=findFirstPoint();

    //find the height and width
    int height,width;
    findSize(point[0],width,height);

    //find columns
    std::vector<int> columns(1);
    findColumns(point[0],width,columns);

    //find rows
    std::vector<int> rows(1);
    findRows(point[0],height,rows);

    ui->lneWidth->setText(QString::number(width));
    ui->lneHeight->setText(QString::number(height));
    for(int i=1;i<=ui->spbFrames->value() and i<=rows.size()*columns.size();i++){
        lneFrame[i][0]->setText(QString::number(columns[(i-1)%columns.size()]));
        lneFrame[i][1]->setText(QString::number(rows[(i-1)/columns.size()]));
    }
    drawPixmap();
}

QPoint MainWindow::findFirstPoint(int xOffset, int yOffset)
{
    QPoint point;
    for(;yOffset<image->height();yOffset++){
        const QRgb *pixel=reinterpret_cast< const QRgb* >(image->constScanLine(yOffset));
        for(;xOffset<image->width();xOffset++){
            if(*(pixel+xOffset)!=4294967295){
                point.setX(xOffset);
                point.setY(yOffset);
                //if white in 100, find the next point
                for(int length=0;length<100 and point.y()+length<image->height() and point.x()+length<image->width();length++){
                    if(image->pixel(point.x(),point.y()+length)==4294967295 or image->pixel(point.x()+length,point.y())==4294967295)
                        point=findFirstPoint(point.x()+1,point.y());
                }
                return point;
            }
        }
        xOffset=0;
    }
    return point;
}

void MainWindow::findSize(QPoint first, int &width, int &height){
    //find width
    for(int i=0;i+first.x()<image->width();i++){
        if(image->pixel(first.x()+i,first.y())==4294967295){
            width=i;
            break;
        }
    }
    for(int i=0;i+first.y()<image->height();i++){
        if(image->pixel(first.x(),first.y()+i)==4294967295){
            height=i;
            break;
        }
    }
}

void MainWindow::findColumns(QPoint first, int width, std::vector<int>& columns)
{
    columns[0]=first.x();
    const QRgb *pixel=reinterpret_cast< const QRgb* >(image->constScanLine(first.y()));
    for(int xOffset=first.x()+width;xOffset<image->width();xOffset++){
        if(*(pixel+xOffset)!=4294967295){
            columns.push_back(xOffset);
            xOffset+=width;
        }
    }
}

void MainWindow::findRows(QPoint first, int height, std::vector<int>& rows)
{
    rows[0]=first.y();
    for(int yOffset=first.y()+height;yOffset<image->height();yOffset++){
        if(image->pixel(first.x(),yOffset)!=4294967295){
            rows.push_back(yOffset);
            yOffset+=height;
        }
    }
}
