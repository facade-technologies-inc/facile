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

This module contains the FacileView class which is the main window of Facile.
Much of Facile is joined together here.
"""
import os
from copy import deepcopy

from PySide2.QtCore import Slot, QTimer, QItemSelection
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, \
	QGraphicsOpacityEffect

from data.project import Project
from data.statemachine import StateMachine
from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior
from gui.copyprojectdialog import CopyProjectDialog
from gui.manageprojectdialog import ManageProjectDialog
from gui.newprojectdialog import NewProjectDialog
from gui.ui.ui_facileview import Ui_MainWindow as Ui_FacileView
from qt_models.projectexplorermodel import ProjectExplorerModel
from tguiil.blinker import Blinker
from gui.actionmenu import ActionMenu


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
		
		self._blinker = None
		
		#Action Menu Initialization
		self._componentActionMenu = ActionMenu()
		self._actionPipelinesMenu = ActionMenu()
		
		#Add labels for each tab on the Action Menu to the view
		self._componentActionMenu.setLabelText("Actions for current selected component.")
		self._actionPipelinesMenu.setLabelText("All user-defined actions.")
		
		#Add Action Menu Tabs to the view
		self.ui.actionMenuTabWidget.addTab(self._componentActionMenu, "Component Actions")
		self.ui.actionMenuTabWidget.addTab(self._actionPipelinesMenu, "Action Pipelines")
		self.ui.actionMenuTabWidget.removeTab(0)
		
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
						msg.setInformativeText(
							"Please choose a directory that does not already contain a project.")
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
		
		A file dialog is open with the .fcl filter. Once the user selects a project, it will be loaded into Facile.
		
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
		This slot is run when the user selects "file -> project settings"
		
		:return: None
		:rtype: NoneType
		"""
		
		manageProjectDialog = ManageProjectDialog(self._project)
		manageProjectDialog.projectCreated.connect(self.setProject)
		manageProjectDialog.exec_()
	
	@Slot()
	def onAddBehaviorTriggered(self) -> None:
		"""
		This slot is run when the user selects "Add Behavior"
		
		:return: None
		:rtype: NoneType
		"""
		self._stateMachine.addBehaviorClicked()
	
	@Slot()
	def onProjectExplorerIndexSelected(self, selected: QItemSelection,
	                                   deselected: QItemSelection) -> None:
		"""
		This slot is called when an item is selected in the project explorer.
		
		:param selected: The newly selected items
		:type selected: QItemSelection
		:param deselected: The items that used to be selected.
		:type deselected: QItemSelection
		:return: None
		:rtype: NoneType
		"""
		selectedIndexes = selected.indexes()
		index = selectedIndexes[0]
		entity = index.internalPointer()
		if not isinstance(entity, (ProjectExplorerModel.LeafIndex, str)):
			self._project.getTargetGUIModel().getScene().clearSelection()
			entity.getGraphicsItem().setSelected(True)
			self.ui.propertyEditorView.setModel(entity.getProperties().getModel())
			self.ui.propertyEditorView.expandAll()
	
	def onStartAppTriggered(self):
		"""
		This slot is run when the user selects "Start App"
		
		:return: None
		:rtype: NoneType
		"""
		self._project.startTargetApplication()
		self._stateMachine.startApp()
	
	@Slot()
	def onStopAppTriggered(self, confirm=True):
		"""
		This slot is run when the user selects "Stop App"

		:return: None
		:rtype: NoneType
		"""
		if confirm:
			title = "Confirm Application Termination"
			message = "Are you sure you'd like to terminate the target application?"
			response = QMessageBox.question(self, title, message)
		else:
			response = QMessageBox.StandardButton.Yes
		
		if response == QMessageBox.StandardButton.Yes:
			self._project.stopTargetApplication()
			self._stateMachine.stopApp()
			self.info("The target application has been\nterminated.")
	
	@Slot(int)
	def onItemSelected(self, id: int) -> None:
		"""
		This slot will update the view when an item is selected.
		
		:return: None
		:rtype: NoneType
		"""
		entity = self._project.getTargetGUIModel().getEntity(id)
		properties = entity.getProperties()
		self.ui.propertyEditorView.setModel(properties.getModel())
		
		if type(entity) == Component:
			self.ui.projectExplorerView.model().selectComponent(entity)
			self._stateMachine.componentClicked(entity)
			
		elif type(entity) == VisibilityBehavior:
			self.ui.projectExplorerView.model().selectBehavior(entity)
	
	@Slot(int)
	def onItemBlink(self, id: int) -> None:
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
			self._stateMachine.startExploration(StateMachine.ExplorationMode.AUTO)
		else:
			self._stateMachine.stopExploration()
	
	@Slot(str, str)
	def info(self, message: str) -> None:
		"""
		This function will show a box with a message that will fade in and then out.

		:param message: The message to show inside of the window
		:type message: str
		:return: None
		:rtype: NoneType
		"""
		# QMessageBox.information(self, title, message)
		
		label = QLabel(self)
		windowWidth = self.width()
		windowHeight = self.height()
		labelWidth = 700
		labelHeight = 300
		label.setGeometry(windowWidth / 2 - labelWidth / 2,
		                  windowHeight / 3 - labelHeight / 2,
		                  labelWidth,
		                  labelHeight)
		label.show()
		style = "border: 3px solid red;" \
		        "border-radius:20px;" \
		        "background-color:#353535;" \
		        "color:#dddddd"
		label.setStyleSheet(style)
		label.setAlignment(Qt.AlignCenter)
		label.setText(message)
		
		fadeInTimer = QTimer()
		waitTimer = QTimer()
		fadeOutTimer = QTimer()
		
		waitTimer.setSingleShot(True)
		waitTimer.setInterval(1000)
		
		effect = QGraphicsOpacityEffect(label)
		label.setGraphicsEffect(effect)
		effect.setOpacity(0)
		
		def fadeIn():
			opacity = effect.opacity() + 0.01
			effect.setOpacity(opacity)
			
			if opacity >= 1:
				fadeInTimer.stop()
				waitTimer.start()
		
		def wait():
			fadeOutTimer.start(10)
		
		def fadeOut():
			opacity = effect.opacity() - 0.01
			effect.setOpacity(opacity)
			
			if opacity <= 0:
				fadeOutTimer.stop()
				label.hide()
		
		fadeInTimer.timeout.connect(fadeIn)
		waitTimer.timeout.connect(wait)
		fadeOutTimer.timeout.connect(fadeOut)
		fadeInTimer.start(10)
