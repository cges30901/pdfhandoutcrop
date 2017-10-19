#ifndef SETPAGESDIALOG_H
#define SETPAGESDIALOG_H

#include <QDialog>

namespace Ui {
class SetPagesDialog;
}

class SetPagesDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SetPagesDialog(int &columns, int &rows, QWidget *parent = 0);
    ~SetPagesDialog();

private slots:
    void on_pushButton_clicked();

private:
    Ui::SetPagesDialog *ui;
    int *columns;
    int *rows;
};

#endif // SETPAGESDIALOG_H
