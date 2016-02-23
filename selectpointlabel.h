#ifndef SELECTPOINTLABEL_H
#define SELECTPOINTLABEL_H

#include <QLabel>
#include <QMouseEvent>

class SelectPointLabel : public QLabel
{
    Q_OBJECT
public:
    SelectPointLabel(QWidget *parent=0);
protected:
    void mousePressEvent(QMouseEvent *event);
public slots:
    void resizeEvent(QResizeEvent *);
signals:
    void mousePressed(int x,int y);
};

#endif // SELECTPOINTLABEL_H
