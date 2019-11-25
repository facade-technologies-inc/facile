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
from gui.facilegraphicsview import FacileGraphicsView
from data.project import Project
from data.tguim.component import Component
from tguiil.blinker import Blinker
from data.properties import Properties
from qt_models.propeditordelegate import PropertyEditorDelegate
from qt_models.projectexplorermodel import ProjectExplorerModel


class FacileView(QMainWindow):
	"""
	FacileView is the main window for Facile.
	"""
	
	# This signal will be emitted when the project changes to notify all components of Facile.
	projectChanged = Signal(Project)
	
	@unique
	class ExploreMode(Enum):
		MANUAL = 1
		AUTOMATIC = 2
		IGNORE = 3
	
	
	def __init__(self) -> 'FacileView':
		"""
		Constructs a FacileView object.
		
		:return: The new FacileView object
		:rtype: FacileView
		"""
		
		super(FacileView, self).__init__()
		self.ui = Ui_FacileView()
		self.ui.setupUi(self)
		self.ui.tempView.hide()
		self.ui.targetGUIModelView = FacileGraphicsView()
		self.ui.apiModelView = FacileGraphicsView()
		self.ui.viewSplitter.addWidget(self.ui.targetGUIModelView)
		self.ui.viewSplitter.addWidget(self.ui.apiModelView)
		
		self._blinker = None
		
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
		
		if project is not None:
			self.setWindowTitle("Facile - " + self._project.getMainProjectFile())
			print(self._project.getProjectDir())
			self.projectChanged.emit(project)
			self._project.save()
			self._project.addToRecents()
			self._project.getTargetGUIModel().getScene().itemSelected.connect(self._onItemSelected)
			self._project.getTargetGUIModel().getScene().itemBlink.connect(self._onItemBlink)
			self._project.getTargetGUIModel().dataChanged.connect(lambda: self.ui.projectExplorerView.update())
			self.ui.projectExplorerView.setModel(self._project.getProjectExplorerModel())
			self.ui.targetGUIModelView.setScene(self._project.getTargetGUIModel().getScene())
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
		self.ui.actionAutoExplore.triggered.connect(self._onAutomaticExploration)
		self.ui.actionManualExplore.triggered.connect(self._onManualExploration)
		self.ui.actionIgnoreExplore.triggered.connect(self._onIgnoreExploration)
	
	def _setEmptyModels(self) -> None:
		"""
		Puts empty models in all of the model-based views in Facile's main window The empty models just contain a
		message.
=

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
	
	@Slot(int)
	def _onItemSelected(self, id: int):
		"""
		This slot will update the view when an item is selected.
		
		:return: None
		"""
		# TODO: Change to get any entity instead of just component
		entity = self._project.getTargetGUIModel().getComponent(id)
		properties = entity.getProperties()
		self.ui.propertyEditorView.setModel(properties.getModel())
	
	
	@Slot(int)
	def _onItemBlink(self, id: int) -> None:
		"""
		Attempt to show an item in the GUI. Can only do this if the item is currently shown in
		the GUI.
		
		:param id: The ID of the component to show.
		:type id: int
		:return: None
		:rtype: NoneType
		"""
		component = self._project.getTargetGUIModel().getComponent(id)
		if self._blinker:
			self._blinker.stop()
		self._blinker = Blinker(self._project.getProcess().pid,
		                        self._project.getBackend(),
		                        component.getSuperToken())
		self._blinker.componentNotFound.connect(self.info)
		self._blinker.start()
	
	@Slot(bool)
	def _onManualExploration(self, checked: bool) -> None:
		"""
		Sets the exploration mode to be manual iff checked is True
		
		:param checked: if True, set the exploration mode to be manual. Else do nothing
		:type checked: bool
		:return: None
		:rtype: NoneType
		"""
		if checked:
			self._setExplorationMode(FacileView.ExploreMode.MANUAL)
	
	@Slot(bool)
	def _onAutomaticExploration(self, checked: bool) -> None:
		"""
		Sets the exploration mode to be automatic iff checked is True

		:param checked: if True, set the exploration mode to automatic. Else do nothing
		:type checked: bool
		:return: None
		:rtype: NoneType
		"""
		if checked:
			self._setExplorationMode(FacileView.ExploreMode.AUTOMATIC)
	
	@Slot(bool)
	def _onIgnoreExploration(self, checked: bool) -> None:
		"""
		Sets the exploration mode to be ignore iff checked is True

		:param checked: if True, set the exploration mode to be ignore. Else do nothing
		:type checked: bool
		:return: None
		:rtype: NoneType
		"""
		if checked:
			self._setExplorationMode(FacileView.ExploreMode.IGNORE)
		
	def _setExplorationMode(self, mode: 'FacileView.ExploreMode') -> None:
		"""
		Sets the exploration mode. If there is no project, or the target application is not running, nothing happens.
		
		:param mode: The mode to set exploration to.
		:type mode: FacileView.ExploreMode
		:return: None
		:rtyp: NoneType
		"""
		if self._project is None:
			return
		if self._project.getProcess() is None:
			return
		
		observer = self._project.getObserver()
		explorer = self._project.getExplorer()
		
		if mode == FacileView.ExploreMode.AUTOMATIC:
			self.ui.actionAutoExplore.setChecked(True)
			self.ui.actionManualExplore.setChecked(False)
			self.ui.actionIgnoreExplore.setChecked(False)
			observer.newSuperToken.connect(self._project.getTargetGUIModel().createComponent)
			observer.play()
			explorer.play()
		
		elif mode == FacileView.ExploreMode.MANUAL:
			self.ui.actionAutoExplore.setChecked(False)
			self.ui.actionManualExplore.setChecked(True)
			self.ui.actionIgnoreExplore.setChecked(False)
			observer.newSuperToken.connect(self._project.getTargetGUIModel().createComponent)
			observer.play()
			explorer.pause()
		
		elif mode == FacileView.ExploreMode.IGNORE:
			self.ui.actionAutoExplore.setChecked(False)
			self.ui.actionManualExplore.setChecked(False)
			self.ui.actionIgnoreExplore.setChecked(True)
			observer.pause()
			explorer.pause()

	@Slot(str, str)
	def info(self, title: str, message: str) -> None:
		"""
		This function displays an information message box. with the FacileView as the parent.
		
		:param title: The title of the window to show.
		:type title: str
		:param message: The message to show inside of the window
		:type message: str
		:return: None
		:rtype: NoneType
		"""
		QMessageBox.information(self, title, message)