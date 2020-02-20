"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This module contains the code for the copy project dialog.
"""
import sys
import os
from os.path import expanduser

from PySide2 import QtCore

import data.statemachine as sm

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QWidget, QButtonGroup, QApplication, QFileDialog
from gui.ui.ui_apicompilerdialog import Ui_Dialog as Ui_ApiCompilerDialog
from libs.bitness import getPythonBitness, isExecutable, appBitnessMatches, getExeBitness


class ApiCompilerDialog(QDialog):
	# TODO: make it un-selectable before a project is open
	def __init__(self, parent: QWidget = None):
		
		super(ApiCompilerDialog, self).__init__(parent)
		self.ui = Ui_ApiCompilerDialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Setup API Compiler")
		
		# disable file path editors
		self.ui.apiLocation.setEnabled(False)
		self.ui.interpreterLocation.setEnabled(False)
		self.ui.apiLocation.setText(sm.StateMachine.instance._project.getProjectDir())
		self.ui.interpreterLocation.setText(sys.executable)
		
		self.ui.browseFilesButton_folder.clicked.connect(self.browseForAPILocation)
		self.ui.browseFilesButton_folder_2.clicked.connect(self.browseForInterpreterLocation)
		
		self.ui.dialogButtons.accepted.connect(self.accept)
		self.ui.dialogButtons.rejected.connect(self.reject)
		
		self.ui.error_label.setText("")
	
	@Slot()
	def browseForAPILocation(self) -> None:
		if getPythonBitness() == 32:
			openDir = "C:/Program Files (x86)"
		else:
			openDir = "C:/Program Files"
		openDir = os.path.abspath(openDir)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.apiLocation.setText(url))
		fileDialog.exec_()
	
	@Slot()
	def browseForInterpreterLocation(self) -> None:
		if getPythonBitness() == 32:
			openDir = "C:/Program Files (x86)"
		else:
			openDir = "C:/Program Files"
		openDir = os.path.abspath(openDir)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.interpreterLocation.setText(url))
		fileDialog.exec_()
		
	@Slot()
	def accept(self):
		self.ui.error_label.setText("")
		errors = []
		interpExe = self.ui.interpreterLocation.text()
		
		# Check for valid target application executable
		if not interpExe:
			errors.append("Need to select target application executable")
		else:
			if not isExecutable(interpExe):
				errors.append("Target application must be an executable file.")
			elif not appBitnessMatches(interpExe):
				pyBit = getPythonBitness()
				appBit = getExeBitness(interpExe)
				errors.append(
					"{} bit Python cannot control {} bit application".format(pyBit, appBit))
		
		# if there are any errors, show them, then return.
		if len(errors) != 0:
			errMsg = "Errors:\n"
			for err in errors:
				errMsg += "\t" + err + "\n"
			self.ui.error_label.setText(errMsg)
			return
		
		# TODO: figure out why FindExecutable: There is no association for the file get printed
		print("apicompilerdialog accepted")
		return QDialog.accept(self)
		

if __name__ == "__main__":
	
	app = QApplication([])
	widget = ApiCompilerDialog()
	widget.show()

	sys.exit(app.exec_())