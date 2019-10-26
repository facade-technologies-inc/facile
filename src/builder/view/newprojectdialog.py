"""
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
"""
import sys
from os.path import expanduser
from PySide2.QtWidgets import QDialog, QApplication, QFileDialog, QButtonGroup
from PySide2.QtCore import QUrl, Signal
from ui.ui_newprojectdialog import Ui_Dialog as Ui_NewProjectDialog


class NewProjectDialog(QDialog):
	
	# carry name, description, target Application executable, and backend
	create = Signal(str, str, str, str)
	
	def __init__(self, parent = None):
		super(NewProjectDialog, self).__init__(parent)
		self.ui = Ui_NewProjectDialog()
		self.ui.setupUi(self)
		
		# allow user to select folder to save project in
		self.ui.browseFilesButton.clicked.connect(self.browseFolders)
		
		# group all radio buttons together to make them mutually exclusive
		group = QButtonGroup()
		group.setExclusive(True)
		group.addButton(self.ui.option_Other)
		group.addButton(self.ui.option_idk)
		group.addButton(self.ui.option_Legacy)
		group.addButton(self.ui.option_MFC)
		group.addButton(self.ui.option_VB6)
		group.addButton(self.ui.option_VCL)
		group.addButton(self.ui.option_Browser)
		group.addButton(self.ui.option_Store_App)
		group.addButton(self.ui.option_WPF)
		group.addButton(self.ui.option_WinForms)
		group.buttonClicked.connect(self.onBackendChecked)
		self.radioBtnGroup = group
		
		# set default backend to unknown
		self.ui.option_idk.setChecked(True)
		self.ui.other_edit.setEnabled(False)
		
	def browseFolders(self):
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(expanduser("~"))
		
		fileDialog.urlSelected.connect(self.setURL)
		fileDialog.fileSelected.connect(self.setURL)
		
		fileDialog.exec_()
		
	def setURL(self, url):
		if isinstance(url, QUrl):
			url = url.toString()
		self.ui.filepath_edit.setText(url)
		
	def onBackendChecked(self, checkedButton):
		for btn in self.radioBtnGroup.buttons():
			if not btn is checkedButton:
				btn.setChecked(False)
				
		if checkedButton is self.ui.option_Other:
			self.ui.other_edit.setEnabled(True)
		else:
			self.ui.other_edit.setText("")
			self.ui.other_edit.setEnabled(False)
			
	def accept(self):
		if not self.ui.project_name_edit.text():
			pass    # show error message
		if not self.ui.description_edit.toPlainText():
			pass    # show error message
		if not self.ui.filepath_edit.text():
			pass    # show error message
		# if target app is not executable:
		# show error message
	
		if self.ui.option_Other.isChecked() and not self.ui.other_edit.text():
			pass # show error message
		
		# return if there are errors.
	
		return QDialog.accept(self)
		
				
		
		
		
if __name__ == "__main__":
	app = QApplication()
	
	dialog = NewProjectDialog()
	dialog.show()
	sys.exit(app.exec_())