# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/gui/ui/copyprojectdialog.ui',
# licensing of '../src/gui/ui/copyprojectdialog.ui' applies.
#
# Created: Fri Jan 31 10:07:33 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(739, 360)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.oldPathEdit = QtWidgets.QLineEdit(self.groupBox)
        self.oldPathEdit.setObjectName("oldPathEdit")
        self.horizontalLayout.addWidget(self.oldPathEdit)
        self.oldBrowseBtn = QtWidgets.QToolButton(self.groupBox)
        self.oldBrowseBtn.setObjectName("oldBrowseBtn")
        self.horizontalLayout.addWidget(self.oldBrowseBtn)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.oldNameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.oldNameEdit.setObjectName("oldNameEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.oldNameEdit)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.oldAppEdit = QtWidgets.QLineEdit(self.groupBox)
        self.oldAppEdit.setObjectName("oldAppEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.oldAppEdit)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.oldDescriptionEdit = QtWidgets.QTextEdit(self.groupBox)
        self.oldDescriptionEdit.setObjectName("oldDescriptionEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.oldDescriptionEdit)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.oldErrorLabel = QtWidgets.QLabel(Dialog)
        self.oldErrorLabel.setStyleSheet("color: red;")
        self.oldErrorLabel.setObjectName("oldErrorLabel")
        self.verticalLayout_3.addWidget(self.oldErrorLabel)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.newPathEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.newPathEdit.setObjectName("newPathEdit")
        self.horizontalLayout_2.addWidget(self.newPathEdit)
        self.newBrowseBtn = QtWidgets.QToolButton(self.groupBox_2)
        self.newBrowseBtn.setObjectName("newBrowseBtn")
        self.horizontalLayout_2.addWidget(self.newBrowseBtn)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.newNameEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.newNameEdit.setObjectName("newNameEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.newNameEdit)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.newAppEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.newAppEdit.setObjectName("newAppEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.newAppEdit)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.newDescriptionEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.newDescriptionEdit.setObjectName("newDescriptionEdit")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.newDescriptionEdit)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.newErrorLabel = QtWidgets.QLabel(Dialog)
        self.newErrorLabel.setStyleSheet("color: red;")
        self.newErrorLabel.setObjectName("newErrorLabel")
        self.verticalLayout_2.addWidget(self.newErrorLabel)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "Existing Project", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Location", None, -1))
        self.oldBrowseBtn.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Application", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Description", None, -1))
        self.oldErrorLabel.setText(QtWidgets.QApplication.translate("Dialog", "Old Project Errors", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Dialog", "New Project", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Dialog", "Location", None, -1))
        self.newBrowseBtn.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Dialog", "Application", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("Dialog", "Description", None, -1))
        self.newErrorLabel.setText(QtWidgets.QApplication.translate("Dialog", "New Project Errors", None, -1))

