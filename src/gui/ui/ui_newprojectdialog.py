# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newprojectdialog.ui',
# licensing of 'newprojectdialog.ui' applies.
#
# Created: Sat Nov  2 18:52:54 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets


class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(538, 515)
		self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Dialog)
		self.horizontalLayout_6.setObjectName("horizontalLayout_6")
		spacerItem = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Expanding,
		                                   QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_6.addItem(spacerItem)
		self.verticalLayout_4 = QtWidgets.QVBoxLayout()
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
		                                    QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacerItem1)
		self.title_label = QtWidgets.QLabel(Dialog)
		self.title_label.setObjectName("title_label")
		self.horizontalLayout_5.addWidget(self.title_label)
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
		                                    QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacerItem2)
		self.verticalLayout_4.addLayout(self.horizontalLayout_5)
		self.formLayout = QtWidgets.QFormLayout()
		self.formLayout.setObjectName("formLayout")
		self.name_label = QtWidgets.QLabel(Dialog)
		self.name_label.setObjectName("name_label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name_label)
		self.project_name_edit = QtWidgets.QLineEdit(Dialog)
		self.project_name_edit.setObjectName("project_name_edit")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.project_name_edit)
		self.description_label = QtWidgets.QLabel(Dialog)
		self.description_label.setObjectName("description_label")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.description_label)
		self.description_edit = QtWidgets.QTextEdit(Dialog)
		self.description_edit.setObjectName("description_edit")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.description_edit)
		self.project_folder_label = QtWidgets.QLabel(Dialog)
		self.project_folder_label.setObjectName("project_folder_label")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.project_folder_label)
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.project_folder_edit = QtWidgets.QLineEdit(Dialog)
		self.project_folder_edit.setObjectName("project_folder_edit")
		self.horizontalLayout_4.addWidget(self.project_folder_edit)
		self.browseFilesButton_folder = QtWidgets.QToolButton(Dialog)
		self.browseFilesButton_folder.setObjectName("browseFilesButton_folder")
		self.horizontalLayout_4.addWidget(self.browseFilesButton_folder)
		self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
		self.application_label = QtWidgets.QLabel(Dialog)
		self.application_label.setObjectName("application_label")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.application_label)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.executable_file_edit = QtWidgets.QLineEdit(Dialog)
		self.executable_file_edit.setObjectName("executable_file_edit")
		self.horizontalLayout.addWidget(self.executable_file_edit)
		self.browseFilesButton_executable = QtWidgets.QToolButton(Dialog)
		self.browseFilesButton_executable.setObjectName("browseFilesButton_executable")
		self.horizontalLayout.addWidget(self.browseFilesButton_executable)
		self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
		self.verticalLayout_4.addLayout(self.formLayout)
		self.line = QtWidgets.QFrame(Dialog)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")
		self.verticalLayout_4.addWidget(self.line)
		self.label_4 = QtWidgets.QLabel(Dialog)
		self.label_4.setObjectName("label_4")
		self.verticalLayout_4.addWidget(self.label_4)
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.groupBox = QtWidgets.QGroupBox(Dialog)
		self.groupBox.setObjectName("groupBox")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.option_MFC = QtWidgets.QRadioButton(self.groupBox)
		self.option_MFC.setObjectName("option_MFC")
		self.verticalLayout_2.addWidget(self.option_MFC)
		self.option_VB6 = QtWidgets.QRadioButton(self.groupBox)
		self.option_VB6.setObjectName("option_VB6")
		self.verticalLayout_2.addWidget(self.option_VB6)
		self.option_VCL = QtWidgets.QRadioButton(self.groupBox)
		self.option_VCL.setObjectName("option_VCL")
		self.verticalLayout_2.addWidget(self.option_VCL)
		self.option_Legacy = QtWidgets.QRadioButton(self.groupBox)
		self.option_Legacy.setObjectName("option_Legacy")
		self.verticalLayout_2.addWidget(self.option_Legacy)
		self.horizontalLayout_3.addWidget(self.groupBox)
		self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
		self.groupBox_2.setObjectName("groupBox_2")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
		self.verticalLayout.setObjectName("verticalLayout")
		self.option_WinForms = QtWidgets.QRadioButton(self.groupBox_2)
		self.option_WinForms.setObjectName("option_WinForms")
		self.verticalLayout.addWidget(self.option_WinForms)
		self.option_WPF = QtWidgets.QRadioButton(self.groupBox_2)
		self.option_WPF.setObjectName("option_WPF")
		self.verticalLayout.addWidget(self.option_WPF)
		self.option_Qt5 = QtWidgets.QRadioButton(self.groupBox_2)
		self.option_Qt5.setObjectName("option_Qt5")
		self.verticalLayout.addWidget(self.option_Qt5)
		self.option_Store_App = QtWidgets.QRadioButton(self.groupBox_2)
		self.option_Store_App.setObjectName("option_Store_App")
		self.verticalLayout.addWidget(self.option_Store_App)
		self.option_Browser = QtWidgets.QRadioButton(self.groupBox_2)
		self.option_Browser.setObjectName("option_Browser")
		self.verticalLayout.addWidget(self.option_Browser)
		self.horizontalLayout_3.addWidget(self.groupBox_2)
		self.verticalLayout_3 = QtWidgets.QVBoxLayout()
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
		                                    QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(spacerItem3)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.option_Other = QtWidgets.QRadioButton(Dialog)
		self.option_Other.setObjectName("option_Other")
		self.horizontalLayout_2.addWidget(self.option_Other)
		self.other_edit = QtWidgets.QLineEdit(Dialog)
		self.other_edit.setObjectName("other_edit")
		self.horizontalLayout_2.addWidget(self.other_edit)
		self.verticalLayout_3.addLayout(self.horizontalLayout_2)
		self.option_idk = QtWidgets.QRadioButton(Dialog)
		self.option_idk.setObjectName("option_idk")
		self.verticalLayout_3.addWidget(self.option_idk)
		spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
		                                    QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(spacerItem4)
		self.horizontalLayout_3.addLayout(self.verticalLayout_3)
		self.verticalLayout_4.addLayout(self.horizontalLayout_3)
		self.error_label = QtWidgets.QLabel(Dialog)
		self.error_label.setAutoFillBackground(False)
		self.error_label.setStyleSheet("color: red")
		self.error_label.setObjectName("error_label")
		self.verticalLayout_4.addWidget(self.error_label)
		self.dialogButtons = QtWidgets.QDialogButtonBox(Dialog)
		self.dialogButtons.setOrientation(QtCore.Qt.Horizontal)
		self.dialogButtons.setStandardButtons(
			QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
		self.dialogButtons.setObjectName("dialogButtons")
		self.verticalLayout_4.addWidget(self.dialogButtons)
		self.horizontalLayout_6.addLayout(self.verticalLayout_4)
		spacerItem5 = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Expanding,
		                                    QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_6.addItem(spacerItem5)
		
		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.dialogButtons, QtCore.SIGNAL("accepted()"), Dialog.accept)
		QtCore.QObject.connect(self.dialogButtons, QtCore.SIGNAL("rejected()"), Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)
	
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
		self.title_label.setText(
			QtWidgets.QApplication.translate("Dialog", "Create a New Project", None, -1))
		self.name_label.setText(
			QtWidgets.QApplication.translate("Dialog", "Project Name", None, -1))
		self.description_label.setText(
			QtWidgets.QApplication.translate("Dialog", "Project Description", None, -1))
		self.project_folder_label.setText(
			QtWidgets.QApplication.translate("Dialog", "Project Folder", None, -1))
		self.browseFilesButton_folder.setText(
			QtWidgets.QApplication.translate("Dialog", "...", None, -1))
		self.application_label.setText(
			QtWidgets.QApplication.translate("Dialog", "Target Application", None, -1))
		self.browseFilesButton_executable.setText(
			QtWidgets.QApplication.translate("Dialog", "...", None, -1))
<<<<<<< HEAD
		self.label_4.setText(
			QtWidgets.QApplication.translate("Dialog",
			                                 "Which category does the target application best fit under?",
			                                 None, -1))
=======
		self.label_4.setText(QtWidgets.QApplication.translate("Dialog",
		                                                      "Which category does the target application best fit under?",
		                                                      None, -1))
>>>>>>> feature/MVPIntegration
		self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "WIN32", None, -1))
		self.option_MFC.setText(QtWidgets.QApplication.translate("Dialog", "MFC", None, -1))
		self.option_VB6.setText(QtWidgets.QApplication.translate("Dialog", "VB6", None, -1))
		self.option_VCL.setText(QtWidgets.QApplication.translate("Dialog", "VCL", None, -1))
		self.option_Legacy.setText(QtWidgets.QApplication.translate("Dialog", "Legacy", None, -1))
		self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Dialog", "UIA", None, -1))
		self.option_WinForms.setText(
			QtWidgets.QApplication.translate("Dialog", "WinForms", None, -1))
		self.option_WPF.setText(QtWidgets.QApplication.translate("Dialog", "WPF", None, -1))
		self.option_Qt5.setText(QtWidgets.QApplication.translate("Dialog", "Qt5", None, -1))
		self.option_Store_App.setText(
			QtWidgets.QApplication.translate("Dialog", "Store App", None, -1))
		self.option_Browser.setText(QtWidgets.QApplication.translate("Dialog", "Browser", None, -1))
		self.option_Other.setText(QtWidgets.QApplication.translate("Dialog", "Other", None, -1))
		self.option_idk.setText(
			QtWidgets.QApplication.translate("Dialog", "I don\'t know", None, -1))
		self.error_label.setText(QtWidgets.QApplication.translate("Dialog", "error:", None, -1))
