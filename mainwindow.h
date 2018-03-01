#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>
#include <QPainter>
#include <QLineEdit>
#include <QImage>
#include <vector>
#include <QSpinBox>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    QSpinBox *spbPage[7][2];
    QPixmap pixmap;
    QImage image;
    int current_page;
    int set;
    int upperleftX,upperleftY;
    QString fileInput,fileOutput;
    double density_render=300;

    void drawPixmap();
    QPoint findFirstPoint(int xOffset=0,int yOffset=0);
    void findSize(QPoint first,int &width,int &height);
    void findColumns(QPoint first,int width,std::vector<int>& columns);
    void findRows(QPoint first,int height,std::vector<int>& rows);
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_btnWidthHeight_clicked();
    void loadPdf();
    void on_btnPageOne_clicked();
    void on_btnPageTwo_clicked();
    void on_btnPageThree_clicked();
    void on_btnPageFour_clicked();
    void on_btnPageFive_clicked();
    void on_btnPageSix_clicked();
    void on_labelSelectPoint_mousePressed(int , int );
    void convert();
    void on_btnAutoDetect_clicked();
    void on_btnUpdate_clicked();
    void on_btnPrevious_clicked();
    void on_btnNext_clicked();
    void on_action_Open_triggered();
    void on_action_Convert_triggered();
    void on_actionAbout_Qt_triggered();
    void on_action_About_triggered();
    void on_btnZoomIn_clicked();
    void on_btnZoomOut_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
