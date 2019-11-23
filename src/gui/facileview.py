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

This module contains the FacileView class which is the main window of Facile.
Much of Facile is joined together here.
"""
import os
import json
from copy import deepcopy
from enum import Enum, unique
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide2.QtCore import Signal, Slot
from gui.ui.ui_facileview import Ui_MainWindow as Ui_FacileView
from gui.newprojectdialog import NewProjectDialog
from gui.copyprojectdialog import CopyProjectDialog
from gui.manageprojectdialog import ManageProjectDialog
from data.project import Project
from data.statemachine import StateMachine


class FacileView(QMainWindow):
	"""
	FacileView is the main window for Facile.
	"""
	
	def __init__(self) -> 'FacileView':
		"""
		Constructs a FacileView object.
		
		:return: The new FacileView object
		:rtype: FacileView
		"""
		super(FacileView, self).__init__()
		
		# UI Initialization
		self.ui = Ui_FacileView()
		self.ui.setupUi(self)
		
		# State Machine Initialization
		self._stateMachine = StateMachine(self)
		self._stateMachine.facileOpened()
		
	@Slot(Project)
	def setProject(self, project: Project) -> None:
		"""
		Sets the project object.
		
		:param project: The new Project object to set
		:type project: Project
		:return: None
		:rtype: NoneType
		"""
		
		self._project = project
		
		if project is not None:
			self._stateMachine.projectOpened(project)
	
	@Slot()
	def onSaveProjectAsTriggered(self) -> None:
		"""
		This slot is run when the user clicks "File -> Save As..."
		
		:return: None
		:rtype: NoneType
		"""
		
		def handler(url: str) -> None:
			"""
			This function is called when the user selects the new directory to save the project in.
			
			:return: None
			:rtype: NoneType
			"""
			
			if os.path.normpath(url) != os.path.normpath(self._project.getProjectDir()):
				for file in os.listdir(url):
					if file[-4:] == ".fcl":
						msg = QMessageBox()
						msg.setIcon(QMessageBox.Critical)
						msg.setText("Error")
						msg.setInformativeText("Please choose a directory that does not already contain a project.")
						msg.setWindowTitle("Error")
						msg.exec_()
						return
			
			newProject = deepcopy(self._project)
			newProject.setProjectDir(url)
			self.setProject(newProject)
			self.onSaveProjectTriggered()
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(os.path.expanduser("~"))
		fileDialog.fileSelected.connect(handler)
		fileDialog.exec_()
	
	@Slot()
	def onSaveProjectTriggered(self) -> None:
		"""
		This slot is run when the user saves the current project in Facile
		
		:return: None
		:rtype: NoneType
		"""
		
		if self._project is not None:
			self._project.save()
			
	@Slot()
	def onNewProjectFromScratchTriggered(self) -> None:
		"""
		This slot is run when the user elects to create a new project from scratch.
		
		A NewProjectDialog is opened that allows the user to specify the target application,
		description, location, etc.
		
		:return: None
		:rtype: NoneType
		"""
		
		newProjectDialog = NewProjectDialog()
		newProjectDialog.projectCreated.connect(self.setProject)
		newProjectDialog.exec_()

	@Slot()
	def onNewProjectFromExistingTriggered(self) -> None:
		"""
		This slot is run when the user elects to create a new project from an existing one.
		A CopyProjectDialog is opened that allows the user to specify the new location, name, and description.
		
		:return: None
		:rtype: NoneType
		"""
		
		copyProjectDialog = CopyProjectDialog()
		copyProjectDialog.projectCreated.connect(self.setProject)
		copyProjectDialog.exec_()
	
	@Slot()
	def onOpenRecentProject(self) -> None:
		"""
		This slot is run when the user selects to open a recent project.
		
		:return: None
		:rtype: NoneType
		"""
		
		self.setProject(Project.load(self.sender().text()))
	
	@Slot()
	def onOpenProjectTriggered(self) -> None:
		"""
		This slot is run when the user elects to open an existing project.
		
		A file dialog is open with the *.fcl filter. Once the user selects a project, it will be loaded into Facile.
		
		:return: None
		:rtype: NoneType
		"""
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		fileDialog.setDirectory(os.path.expanduser("~"))
		fileDialog.setNameFilter("Facile Project File (*.fcl)")
		fileDialog.fileSelected.connect(lambda url: self.setProject(Project.load(url)))
		fileDialog.exec_()
		
	@Slot()
	def onManageProjectTriggered(self) -> None:
		"""
		This slot is run when a the user selects "file -> project settings"
		
		:return: None
		:rtype: NoneType
		"""
		
		manageProjectDialog = ManageProjectDialog(self._project)
		manageProjectDialog.projectCreated.connect(self.setProject)
		manageProjectDialog.exec_()
		
	@Slot(int)
	def onItemSelected(self, id: int):
		"""
		This slot will update the view when an item is selected.
		
		:return: None
		"""
		# TODO: Change to get any entity instead of just component
		properties = self._project.getTargetGUIModel().getComponent(id).getProperties()
		self.ui.propertyEditorView.setModel(properties.getModel())
		
	@Slot(bool)
	def onManualExploration(self, checked: bool) -> None:
		"""
		Sets the exploration mode to be manual iff checked is True
		
		:param checked: if True, set the exploration mode to be manual. Else leave exploration.
		:type checked: bool
		:return: None
		:rtype: NoneType
		"""
		if checked:
			self._stateMachine.startExploration(StateMachine.ExplorationMode.MANUAL)
		else:
			self._stateMachine.stopExploration()
	
	@Slot(bool)
	def onAutomaticExploration(self, checked: bool) -> None:
		"""
		Sets the exploration mode to be automatic iff checked is True

		:param checked: if True, set the exploration mode to automatic. Else leave exploration.
		:type checked: bool
		:return: None
		:rtype: NoneType
		"""
		if checked:
			self._stateMachine.startExploration(StateMachine.ExplorationMode.AUTOMATIC)
		else:
			self._stateMachine.stopExploration()
