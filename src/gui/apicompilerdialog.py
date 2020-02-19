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
	
	def __init__(self, parent: QWidget = None):
		
		super(ApiCompilerDialog, self).__init__(parent)
		self.ui = Ui_ApiCompilerDialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Setup API Compiler")
		
		# # allow user to select folder to save project in
		# self.ui.browseFilesButton_folder.clicked.connect(self._browseProjectFolders)
		# self.ui.browseFilesButton_executable.clicked.connect(self._browseApplicationFile)
		
		# group all radio buttons together to make them mutually exclusive
		# TODO: change it to checkbox to allow user to select multiple doc type
		group = QButtonGroup()
		group.setExclusive(False)
		group.addButton(self.ui.docOptionDocx)
		group.addButton(self.ui.docOptionHtml)
		group.addButton(self.ui.docOptionPdf)
		
		# TODO: add component resolution options
		
		# disable file path editors
		self.ui.apiLocation.setEnabled(False)
		self.ui.interpreterLocation.setEnabled(False)
		self.ui.apiLocation.setText(sm.StateMachine.instance._project.getProjectDir())
		self.ui.interpreterLocation.setText(sys.executable)
		
		self.ui.browseFilesButton_folder.clicked.connect(self.browseForAPILocation)
		self.ui.browseFilesButton_folder_2.clicked.connect(self.browseForInterpreterLocation)
		
		self.ui.dialogButtons.accepted.connect(self.accept)
		self.ui.dialogButtons.rejected.connect(self.reject)
		
		# TODO: change the layout. Break the current vertical layout. Right click on the background and make a new layout on the entire dialog
	
	@Slot()
	def browseForAPILocation(self) -> None:
		# TODO: it should only allow user to open a folder
		if getPythonBitness() == 32:
			openDir = "C:/Program Files (x86)"
		else:
			openDir = "C:/Program Files"
		openDir = os.path.abspath(openDir)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
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
		# openDir = sys.executable
		# print(sys.executable)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.interpreterLocation.setText(url))
		fileDialog.exec_()
		
	@Slot()
	def accept(self):
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
		
		if len(errors) != 0:
			errMsg = "Errors:\n"
			for err in errors:
				errMsg += "\t" + err + "\n"
			print(errMsg)
			return
		
		# TODO: create error label later
		print("accepted")
		return QDialog.accept(self)
		

if __name__ == "__main__":
	
	app = QApplication([])
	widget = ApiCompilerDialog()
	widget.show()

	sys.exit(app.exec_())