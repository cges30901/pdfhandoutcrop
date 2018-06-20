# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1043, 499)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1023, 327))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelSelectPoint = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSelectPoint.sizePolicy().hasHeightForWidth())
        self.labelSelectPoint.setSizePolicy(sizePolicy)
        self.labelSelectPoint.setText("")
        self.labelSelectPoint.setObjectName("labelSelectPoint")
        self.horizontalLayout_5.addWidget(self.labelSelectPoint)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnAutoDetect = QtWidgets.QPushButton(self.centralWidget)
        self.btnAutoDetect.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAutoDetect.sizePolicy().hasHeightForWidth())
        self.btnAutoDetect.setSizePolicy(sizePolicy)
        self.btnAutoDetect.setObjectName("btnAutoDetect")
        self.horizontalLayout_2.addWidget(self.btnAutoDetect)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spbPagesPerSheet = QtWidgets.QSpinBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbPagesPerSheet.sizePolicy().hasHeightForWidth())
        self.spbPagesPerSheet.setSizePolicy(sizePolicy)
        self.spbPagesPerSheet.setMinimum(1)
        self.spbPagesPerSheet.setProperty("value", 6)
        self.spbPagesPerSheet.setObjectName("spbPagesPerSheet")
        self.horizontalLayout_2.addWidget(self.spbPagesPerSheet)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnUpdate = QtWidgets.QPushButton(self.centralWidget)
        self.btnUpdate.setEnabled(False)
        self.btnUpdate.setObjectName("btnUpdate")
        self.horizontalLayout_2.addWidget(self.btnUpdate)
        self.labelPageNum = QtWidgets.QLabel(self.centralWidget)
        self.labelPageNum.setText("")
        self.labelPageNum.setObjectName("labelPageNum")
        self.horizontalLayout_2.addWidget(self.labelPageNum)
        self.btnPrevious = QtWidgets.QPushButton(self.centralWidget)
        self.btnPrevious.setEnabled(False)
        self.btnPrevious.setObjectName("btnPrevious")
        self.horizontalLayout_2.addWidget(self.btnPrevious)
        self.btnNext = QtWidgets.QPushButton(self.centralWidget)
        self.btnNext.setEnabled(False)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout_2.addWidget(self.btnNext)
        self.btnZoomIn = QtWidgets.QPushButton(self.centralWidget)
        self.btnZoomIn.setObjectName("btnZoomIn")
        self.horizontalLayout_2.addWidget(self.btnZoomIn)
        self.btnZoomOut = QtWidgets.QPushButton(self.centralWidget)
        self.btnZoomOut.setObjectName("btnZoomOut")
        self.horizontalLayout_2.addWidget(self.btnZoomOut)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelWidthHeight = QtWidgets.QLabel(self.centralWidget)
        self.labelWidthHeight.setObjectName("labelWidthHeight")
        self.horizontalLayout_3.addWidget(self.labelWidthHeight)
        self.spbWidth = QtWidgets.QSpinBox(self.centralWidget)
        self.spbWidth.setMaximum(9999)
        self.spbWidth.setObjectName("spbWidth")
        self.horizontalLayout_3.addWidget(self.spbWidth)
        self.spbHeight = QtWidgets.QSpinBox(self.centralWidget)
        self.spbHeight.setMaximum(9999)
        self.spbHeight.setObjectName("spbHeight")
        self.horizontalLayout_3.addWidget(self.spbHeight)
        self.btnWidthHeight = QtWidgets.QPushButton(self.centralWidget)
        self.btnWidthHeight.setObjectName("btnWidthHeight")
        self.horizontalLayout_3.addWidget(self.btnWidthHeight)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboPosition = QtWidgets.QComboBox(self.centralWidget)
        self.comboPosition.setObjectName("comboPosition")
        self.horizontalLayout_3.addWidget(self.comboPosition)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.spbPositionX = QtWidgets.QSpinBox(self.centralWidget)
        self.spbPositionX.setMaximum(9999)
        self.spbPositionX.setObjectName("spbPositionX")
        self.horizontalLayout_3.addWidget(self.spbPositionX)
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spbPositionY = QtWidgets.QSpinBox(self.centralWidget)
        self.spbPositionY.setMaximum(9999)
        self.spbPositionY.setObjectName("spbPositionY")
        self.horizontalLayout_3.addWidget(self.spbPositionY)
        self.btnPosition = QtWidgets.QPushButton(self.centralWidget)
        self.btnPosition.setObjectName("btnPosition")
        self.horizontalLayout_3.addWidget(self.btnPosition)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1043, 32))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Convert = QtWidgets.QAction(MainWindow)
        self.action_Convert.setObjectName("action_Convert")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Convert)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_Help.addAction(self.action_About)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PdfHandoutCrop"))
        self.btnAutoDetect.setText(_translate("MainWindow", "&Auto detect"))
        self.label.setText(_translate("MainWindow", "Pages per sheet:"))
        self.btnUpdate.setText(_translate("MainWindow", "&Update"))
        self.btnPrevious.setText(_translate("MainWindow", "&Previous"))
        self.btnNext.setText(_translate("MainWindow", "&Next"))
        self.btnZoomIn.setText(_translate("MainWindow", "Zoom &in"))
        self.btnZoomOut.setText(_translate("MainWindow", "Zoom &out"))
        self.labelWidthHeight.setText(_translate("MainWindow", "Width and Height"))
        self.btnWidthHeight.setText(_translate("MainWindow", "Click to set"))
        self.label_2.setText(_translate("MainWindow", "Position:"))
        self.label_3.setText(_translate("MainWindow", "x:"))
        self.label_4.setText(_translate("MainWindow", "y:"))
        self.btnPosition.setText(_translate("MainWindow", "Click to set"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_Convert.setText(_translate("MainWindow", "&Convert"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About &Qt"))
        self.action_About.setText(_translate("MainWindow", "&About"))

