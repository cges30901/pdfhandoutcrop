#-------------------------------------------------
#
# Project created by QtCreator 2016-02-06T11:41:57
#
#-------------------------------------------------

QT       += core gui
LIBS+=-lpoppler-qt5 -lpodofo

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = pdf-qt
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    selectpointlabel.cpp

HEADERS  += mainwindow.h \
    selectpointlabel.h

FORMS    += mainwindow.ui
