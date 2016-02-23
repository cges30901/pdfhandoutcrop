#include "selectpointlabel.h"

SelectPointLabel::SelectPointLabel(QWidget *parent):QLabel(parent)
{

}

void SelectPointLabel::mousePressEvent(QMouseEvent *event){
    emit mousePressed(event->pos().x(),event->pos().y());
}

void SelectPointLabel::resizeEvent(QResizeEvent * e)
{
    if(this->pixmap()!=0)
    this->setPixmap(this->pixmap()->scaledToHeight(this->height()));
    QLabel::resizeEvent(e);

}
