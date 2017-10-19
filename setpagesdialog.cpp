#include "setpagesdialog.h"
#include "ui_setpagesdialog.h"

SetPagesDialog::SetPagesDialog(int &columns, int &rows, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::SetPagesDialog)
{
    ui->setupUi(this);
    this->columns=&columns;
    this->rows=&rows;
}

SetPagesDialog::~SetPagesDialog()
{
    delete ui;
}

void SetPagesDialog::on_pushButton_clicked()
{
    *columns=ui->spbColumns->value();
    *rows=ui->spbRows->value();
    this->accept();
}
