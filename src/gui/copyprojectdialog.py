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

import os
from copy import deepcopy
from os.path import expanduser

from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QFileDialog, QWidget

from data.project import Project
# uses this autogenerated python file to create dialog structure.
from gui.ui.ui_copyprojectdialog import Ui_Dialog as Ui_CopyProjectDialog


class CopyProjectDialog(QDialog):
	"""
	This class is used to create a new project from an existing one. It is a dialog that pops up
	and prompts the user to enter information about the project to copy and the project to be created.
	
	When the user enters information, the information will be checked for validity.
	If any information is not valid, the project will not be created and error messages will appear.
	"""
	
	# When a new project is successfully created, this signal will be emitted.
	# It carries the new project.
	projectCreated = Signal(Project)
	
	def __init__(self, parent: QWidget = None, oldProject: Project = None):
		"""
		Constructs a CopyProjectDialog object.
		
		:param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
		:type parent: PySide2.QtWidgets.QWidget
		:param oldProject: The project to copy. If None, the user can select the location of an existing project.
		:type oldProject: Project
		"""
		
		super(CopyProjectDialog, self).__init__(parent)
		self.ui = Ui_CopyProjectDialog()
		self.ui.setupUi(self)
		self.setWindowTitle("Copy Existing Project")
		
		# set the old project to copy from
		self._newProject = None
		if oldProject:
			self._setProject(oldProject)
		else:
			self._oldProject = None
		
		# allow user to select folder to save project in
		self.ui.oldBrowseBtn.clicked.connect(self._browseForExistingProject)
		self.ui.newBrowseBtn.clicked.connect(self._browseForNewProjectDir)
		
		# Remove error message originally
		self.ui.oldErrorLabel.setText("")
		self.ui.newErrorLabel.setText("")
		
		# disable widgets all widgets initially except old file browser.
		self.ui.oldPathEdit.setEnabled(False)
		self.ui.oldNameEdit.setEnabled(False)
		self.ui.oldAppEdit.setEnabled(False)
		self.ui.oldDescriptionEdit.setEnabled(False)
		self.ui.newPathEdit.setEnabled(False)
		self.ui.newNameEdit.setEnabled(False)
		self.ui.newAppEdit.setEnabled(False)
		self.ui.newDescriptionEdit.setEnabled(False)
		self.ui.newBrowseBtn.setEnabled(False)
	
	@Slot(Project)
	def _setOldProject(self, oldProject: Project) -> None:
		"""
		Sets the existing project that will be copied and fills/enables the appropriate fields in the dialog.
		
		:param oldProject: The project to copy from
		:type oldProject: Project
		:return: None
		:rtype: NoneType
		"""
		self._oldProject = oldProject
		self._newProject = deepcopy(self._oldProject)
		
		self.ui.oldPathEdit.setText(self._oldProject.getProjectDir())
		self.ui.oldNameEdit.setText(self._oldProject.getName())
		self.ui.oldAppEdit.setText(self._oldProject.getExecutableFile())
		self.ui.oldDescriptionEdit.setText(self._oldProject.getDescription())
		
		self.ui.newBrowseBtn.setEnabled(True)
		self.ui.newNameEdit.setEnabled(True)
		self.ui.newDescriptionEdit.setEnabled(True)
		
		self.ui.newPathEdit.setText("")
		self.ui.newNameEdit.setText(self._newProject.getName())
		self.ui.newAppEdit.setText(self._newProject.getExecutableFile())
		self.ui.newDescriptionEdit.setText(self._newProject.getDescription())
	
	@Slot(str)
	def _setNewProjectURL(self, url: str) -> None:
		"""
		Fills the text of the new project's location field

		:param url: The path to the *.fcl file of the existing project
		:type url: str
		:return: None
		:rtype: NoneType
		"""
		self._newProject.setProjectDir(url)
		self.ui.newPathEdit.setText(url)
	
	@Slot()
	def _browseForExistingProject(self) -> None:
		"""
		Opens a file dialog when the user clicks on the existing project's "..." button to choose an
		existing *.fcl file.
		
		:return: None
		:rtype: NoneType
		"""
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(expanduser("~"))
		fileDialog.setNameFilter("Facile Project File (*.fcl)")
		fileDialog.fileSelected.connect(lambda url: self._setOldProject(Project.load(url)))
		fileDialog.exec_()
	
	@Slot()
	def _browseForNewProjectDir(self) -> None:
		"""
		Opens a file dialog when the user clicks on the new project's "..." button to choose the directory
		for the new project.

		The file dialog will only show folders. If the user selects a folder that already has a project in
		it, an error message will appear when the user tries to copy.
		
		:return: None
		:rtype: NoneType
		"""
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(expanduser("~"))
		fileDialog.fileSelected.connect(self._setNewProjectURL)
		fileDialog.exec_()
	
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
		
		oldPath = self.ui.oldPathEdit.text()
		oldName = self.ui.oldNameEdit.text()
		oldDescription = self.ui.oldDescriptionEdit.toPlainText()
		oldExe = self.ui.oldAppEdit.text()
		newPath = self.ui.newPathEdit.text()
		newName = self.ui.newNameEdit.text()
		newDescription = self.ui.newDescriptionEdit.toPlainText()
		newExe = self.ui.newAppEdit.text()
		
		# clear error messages
		self.ui.oldErrorLabel.setText("")
		self.ui.newErrorLabel.setText("")
		
		# detect any errors
		oldErrors = []
		newErrors = []
		
		# check existing project for errors (as much as we can)
		if not self._oldProject:
			oldErrors.append("must select an existing project")
		
		# check new project details for errors
		if not newName:
			newErrors.append("new project must have a name")
		
		if not newDescription:
			newErrors.append("new project must have a description")
		
		if newExe != oldExe:
			newErrors.append("new project must use the same executable as the old project")
		if not newPath:
			newErrors.append("Must specify location of new project")
		else:
			isAlreadyProject = False
			for file in os.listdir(newPath):
				if file[-4:] == ".fcl":
					isAlreadyProject = True
					break
			if isAlreadyProject:
				newErrors.append(
					"The selected project directory already belongs to a different project. Please select another.")
		
		# if there are any errors, show them, then return.
		if len(newErrors) != 0:
			errMsg = "Errors:\n"
			for err in newErrors:
				errMsg += "\t" + err + "\n"
			self.ui.newErrorLabel.setText(errMsg)
		if len(oldErrors) != 0:
			errMsg = "Errors:\n"
			for err in oldErrors:
				errMsg += "\t" + err + "\n"
			self.ui.oldErrorLabel.setText(errMsg)
		
		# if there are no errors, create a new project, emit the projectCreated signal, and
		# call the super-class's accept method to perform the default behavior.
		if len(newErrors) == 0 and len(oldErrors) == 0:
			self._newProject.setName(newName)
			self._newProject.setDescription(newDescription)
			self._newProject.setProjectDir(newPath)
			self.projectCreated.emit(self._newProject)
			return QDialog.accept(self)
