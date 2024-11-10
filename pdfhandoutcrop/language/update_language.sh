#!/bin/bash
pylupdate6 --no-obsolete --ts pdfhandoutcrop.ts --ts pdfhandoutcrop_it.ts --ts pdfhandoutcrop_nl.ts --ts pdfhandoutcrop_ru.ts --ts pdfhandoutcrop_zh_TW.ts ../mainwindow.py ../setlayoutdialog.py ../mainwindow.ui ../setlayoutdialog.ui
/usr/lib/qt6/bin/lrelease pdfhandoutcrop_*.ts
