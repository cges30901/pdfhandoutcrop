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
    /*
    printf("%f %f %f %f\n",
           rCropBox.GetLeft(),
           rCropBox.GetBottom(),
           rCropBox.GetWidth(),
           rCropBox.GetHeight());
    */
    rCropBox.ToVariant( var );
    pPage->GetObject()->GetDictionary().AddKey( PdfName("MediaBox"), var );
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    set=0;
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
        pixmap=new QPixmap(QPixmap::fromImage(pdfPage->renderToImage(IMAGE_DENSITY,IMAGE_DENSITY)));
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
    if(set==1){
        ui->lneFrameOneX->setText(QString::number(x));
        ui->lneFrameOneY->setText(QString::number(y));
        set=0;
    }
    else if(set==2){
        ui->lneFrameTwoX->setText(QString::number(x));
        ui->lneFrameTwoY->setText(QString::number(y));
        set=0;
    }
    else if(set==3){
        ui->lneFrameThreeX->setText(QString::number(x));
        ui->lneFrameThreeY->setText(QString::number(y));
        set=0;
    }
    else if(set==4){
        ui->lneFrameFourX->setText(QString::number(x));
        ui->lneFrameFourY->setText(QString::number(y));
        set=0;
    }
    else if(set==5){
        ui->lneFrameFiveX->setText(QString::number(x));
        ui->lneFrameFiveY->setText(QString::number(y));
        set=0;
    }
    else if(set==6){
        ui->lneFrameSixX->setText(QString::number(x));
        ui->lneFrameSixY->setText(QString::number(y));
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
    /*vector<Image> input;
    ReadOptions options;
    options.density(Geometry(IMAGE_DENSITY,IMAGE_DENSITY));
    ui->statusBar->showMessage("reading...");
    readImages(&input,ui->lneInput->text().toStdString(),options);
    int frames=ui->spbFrames->value();
    //int size=input.size()*frames;
    vector<Image> output(input.size()*frames);
    int xOffset[6];
    int yOffset[6];
    //for(int i=0;i<frames;i++){
        //cin>>xOffset[i]>>yOffset[i];
    //}
    xOffset[0]=ui->lneFrameOneX->text().toInt();
    yOffset[0]=ui->lneFrameOneY->text().toInt();
    xOffset[1]=ui->lneFrameTwoX->text().toInt();
    yOffset[1]=ui->lneFrameTwoY->text().toInt();
    xOffset[2]=ui->lneFrameThreeX->text().toInt();
    yOffset[2]=ui->lneFrameThreeY->text().toInt();
    xOffset[3]=ui->lneFrameFourX->text().toInt();
    yOffset[3]=ui->lneFrameFourY->text().toInt();
    xOffset[4]=ui->lneFrameFiveX->text().toInt();
    yOffset[4]=ui->lneFrameFiveY->text().toInt();
    xOffset[5]=ui->lneFrameSixX->text().toInt();
    yOffset[5]=ui->lneFrameSixY->text().toInt();
    ui->statusBar->showMessage("cropping...");
    for(unsigned int i=0;i<input.size();i++){
        for(int j=0;j<frames;j++){
            output[i*frames+j]=input[i];
            output[i*frames+j].crop(Geometry(ui->lneWidth->text().toInt(),ui->lneHeight->text().toInt(),xOffset[j],yOffset[j]));
            output[i*frames+j].page(Geometry(ui->lneWidth->text().toInt(),ui->lneHeight->text().toInt()));
        }
    }
    ui->statusBar->showMessage("writing...");
    writeImages(output.begin(),output.end(),ui->lneOutput->text().toStdString());
    ui->statusBar->clearMessage();
    QMessageBox::information(this,"finished","finished");
    */
    PdfError::EnableDebug( true );
    PdfError::EnableLogging(false);
    PdfMemDocument pdfInput;
    pdfInput.Load(ui->lneInput->text().toLocal8Bit().constData());
    int frames=ui->spbFrames->value();
    PdfMemDocument pdfOutput;
    int xOffset[6];
    int yOffset[6];
    xOffset[0]=ui->lneFrameOneX->text().toInt();
    yOffset[0]=ui->lneFrameOneY->text().toInt();
    xOffset[1]=ui->lneFrameTwoX->text().toInt();
    yOffset[1]=ui->lneFrameTwoY->text().toInt();
    xOffset[2]=ui->lneFrameThreeX->text().toInt();
    yOffset[2]=ui->lneFrameThreeY->text().toInt();
    xOffset[3]=ui->lneFrameFourX->text().toInt();
    yOffset[3]=ui->lneFrameFourY->text().toInt();
    xOffset[4]=ui->lneFrameFiveX->text().toInt();
    yOffset[4]=ui->lneFrameFiveY->text().toInt();
    xOffset[5]=ui->lneFrameSixX->text().toInt();
    yOffset[5]=ui->lneFrameSixY->text().toInt();
    int width=ui->lneWidth->text().toDouble()*72/300;
    int height=ui->lneHeight->text().toDouble()*72/300;
    PdfRect cropbox[frames];
    for(int i=0;i<frames;i++){
        cropbox[i]=PdfRect(double(xOffset[i]*72/300),
                                pdfInput.GetPage(0)->GetPageSize().GetHeight()-yOffset[i]*72/300-height,
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
    QPainterPath path[6];
    path[0].moveTo(ui->lneFrameOneX->text().toDouble(),ui->lneFrameOneY->text().toDouble());
    path[0].lineTo(ui->lneFrameOneX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameOneY->text().toDouble());
    path[0].lineTo(ui->lneFrameOneX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameOneY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[0].lineTo(ui->lneFrameOneX->text().toDouble(),ui->lneFrameOneY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[0].lineTo(ui->lneFrameOneX->text().toDouble(),ui->lneFrameOneY->text().toDouble());
    path[1].moveTo(ui->lneFrameTwoX->text().toDouble(),ui->lneFrameTwoY->text().toDouble());
    path[1].lineTo(ui->lneFrameTwoX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameTwoY->text().toDouble());
    path[1].lineTo(ui->lneFrameTwoX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameTwoY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[1].lineTo(ui->lneFrameTwoX->text().toDouble(),ui->lneFrameTwoY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[1].lineTo(ui->lneFrameTwoX->text().toDouble(),ui->lneFrameTwoY->text().toDouble());
    path[2].moveTo(ui->lneFrameThreeX->text().toDouble(),ui->lneFrameThreeY->text().toDouble());
    path[2].lineTo(ui->lneFrameThreeX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameThreeY->text().toDouble());
    path[2].lineTo(ui->lneFrameThreeX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameThreeY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[2].lineTo(ui->lneFrameThreeX->text().toDouble(),ui->lneFrameThreeY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[2].lineTo(ui->lneFrameThreeX->text().toDouble(),ui->lneFrameThreeY->text().toDouble());
    path[3].moveTo(ui->lneFrameFourX->text().toDouble(),ui->lneFrameFourY->text().toDouble());
    path[3].lineTo(ui->lneFrameFourX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameFourY->text().toDouble());
    path[3].lineTo(ui->lneFrameFourX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameFourY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[3].lineTo(ui->lneFrameFourX->text().toDouble(),ui->lneFrameFourY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[3].lineTo(ui->lneFrameFourX->text().toDouble(),ui->lneFrameFourY->text().toDouble());
    path[4].moveTo(ui->lneFrameFiveX->text().toDouble(),ui->lneFrameFiveY->text().toDouble());
    path[4].lineTo(ui->lneFrameFiveX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameFiveY->text().toDouble());
    path[4].lineTo(ui->lneFrameFiveX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameFiveY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[4].lineTo(ui->lneFrameFiveX->text().toDouble(),ui->lneFrameFiveY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[4].lineTo(ui->lneFrameFiveX->text().toDouble(),ui->lneFrameFiveY->text().toDouble());
    path[5].moveTo(ui->lneFrameSixX->text().toDouble(),ui->lneFrameSixY->text().toDouble());
    path[5].lineTo(ui->lneFrameSixX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameSixY->text().toDouble());
    path[5].lineTo(ui->lneFrameSixX->text().toDouble()+ui->lneWidth->text().toDouble(),ui->lneFrameSixY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[5].lineTo(ui->lneFrameSixX->text().toDouble(),ui->lneFrameSixY->text().toDouble()+ui->lneHeight->text().toDouble());
    path[5].lineTo(ui->lneFrameSixX->text().toDouble(),ui->lneFrameSixY->text().toDouble());

    for(int i=0;i<ui->spbFrames->value();i++){
        painter.drawPath(path[i]);
    }
    ui->labelSelectPoint->setPixmap(*pixmap_draw);
}
