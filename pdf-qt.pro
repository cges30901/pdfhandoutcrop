#-------------------------------------------------
#
# Project created by QtCreator 2016-02-06T11:41:57
#
#-------------------------------------------------

QT       += core gui
QMAKE_CXXFLAGS+=`Magick++-config --cppflags --cxxflags --ldflags --lib`
QMAKE_LFLAGS+=`Magick++-config --cppflags --cxxflags --ldflags --lib`
LIBS+=-lpoppler-qt5

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = pdf-qt
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    selectpointlabel.cpp

HEADERS  += mainwindow.h \
    selectpointlabel.h

FORMS    += mainwindow.ui
