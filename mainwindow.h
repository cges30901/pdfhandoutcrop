#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    QPixmap *pixmap;
    int set;
    int upperleftX,upperleftY;
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_btnWidthHeight_clicked();
    void on_lneInput_returnPressed();
    void on_btnFrameOne_clicked();
    void on_btnFrameTwo_clicked();
    void on_btnFrameThree_clicked();
    void on_btnFrameFour_clicked();
    void on_btnFrameFive_clicked();
    void on_btnFrameSix_clicked();
    void on_labelSelectPoint_mousePressed(int , int );
    void on_btnConvert_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
