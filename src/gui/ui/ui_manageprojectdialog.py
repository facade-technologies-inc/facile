# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../src/gui/ui/manageprojectdialog.ui',
# licensing of '../src/gui/ui/manageprojectdialog.ui' applies.
#
# Created: Wed Jan 29 22:26:32 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(641, 410)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.project_tab = QtWidgets.QWidget()
        self.project_tab.setObjectName("project_tab")
        self.formLayout = QtWidgets.QFormLayout(self.project_tab)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.project_tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.locationEdit = QtWidgets.QLineEdit(self.project_tab)
        self.locationEdit.setObjectName("locationEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.locationEdit)
        self.label_2 = QtWidgets.QLabel(self.project_tab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.nameEdit = QtWidgets.QLineEdit(self.project_tab)
        self.nameEdit.setEnabled(False)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.nameEdit)
        self.label_3 = QtWidgets.QLabel(self.project_tab)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.descriptionEdit = QtWidgets.QTextEdit(self.project_tab)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.descriptionEdit)
        self.label_4 = QtWidgets.QLabel(self.project_tab)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.appEdit = QtWidgets.QLineEdit(self.project_tab)
        self.appEdit.setEnabled(False)
        self.appEdit.setObjectName("appEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.appEdit)
        self.label_5 = QtWidgets.QLabel(self.project_tab)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.backendEdit = QtWidgets.QComboBox(self.project_tab)
        self.backendEdit.setObjectName("backendEdit")
        self.backendEdit.addItem("")
        self.backendEdit.addItem("")
        self.backendEdit.addItem("")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.backendEdit)
        self.tabWidget.addTab(self.project_tab, "")
        self.target_gui_model_tab = QtWidgets.QWidget()
        self.target_gui_model_tab.setObjectName("target_gui_model_tab")
        self.tabWidget.addTab(self.target_gui_model_tab, "")
        self.api_model_tab = QtWidgets.QWidget()
        self.api_model_tab.setObjectName("api_model_tab")
        self.tabWidget.addTab(self.api_model_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.backendEdit.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Location", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Description", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Application", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Dialog", "Accessibility\n"
"                                            Technology\n"
"                                        ", None, -1))
        self.backendEdit.setItemText(0, QtWidgets.QApplication.translate("Dialog", "WIN32", None, -1))
        self.backendEdit.setItemText(1, QtWidgets.QApplication.translate("Dialog", "UIA", None, -1))
        self.backendEdit.setItemText(2, QtWidgets.QApplication.translate("Dialog", "Other", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project_tab), QtWidgets.QApplication.translate("Dialog", "Project", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.target_gui_model_tab), QtWidgets.QApplication.translate("Dialog", "Target GUI Model", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.api_model_tab), QtWidgets.QApplication.translate("Dialog", "API Model", None, -1))

