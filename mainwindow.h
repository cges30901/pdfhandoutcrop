#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>
#include <QPainter>
#include <QLineEdit>
#include <QImage>
#include <vector>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    QLineEdit *lneFrame[7][2];
    QPixmap *pixmap;
    QPixmap *pixmap_draw;
    QImage *image;
    int current_page;
    int set;
    int upperleftX,upperleftY;
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
    void on_lneInput_returnPressed();
    void loadPdf();
    void on_btnFrameOne_clicked();
    void on_btnFrameTwo_clicked();
    void on_btnFrameThree_clicked();
    void on_btnFrameFour_clicked();
    void on_btnFrameFive_clicked();
    void on_btnFrameSix_clicked();
    void on_labelSelectPoint_mousePressed(int , int );
    void on_btnConvert_clicked();
    void on_btnInput_clicked();
    void on_btnOutput_clicked();

    void on_btnAutoDetect_clicked();

    void on_btnUpdate_clicked();

    void on_btnPrevious_clicked();

    void on_btnNext_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
