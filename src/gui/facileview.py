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
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide2.QtCore import Signal, Slot
from gui.ui.ui_facileview import Ui_MainWindow as Ui_FacileView
from gui.newprojectdialog import NewProjectDialog
from gui.copyprojectdialog import CopyProjectDialog
from gui.manageprojectdialog import ManageProjectDialog
from data.project import Project
from qt_models.projectexplorermodel import ProjectExplorerModel


class FacileView(QMainWindow):
	"""
	FacileView is the main window for Facile.
	"""
	
	# This signal will be emitted when the project changes to notify all components of Facile.
	projectChanged = Signal(Project)
	
	def __init__(self) -> 'FacileView':
		"""
		Constructs a FacileView object.
		
		:return: The new FacileView object
		:rtype: FacileView
		"""
		
		super(FacileView, self).__init__()
		self.ui = Ui_FacileView()
		self.ui.setupUi(self)

		self._setProject(None)
		self._connectActions()
		self._setEmptyModels()
		
	@Slot(Project)
	def _setProject(self, project: Project) -> None:
		"""
		Sets the project object.
		
		:param project: The new Project object to set
		:type project: Project
		:return: None
		:rtype: NoneType
		"""
		
		self._project = project
		
		if not project is None:
			self.setWindowTitle("Facile - " + self._project.getMainProjectFile())
			print(self._project.getProjectDir())
			self.projectChanged.emit(project)
			self._project.save()
			self._project.addToRecents()
			self.ui.projectExplorerView.setModel(self._project.getProjectExplorerModel())
			self._project.startTargetApplication()
			
	def _connectActions(self) -> None:
		"""
		Connects actions in Facile's GUI to business logic. Actions may be triggered by
		clicking on the toolbar, menu bar, or something else.
		
		:return: None
		:rtype: NoneType
		"""
		
		self._populateRecents()
		
		self.ui.actionFrom_Scratch.triggered.connect(self._onNewProjectFromScratchTriggered)
		self.ui.actionFrom_Existing_Project.triggered.connect(self._onNewProjectFromExistingTriggered)
		self.ui.actionOpen_Project.triggered.connect(self._onOpenProjectTriggered)
		self.ui.actionSave_Project.triggered.connect(self._onSaveProjectTriggered)
		self.ui.actionSave_as.triggered.connect(self._onSaveProjectAsTriggered)
		self.ui.actionManage_Project.triggered.connect(self._onManageProjectTriggered)
		
	def _setEmptyModels(self) -> None:
		"""
		Puts empty models in all of the model-based views in Facile's main window The empty models just contain a
		message.

		:return: None
		:rtype: NoneType
		"""
		# create blank model to show that no project is open.
		blankProjectExplorer = QStandardItemModel()
		blankProjectExplorer.setHorizontalHeaderLabels([""])
		label = QStandardItem("No project is open.")
		label.setFlags(Qt.NoItemFlags)
		blankProjectExplorer.appendRow([label])
		self.ui.projectExplorerView.setModel(blankProjectExplorer)
		
		# create blank model to show that no item is selected.
		blankPropertiesModel = QStandardItemModel()
		blankPropertiesModel.setHorizontalHeaderLabels([""])
		label = QStandardItem("No model item is selected.")
		label.setFlags(Qt.NoItemFlags)
		blankPropertiesModel.appendRow([label])
		self.ui.propertyEditorView.setModel(blankPropertiesModel)
		
	def _populateRecents(self) -> None:
		"""
		Creates the recents dropdown menu by reading the recents file. If the recents file does not exist, the message
		"No recent projects." is shown. If there was a problem decoding the file, the message "Error loading recent
		projects." is shown.
		
		:return: None
		:rtype: NoneType
		"""
		try:
			recentProjects = Project.getRecents(limit=10)
			
		except json.JSONDecodeError as e:
			self.ui.menuRecent_Projects.addAction("Error loading recent projects.")
			
		else:
			if len(recentProjects) == 0:
				self.ui.menuRecent_Projects.addAction("No recent projects.")
			
			else:
				for proj in recentProjects[:10]:
					action = self.ui.menuRecent_Projects.addAction(proj)
					action.triggered.connect(self._onOpenRecentProject)
	
	@Slot()
	def _onSaveProjectAsTriggered(self) -> None:
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
			self._setProject(newProject)
			self._onSaveProjectTriggered()
		
		fileDialog = QFileDialog()
		fileDialog.setFileMode(QFileDialog.Directory)
		fileDialog.setDirectory(os.path.expanduser("~"))
		fileDialog.fileSelected.connect(handler)
		fileDialog.exec_()
	
	@Slot()
	def _onSaveProjectTriggered(self) -> None:
		"""
		This slot is run when the user saves the current project in Facile
		
		:return: None
		:rtype: NoneType
		"""
		
		if self._project is not None:
			self._project.save()
			
	@Slot()
	def _onNewProjectFromScratchTriggered(self) -> None:
		"""
		This slot is run when the user elects to create a new project from scratch.
		
		A NewProjectDialog is opened that allows the user to specify the target application,
		description, location, etc.
		
		:return: None
		:rtype: NoneType
		"""
		
		newProjectDialog = NewProjectDialog()
		newProjectDialog.projectCreated.connect(self._setProject)
		newProjectDialog.exec_()

	@Slot()
	def _onNewProjectFromExistingTriggered(self) -> None:
		"""
		This slot is run when the user elects to create a new project from an existing one.
		A CopyProjectDialog is opened that allows the user to specify the new location, name, and description.
		
		:return: None
		:rtype: NoneType
		"""
		
		copyProjectDialog = CopyProjectDialog()
		copyProjectDialog.projectCreated.connect(self._setProject)
		copyProjectDialog.exec_()
	
	@Slot()
	def _onOpenRecentProject(self) -> None:
		"""
		This slot is run when the user selects to open a recent project.
		
		:return: None
		:rtype: NoneType
		"""
		
		self._setProject(Project.load(self.sender().text()))
	
	@Slot()
	def _onOpenProjectTriggered(self) -> None:
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
		fileDialog.fileSelected.connect(lambda url: self._setProject(Project.load(url)))
		fileDialog.exec_()
		
	@Slot()
	def _onManageProjectTriggered(self) -> None:
		"""
		This slot is run when a the user selects "file -> project settings"
		
		:return: None
		:rtype: NoneType
		"""
		
		manageProjectDialog = ManageProjectDialog(self._project)
		manageProjectDialog.projectCreated.connect(self._setProject)
		manageProjectDialog.exec_()