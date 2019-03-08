# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setlayoutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetLayoutDialog(object):
    def setupUi(self, SetLayoutDialog):
        SetLayoutDialog.setObjectName("SetLayoutDialog")
        SetLayoutDialog.resize(521, 305)
        self.verticalLayout = QtWidgets.QVBoxLayout(SetLayoutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SetLayoutDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(SetLayoutDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spbColumns = QtWidgets.QSpinBox(SetLayoutDialog)
        self.spbColumns.setProperty("value", 1)
        self.spbColumns.setObjectName("spbColumns")
        self.horizontalLayout.addWidget(self.spbColumns)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(SetLayoutDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spbRows = QtWidgets.QSpinBox(SetLayoutDialog)
        self.spbRows.setProperty("value", 1)
        self.spbRows.setObjectName("spbRows")
        self.horizontalLayout_2.addWidget(self.spbRows)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(SetLayoutDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.comboOrder = QtWidgets.QComboBox(SetLayoutDialog)
        self.comboOrder.setObjectName("comboOrder")
        self.horizontalLayout_6.addWidget(self.comboOrder)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.pushButton = QtWidgets.QPushButton(SetLayoutDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SetLayoutDialog)
        QtCore.QMetaObject.connectSlotsByName(SetLayoutDialog)

    def retranslateUi(self, SetLayoutDialog):
        _translate = QtCore.QCoreApplication.translate
        SetLayoutDialog.setWindowTitle(_translate("SetLayoutDialog", "Select layout"))
        self.label.setText(_translate("SetLayoutDialog", "Only one page is detected. Please select layout"))
        self.label_2.setText(_translate("SetLayoutDialog", "Columns:"))
        self.label_3.setText(_translate("SetLayoutDialog", "Rows:"))
        self.label_4.setText(_translate("SetLayoutDialog", "Order:"))
        self.pushButton.setText(_translate("SetLayoutDialog", "Ok"))


