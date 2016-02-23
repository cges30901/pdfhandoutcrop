#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <Magick++.h>
#include <vector>
#include <QMessageBox>
#include <poppler/qt5/poppler-qt5.h>

#define IMAGE_DENSITY 300

using namespace Magick;
using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    set=0;
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
        Poppler::Page* pdfPage = document->page(0);
        //pixmap=new QPixmap::fromImage(pdfPage->renderToImage(300,300));
        ui->labelSelectPoint->setPixmap(QPixmap::fromImage(pdfPage->renderToImage(300,300)));
        /*Image image;
        image.density(Geometry(IMAGE_DENSITY,IMAGE_DENSITY));
        image.read(ui->lneInput->text().toStdString()+"[0]");
        image.write("pdf-qt-output.png");
        pixmap=new QPixmap("pdf-qt-output.png");
        ui->labelSelectPoint->setPixmap(*pixmap);*/
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
}

void MainWindow::on_btnConvert_clicked()
{
    vector<Image> input;
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
}
