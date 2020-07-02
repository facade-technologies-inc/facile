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

This module contains the code for the new project dialog.
"""

import os
from os.path import expanduser

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QFileDialog, QButtonGroup, QWidget, QRadioButton, QGroupBox

from data.project import Project
# uses this autogenerated python file to create dialog structure.
from gui.ui.ui_newprojectdialog import Ui_Dialog as Ui_NewProjectDialog
from libs.bitness import isExecutable, appBitnessMatches, getPythonBitness, getExeBitness


class NewProjectDialog(QDialog):
	"""
	This class is used to create a new project from scratch. It is a dialog that pops up
	and prompts the user to enter information about the project to be created.
	
	When the user enters information, the information will be checked for validity.
	If any information is not valid, the project will not be created and error messages will appear.
	"""
	
	# When a new project is successfully created, this signal will be emitted.
	# It carries the new project.
	projectCreated = Signal(Project)
	
	def __init__(self, parent: QWidget = None):
		"""
		Constructs a NewProjectDialog object.
		
		:param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
		:type parent: PySide2.QtWidgets.QWidget
		:return: The constructed new project dialog object.
		:rtype: NewProjectDialog
		"""
		
		super(NewProjectDialog, self).__init__(parent)
		self.ui = Ui_NewProjectDialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Create New Project")
		
		# allow user to select folder to save project in
		self.ui.browseFilesButton_folder.clicked.connect(self._browseProjectFolders)
		self.ui.browseFilesButton_executable.clicked.connect(self._browseApplicationFile)
		
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
		group.addButton(self.ui.option_Qt5)
		group.buttonClicked.connect(self._onBackendChecked)
		self._radioBtnGroup = group
		
		# set default backend to unknown
		self.ui.option_idk.setChecked(True)
		self.ui.other_edit.setEnabled(False)
		
		# Remove error message originally
		self.ui.error_label.setText("")
		
		# disable file path editors
		self.ui.executable_file_edit.setEnabled(False)
		self.ui.project_folder_edit.setEnabled(False)
	
	@Slot()
	def _browseProjectFolders(self) -> None:
		"""
		Opens a file dialog when the user clicks on the "..." button to choose a project directory.
		
		The user will only be able to select folders, and when a folder is selected, the value will
		be placed into the read-only text editor to the left. The user should not select a directory
		where a project already exists.
		
		:return: None
		:rtype: NoneType
		"""
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(expanduser("~"))
		fileDialog.fileSelected.connect(lambda url: self.ui.project_folder_edit.setText(url))
		fileDialog.exec_()
	
	@Slot()
	def _browseApplicationFile(self) -> None:
		"""
		Opens a file dialog when the user clicks on the "..." button to choose a target application.

		The dialog that pops up doesn't restrict what file the user selects, but before creating the
		project, the file will be checked for correct bitness, and to make sure that it's an executable file.
		The path to the file will be placed into the read-only text editor to the left.
		
		:return: None
		:rtype: NoneType
		"""
		
		# determine which programs directory to open based on the bitness of Facile.
		if getPythonBitness() == 32:
			openDir = "C:/Program Files (x86)"
		else:
			openDir = "C:/Program Files"
		openDir = os.path.abspath(openDir)
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(openDir)
		fileDialog.fileSelected.connect(lambda url: self.ui.executable_file_edit.setText(url))
		fileDialog.exec_()
	
	@Slot(QRadioButton)
	def _onBackendChecked(self, checkedButton: QRadioButton) -> None:
		"""
		Unchecks all of the backend radio buttons except the button that was passed in.
		
		If the button that was passed in is anything but the "other" button, clear the
		text field next to the "other" radio button.
		
		:param checkedButton: The radio button that was just clicked.
		:type checkedButton: QRadioButton
		:return: None
		:rtype: NoneType
		"""
		
		for btn in self._radioBtnGroup.buttons():
			if not btn is checkedButton:
				btn.setChecked(False)
		
		if checkedButton is self.ui.option_Other:
			self.ui.other_edit.setEnabled(True)
		else:
			self.ui.other_edit.setText("")
			self.ui.other_edit.setEnabled(False)
	
	@Slot()
	def accept(self) -> None:
		"""
		This method is called when the user clicks the "OK" button.
		
		It will validate all of the user's input and show error messages if
		any information is invalid.
		
		:emits: projectCreated if a project was successfully created
		:return: None
		:rtype: NoneType
		"""
		
		name = self.ui.project_name_edit.text().strip()
		description = self.ui.description_edit.toPlainText().strip()
		projectDir = self.ui.project_folder_edit.text().strip()
		appExe = self.ui.executable_file_edit.text().strip()
		
		# clear error message
		self.ui.error_label.setText("")
		
		# detect any errors
		errors = []
		if not name:
			errors.append("Need project name")
		if not name.replace(" ", "_").isidentifier():
			errors.append("The project name may only contain alphanumeric characters and spaces and cannot begin with a number.")
		if not description:
			errors.append("Need project description")
		
		# Check for valid project directory.
		if not projectDir:
			errors.append("Need to select project folder")
		else:
			isAlreadyProject = False
			for file in os.listdir(projectDir):
				if file[-4:] == ".fcl":
					isAlreadyProject = True
					break
			
			if isAlreadyProject:
				errors.append(
					"The selected project directory already belongs to a different project. Please select another.")
		
		# Check for valid target application executable
		if not appExe:
			errors.append("Need to select target application executable")
		else:
			if not isExecutable(appExe):
				errors.append("Target application must be an executable file.")
			elif not appBitnessMatches(appExe):
				pyBit = getPythonBitness()
				appBit = getExeBitness(appExe)
				errors.append(
					"{} bit Python cannot control {} bit application".format(pyBit, appBit))
		
		# Check for valid framework
		frameworkOption = self._radioBtnGroup.checkedButton()
		framework = frameworkOption.text()
		if frameworkOption == self.ui.option_Other:
			framework = self.ui.other_edit.text()
		if not framework:
			errors.append("Must specify which framework is being used")
		
		# check for valid backend
		backendWidget = frameworkOption.parentWidget()
		if isinstance(backendWidget, QGroupBox):
			backend = backendWidget.title()
		else:
			backend = "auto"  # Auto selection is used for both IDK and Other options
		
		# if there are any errors, show them, then return.
		if len(errors) != 0:
			errMsg = "Errors:\n"
			for err in errors:
				errMsg += "\t" + err + "\n"
			self.ui.error_label.setText(errMsg)
			return
		
		# if there are no errors, create a new project, emit the projectCreated signal, and
		# call the super-class's accept method to perform the default behavior.
		else:
			newProject = Project(name, description, appExe, backend, projectDir=projectDir)
			self.projectCreated.emit(newProject)
			return QDialog.accept(self)
