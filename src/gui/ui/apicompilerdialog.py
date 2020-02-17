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

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QWidget, QButtonGroup, QApplication
from gui.ui.ui_apicompilerdialog import Ui_Dialog as Ui_ApiCompilerDialog


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
		self.ui.compilerLocation.setEnabled(False)
		self.ui.interpreterLocatoin.setEnabled(False)
	
	@Slot()
	def _browseProjectFolders(self) -> None:
		pass
		# fileDialog = QFileDialog()
		# fileDialog.setFileMode(QFileDialog.Directory)
		# fileDialog.setDirectory(expanduser("~"))
		# fileDialog.fileSelected.connect(lambda url: self.ui.project_folder_edit.setText(url))
		# fileDialog.exec_()


if __name__ == "__main__":
	
	app = QApplication([])
	widget = ApiCompilerDialog()
	widget.show()

	sys.exit(app.exec_())