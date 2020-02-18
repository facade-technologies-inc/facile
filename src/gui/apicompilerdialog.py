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

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QWidget, QButtonGroup, QApplication, QFileDialog
from gui.ui.ui_apicompilerdialog import Ui_Dialog as Ui_ApiCompilerDialog
from libs.bitness import getPythonBitness


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
		group = QButtonGroup()
		group.setExclusive(True)
		group.addButton(self.ui.docOptionDocx)
		group.addButton(self.ui.docOptionHtml)
		group.addButton(self.ui.docOptionPdf)
		
		# disable file path editors
		self.ui.apiLocation.setEnabled(False)
		self.ui.interpreterLocation.setEnabled(False)
		
		self.ui.browseFilesButton_folder.clicked.connect(self.browseForAPILocation)
		self.ui.browseFilesButton_folder_2.clicked.connect(self.browseForInterpreterLocation)
		
		#is it the right way to deal with ok and cancel button?
		self.ui.dialogButtons.clicked.connect(self.reject)
	
	@Slot()
	def browseForAPILocation(self) -> None:
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
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.interpreterLocation.setText(url))
		fileDialog.exec_()
		

if __name__ == "__main__":
	
	app = QApplication([])
	widget = ApiCompilerDialog()
	widget.show()

	sys.exit(app.exec_())