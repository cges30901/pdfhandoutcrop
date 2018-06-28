# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setpagesdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SetPagesDialog(object):
    def setupUi(self, SetPagesDialog):
        SetPagesDialog.setObjectName("SetPagesDialog")
        SetPagesDialog.resize(521, 208)
        self.verticalLayout = QtWidgets.QVBoxLayout(SetPagesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SetPagesDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(SetPagesDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spbColumns = QtWidgets.QSpinBox(SetPagesDialog)
        self.spbColumns.setProperty("value", 1)
        self.spbColumns.setObjectName("spbColumns")
        self.horizontalLayout.addWidget(self.spbColumns)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(SetPagesDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spbRows = QtWidgets.QSpinBox(SetPagesDialog)
        self.spbRows.setProperty("value", 1)
        self.spbRows.setObjectName("spbRows")
        self.horizontalLayout_2.addWidget(self.spbRows)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.pushButton = QtWidgets.QPushButton(SetPagesDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SetPagesDialog)
        QtCore.QMetaObject.connectSlotsByName(SetPagesDialog)

    def retranslateUi(self, SetPagesDialog):
        _translate = QtCore.QCoreApplication.translate
        SetPagesDialog.setWindowTitle(_translate("SetPagesDialog", "Select layout"))
        self.label.setText(_translate("SetPagesDialog", "Only one page is detected. Please select layout"))
        self.label_2.setText(_translate("SetPagesDialog", "Columns:"))
        self.label_3.setText(_translate("SetPagesDialog", "Rows:"))
        self.pushButton.setText(_translate("SetPagesDialog", "Ok"))

