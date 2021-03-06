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

from PySide2.QtCore import Slot, QTimer, QItemSelection, QThread, QSize, Signal
from PySide2.QtGui import Qt, QCloseEvent, QKeyEvent, QPalette, QColor
from PySide2.QtWidgets import (QMainWindow, QFileDialog, QLabel, QWidget, QMessageBox,
							   QGraphicsOpacityEffect, QProgressDialog, QApplication)

from data.project import Project
from data.statemachine import StateMachine
from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior
from data.apim.componentaction import ComponentAction
from data.apim.action import Action
from data.apim.port import Port
from gui.copyprojectdialog import CopyProjectDialog
from gui.manageprojectdialog import ManageProjectDialog
from gui.newprojectdialog import NewProjectDialog
from gui.validatorview import ValidatorView
from gui.ui.ui_facileview import Ui_MainWindow as Ui_FacileView
from qt_models.projectexplorermodel import ProjectExplorerModel
from qt_models.propeditormodel import PropModel
from tguiil.blinker import Blinker
from gui.actionmenu import ActionMenu
from graphics.apim.actiongraphics import ActionGraphics
from graphics.apim.actionwrappergraphics import ActionWrapperGraphics
from graphics.apim.portgraphics import PortGraphics

import data.statemachine as sm
import qtmodern.styles as styles
import pyautogui
import json
from enum import Enum
from gui.theme import Theme
from libs.logging import main_logger as logger
import QNotifications


class FacileView(QMainWindow):
	"""
	FacileView is the main window for Facile.
	"""

	# Allows notifications to be shown
	notify = Signal(str, str, int, bool, str)  # text to show, severity, duration, autohide, close button text

	class Layout(Enum):
		MODELS = 1
		ESSENTIALS = 2
		CLASSIC = 3
		ALL = 4
		CUSTOM = 5

	DEFAULT_THEMES = [Theme(styles.darkClassic),
					  Theme(styles.lightClassic),
					  Theme(styles.darkModern),
					  Theme(styles.lightModern),
					  Theme(styles.darkUltra),
					  Theme(styles.lightUltra)]

	# Possible message levels are: primary, success, info, warning, and danger
	NOTIF_LENGTH = 5000  # Time in ms to show a notification
	NOTIF_AUTOHIDE = False  # Automatically hide notifications on mouse hover
	NOTIF_BUTTON = ''  # Text for button to close the notification. Empty str is a good looking X
	
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

		# Set up variables
		self._theme = None  # Handled by the loadSettings function
		self.themeList = FacileView.DEFAULT_THEMES
		self._layout = FacileView.Layout.CLASSIC
		self._scrollBarsEnabled = False

		# Initialize variables
		self.screenSize = pyautogui.size()

		# Connect signals
		self.connectSignals()
		
		# Add validator view
		self.ui.validatorView = ValidatorView()
		self.ui.validatorDockWidget.setWidget(self.ui.validatorView)
		self.ui.validatorDockWidget.hide()  # Hide until validator button is pressed
		
		self._blinker = None
		
		# State label in status bar
		self.ui.stateLabel = QLabel("")
		self.ui.statusBar.addPermanentWidget(self.ui.stateLabel)
		
		# Action Menu Initialization
		self._componentActionMenu = ActionMenu()
		self._actionPipelinesMenu = ActionMenu()
		
		# Add labels for each tab on the Action Menu to the view
		self._componentActionMenu.setLabelText("Actions for current selected component.")
		self._actionPipelinesMenu.setLabelText("All user-defined actions.")
		
		# Add Action Menu Tabs to the view
		self.ui.actionMenuTabWidget.addTab(self._componentActionMenu, "Component Actions")
		self.ui.actionMenuTabWidget.addTab(self._actionPipelinesMenu, "Action Pipelines")
		self.ui.actionMenuTabWidget.removeTab(0)

		# Set sizes and alignments
		self.ui.actionMenuTabWidget.setMinimumWidth(.135*self.screenSize.width)  # So that tabs don't get compressed
		self.ui.toolBar.setIconSize(QSize(.048*self.screenSize.height, .055*self.screenSize.height))  # Fix big icons
		
		# State Machine Initialization
		self._stateMachine = StateMachine(self)
		self._stateMachine.facileOpened()

		self._layout = FacileView.Layout.CLASSIC
		self.loadSettings()

		self.notificationArea = self.setupNotificationArea()

		self.notify.emit("Welcome back!", 'primary', FacileView.NOTIF_LENGTH, FacileView.NOTIF_AUTOHIDE,
						 FacileView.NOTIF_BUTTON)

	def setupNotificationArea(self):
		"""
		Sets up the notification area for this dialog
		"""

		notificationArea = QNotifications.QNotificationArea(self, location='facileview', maxMessages=2)
		notificationArea.setEntryEffect('fadeIn', 200)
		notificationArea.setExitEffect('fadeOut', 300)
		self.notify.connect(notificationArea.display)
		return notificationArea

	def getCurrentTheme(self) -> Theme:
		"""
		Returns the current Theme

		:return: Current theme
		:rtype: Theme
		"""
		return self._theme
	
	def refreshAPIM(self) -> None:
		"""
		Clears the APIMGraphicsView scene and recreates it. Also refreshes the action menus.
		
		:return: None
		:rtype: NoneType
		"""
		self.ui.apiModelView.refresh()
		self._actionPipelinesMenu.refresh()
		self._componentActionMenu.refresh()
		
	def updateAPIMColors(self, apimColors):
		"""
		Updates the colors for the APIM.
		
		:param apimColors: The dictionary of APIM Colors
		:type apimColors: dict
		"""

		ActionGraphics.COLOR = apimColors['Action Pipeline']
		ActionWrapperGraphics.COLOR = apimColors['Action Wrapper']
		PortGraphics.INNER_COLOR = apimColors['Inside Port']
		PortGraphics.OUTER_COLOR = apimColors['Outside Port']
		ActionWrapperGraphics.TAG_BACKGROUND_COLOR = apimColors['Sequence Tag']

		self.refreshAPIM()
	
	def getLayout(self) -> Layout:
		"""
		Returns the current Theme

		:return: Current layout
		:rtype: Layout
		"""
		return self._layout
	
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

			self.notify.emit("Opened Project: " + project.getName(), 'primary', FacileView.NOTIF_LENGTH,
							 FacileView.NOTIF_AUTOHIDE, FacileView.NOTIF_BUTTON)
	
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
		self.loadProject(self.sender().text())
	
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
		fileDialog.fileSelected.connect(lambda url: self.loadProject(url))
		fileDialog.exec_()

	def loadProject(self, url:str) -> None:
		"""
		Loads an existing project into the GUI while displaying a progressbar.

		:param url: The file path to the *.fcl file for the project to load.
		:type url: str
		:return: None
		:rtype: NoneType
		"""

		self.thread = QThread()
		self.thread.setTerminationEnabled(True)

		numSteps = Project.getEntityCount(url)

		self.progress = QProgressDialog("Loading Project ...", "Cancel Loading", 0, numSteps, parent=self.parent())
		self.progress.setValue(0)
		self.progress.setModal(True)

		self.progress.moveToThread(self.thread)
		self.thread.start()

		def increment():
			self.progress.setValue(self.progress.value() + 1)

		def complete():
			self.progress.setValue(numSteps)
			self.thread.terminate()

			self._componentActionMenu.clearActions()
			self._actionPipelinesMenu.clearActions()

		proj = Project.load(url, onEntityCreation=increment, onCompletion=complete)
		self.setProject(proj)

		# add action pipelines to the menu/view
		for ap in proj.getAPIModel().getActionPipelines():
			self.addActionPipelineToMenu(ap)

		self.thread.deleteLater()

	@Slot()
	def onManageProjectTriggered(self) -> None:
		"""
		This slot is run when the user selects "file -> project settings"
		
		:return: None
		:rtype: NoneType
		"""
		
		manageProjectDialog = ManageProjectDialog(self._project, self)
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
	def onProjectExplorerIndexSelected(self, selected: QItemSelection, deselected: QItemSelection) -> None:
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

		if not selectedIndexes:
			return

		index = selectedIndexes[0]
		entity = index.internalPointer()
		if not isinstance(entity, (ProjectExplorerModel.LeafIndex, str)):
			scene = sm.StateMachine.instance.view.ui.targetGUIModelView.scene()
			scene.clearSelection()
			scene.getGraphics(entity).setSelected(True)
			self.ui.propertyEditorView.setModel(entity.getProperties().getModel())
			self.ui.propertyEditorView.expandAll()

		if isinstance(entity, Component) or isinstance(entity, VisibilityBehavior):
			self.ui.targetGUIModelView.smoothFocus(self.ui.targetGUIModelView.scene().getGraphics(entity))
	
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
		
		self.ui.actionPower_App.setChecked(True)
		if confirm:
			title = "Confirm Application Termination"
			message = "Are you sure you'd like to terminate the target application?"
			response = QMessageBox.question(self, title, message, buttons=QMessageBox.Yes | QMessageBox.Cancel)
		else:
			response = QMessageBox.StandardButton.Yes
		
		if response == QMessageBox.StandardButton.Yes:
			self.ui.actionPower_App.setChecked(True)
			self.notify.emit("The target application has been terminated.", 'danger', FacileView.NOTIF_LENGTH,
							 FacileView.NOTIF_AUTOHIDE, FacileView.NOTIF_BUTTON)
			self._project.stopTargetApplication()
			self._stateMachine.stopApp()
	
	@Slot(int)
	def onItemSelected(self, id: int) -> None:
		"""
		This slot will update the view when an item is selected.
		
		:return: None
		:rtype: NoneType
		"""
		entity = self._project.getTargetGUIModel().getEntity(id)
		self.onEntitySelected(entity)

	@Slot('Entity')
	def onEntitySelected(self, entity: 'Entity') -> None:
		properties = entity.getProperties()
		self.ui.propertyEditorView.setModel(properties.getModel())
		
		if type(entity) == Component:
			self.ui.projectExplorerView.model().selectComponent(entity)
			self._stateMachine.componentClicked(entity)
			
			# show all component actions in the component action menu
			cType = entity.getProperties().getProperty('Class Name')[1].getValue()
			specs = self._project.getAPIModel().getSpecifications(cType)
			self._componentActionMenu.clearActions()
			self.ui.actionMenuTabWidget.setCurrentWidget(self._componentActionMenu)
			for spec in specs:
				action = ComponentAction(entity, spec)
				self._componentActionMenu.addAction(action)
			
		elif type(entity) == VisibilityBehavior:
			self.ui.projectExplorerView.model().selectBehavior(entity)
			self.ui.propertyEditorView.expandAll()

		elif type(entity) == Port:
			self.ui.propertyEditorView.setModel(PropModel(entity.getProperties()))
			self.ui.propertyEditorView.expandAll()

		elif isinstance(entity, Action):
			self.ui.propertyEditorView.setModel(PropModel(entity.getProperties()))
			self.ui.propertyEditorView.expandAll()
	
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
		waitTimer.setInterval(3000)
		
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
	
	def closeEvent(self, event: QCloseEvent) -> None:
		"""
		Handles what happens when the user tries to quit the application.
		
		If there is a project open, ask them if they want to save their progress. We also give
		the option to not save or to cancel the closing of Facile.
		
		If a project is not open, ask them if they are sure they want to quit.
		
		:param event: The close event used to determine if the application should be closed or not.
		:type event: QCloseEvent
		:return: None
		:rtype: NoneType
		"""

		title = "Cancel confirmation..."
		if self._project:
			if self._project.autoCloseAppOnExit is None:
				if self._project.getProcess():
					message = "Your target application is still running. Close it automatically when Facile is closed?\n" \
							  "(This can always be changed later in settings)"
					options = QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
					result = QMessageBox.question(self, "App is running...", message, options)

					if result == QMessageBox.Yes:
						self._project.autoCloseAppOnExit = True
					else:
						self._project.autoCloseAppOnExit = False

					self._project.acaWarningShown = True

			message = "Would you like to save your project before exiting?"
			options = QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
			result = QMessageBox.question(self, title, message, options)
			event.ignore()
			
			if result == QMessageBox.Yes:
				self.onSaveProjectTriggered()
				
			if result != QMessageBox.Cancel:
				if self._project.autoCloseAppOnExit:
					self.onStopAppTriggered(confirm=False)

				for runner in [self._project.getObserver(), self._project.getExplorer()]:
					if runner:
						while runner.isPlaying(): # wait until the runner actually stops
							runner.setPlaying(False) # tell the runner to stop
						runner.terminate()

				event.accept()
				QApplication.instance().exit(0)
		else:
			message = "Are you sure you want to quit?"
			options = QMessageBox.Yes | QMessageBox.No
			result = QMessageBox.question(self, title, message, options)
			event.ignore()
			
			if result == QMessageBox.Yes:
				self.onSaveProjectTriggered()
				event.accept()
				QApplication.instance().exit(0)
	
	def keyPressEvent(self, event: QKeyEvent) -> None:
		"""
		Handles key presses for the main window.
		
		When the "Esc" key is pressed, we'll try to close Facile
		
		:param event: The event carrying the code of the key that was pressed.
		:type event: QKeyEvent
		:return: None
		:rtype: NoneType
		"""
		
		if event.key() == Qt.Key_Escape:
			self.close()
		event.accept()

	def addActionPipelineToMenu(self, ap: 'ActionPipeline'):
		"""
		Adds an action pipeline to the action pipeline menu, and sets it as the current one.

		:param ap: The action pipeline to add
		:type ap: ActionPipeline
		"""

		self._actionPipelinesMenu.addAction(ap)
		self.ui.actionMenuTabWidget.setCurrentWidget(self._actionPipelinesMenu)

	def setTheme(self, theme: Theme) -> None:
		"""
		Sets theme to the one that is input, does nothing if not a valid theme.

		:param theme: the theme to set
		:type theme: Theme
		"""

		theme.applyTo(self)

		for thm in self.themeList:
			if theme.getName() == thm.getName():
				self.themeList.remove(thm)
				break

		self.themeList.append(theme)
		self._theme = theme

	def saveSettings(self) -> None:
		"""
		Saves general settings for use between sessions.
		"""

		cwd = os.getcwd()
		tempDir = os.path.join(cwd, "temp")
		settingsFile = os.path.join(tempDir, "settings.json")

		settings = {'theme':       self._theme.getName(),
					'theme list':  [theme.asDict() for theme in self.themeList if theme.isCustom()],
					'layout':      self._layout.value,
					'scrollbars':  self._scrollBarsEnabled}

		if not os.path.exists(tempDir):
			os.mkdir(tempDir)

		with open(settingsFile, "w") as f:
			f.write(json.dumps(settings, indent=4))

	def loadSettings(self) -> None:
		"""
		Loads and applies general settings from local file
		"""

		try:
			with open(os.path.join(os.getcwd(), "temp", "settings.json"), "r") as f:
				settings = json.loads(f.read())

			self.setLayout(FacileView.Layout(settings['layout']))
			self.enableScrollBars(settings['scrollbars'])

			# Load custom themes
			self.themeList = FacileView.DEFAULT_THEMES
			for themeDict in settings['theme list']:
				thm = Theme.fromDict(themeDict)
				self.themeList.append(thm)

			for theme in self.themeList:
				if theme.getName() == settings['theme']:
					self.setTheme(theme)

		except (FileNotFoundError, IndexError, TypeError, KeyError) as e:  # For older versions of Facile
			logger.warning("Could not load settings. Expected if it's the first time loading an updated version, or if"
						   "the settings file was deleted. Otherwise, this is bad.")
			logger.exception(str(e))
			# Set the initial settings to classic theme, layout, and model colors
			self.setTheme(FacileView.DEFAULT_THEMES[0])
			self.themeList = FacileView.DEFAULT_THEMES
			self.setLayout(FacileView.Layout.CLASSIC)
			self.enableScrollBars(False)

	def enableScrollBars(self, enabled: bool = True):
		"""
		Enables or disables scrollbars in the graphicsViews

		:param enabled: whether to enable or disable them
		:type enabled: bool
		"""
		self._scrollBarsEnabled = enabled
		if not enabled:
			self.ui.targetGUIModelView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.ui.targetGUIModelView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.ui.apiModelView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.ui.apiModelView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		else:
			self.ui.targetGUIModelView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.ui.targetGUIModelView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.ui.apiModelView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.ui.apiModelView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

	def scrollBarsEnabled(self) -> bool:
		"""
		Returns whether or not the Model View scrollbars are enabled
		"""
		return self._scrollBarsEnabled

	def connectSignals(self) -> None:
		"""
		Connects extra signals for Facile, from menu and other general signals
		"""

		# View Menu - Layout Presets
		self.ui.actionModelsOnly.toggled.connect(self.showModelsOnly)
		self.ui.actionEssentials.toggled.connect(self.showEssentials)
		self.ui.actionClassic.toggled.connect(self.showClassic)
		self.ui.actionAll.toggled.connect(self.showAll)
		# TODO: Implement custom layout saving/applying

	def setLayout(self, layout: Layout):
		"""
		Sets and applies the current layout

		:param layout: Layout to set
		:type layout: Layout
		"""

		if layout == FacileView.Layout.CLASSIC:
			self.ui.actionClassic.setChecked(True)
		elif layout == FacileView.Layout.MODELS:
			self.ui.actionModelsOnly.setChecked(True)
		elif layout == FacileView.Layout.ESSENTIALS:
			self.ui.actionEssentials.setChecked(True)
		elif layout == FacileView.Layout.ALL:
			self.ui.actionAll.setChecked(True)
		elif layout == FacileView.Layout.CUSTOM:
			pass  # TODO: Implement custom layout saving/applying

	@Slot()
	def showModelsOnly(self):
		"""
		Shows only the 2 models
		"""
		if self.ui.actionModelsOnly.isChecked():
			# Move toolbar
			self.moveTBToLeft()

			# Uncheck other options
			self.ui.actionClassic.setChecked(False)
			self.ui.actionEssentials.setChecked(False)
			self.ui.actionAll.setChecked(False)

			# Perform Layout modifications
			self.ui.actionMenuDockWidget.hide()
			self.ui.propertyDockWidget.hide()
			self.ui.explorerDockWidget.hide()
			self.ui.validatorDockWidget.hide()

			# Disable currently selected layout, re-enable others
			self.ui.actionModelsOnly.setEnabled(False)
			self.ui.actionClassic.setEnabled(True)
			self.ui.actionAll.setEnabled(True)
			self.ui.actionEssentials.setEnabled(True)

			self._layout = FacileView.Layout.MODELS

	@Slot()
	def showClassic(self):
		"""
		Shows everything except the validator (unless called)
		"""

		if self.ui.actionClassic.isChecked():
			# Move toolbar
			self.moveTBToTop()

			# Uncheck other options
			self.ui.actionModelsOnly.setChecked(False)
			self.ui.actionEssentials.setChecked(False)
			self.ui.actionAll.setChecked(False)

			# Perform Layout modifications
			self.ui.actionMenuDockWidget.show()
			self.ui.propertyDockWidget.show()
			self.ui.explorerDockWidget.show()
			self.ui.validatorDockWidget.hide()

			# Disable currently selected layout, re-enable others
			self.ui.actionModelsOnly.setEnabled(True)
			self.ui.actionClassic.setEnabled(False)
			self.ui.actionAll.setEnabled(True)
			self.ui.actionEssentials.setEnabled(True)

			self._layout = FacileView.Layout.CLASSIC

	@Slot()
	def showEssentials(self):
		"""
		Shows only the two models and the action menu
		"""

		if self.ui.actionEssentials.isChecked():
			# Move toolbar
			self.moveTBToTop()

			# Uncheck other options
			self.ui.actionModelsOnly.setChecked(False)
			self.ui.actionClassic.setChecked(False)
			self.ui.actionAll.setChecked(False)

			# Perform Layout modifications
			self.ui.actionMenuDockWidget.show()
			self.ui.propertyDockWidget.hide()
			self.ui.explorerDockWidget.hide()
			self.ui.validatorDockWidget.hide()

			# Disable currently selected layout, re-enable others
			self.ui.actionModelsOnly.setEnabled(True)
			self.ui.actionClassic.setEnabled(True)
			self.ui.actionAll.setEnabled(True)
			self.ui.actionEssentials.setEnabled(False)

			self._layout = FacileView.Layout.ESSENTIALS

	@Slot()
	def showAll(self):
		"""
		Shows everything in GUI
		"""

		if self.ui.actionAll.isChecked():
			# Move toolbar
			self.moveTBToTop()

			# Uncheck other options
			self.ui.actionModelsOnly.setChecked(False)
			self.ui.actionEssentials.setChecked(False)
			self.ui.actionClassic.setChecked(False)

			# Perform Layout modifications
			self.ui.actionMenuDockWidget.show()
			self.ui.propertyDockWidget.show()
			self.ui.explorerDockWidget.show()
			self.ui.validatorDockWidget.show()

			# Disable currently selected layout, re-enable others
			self.ui.actionModelsOnly.setEnabled(True)
			self.ui.actionClassic.setEnabled(True)
			self.ui.actionAll.setEnabled(False)
			self.ui.actionEssentials.setEnabled(True)

			self._layout = FacileView.Layout.ALL

	def moveTBToLeft(self):
		"""
		Moves toolbar to left of screen
		"""
		toolbar = self.ui.toolBar
		self.removeToolBar(toolbar)
		self.addToolBar(Qt.LeftToolBarArea, toolbar)
		toolbar.show()
		self.ui.toolBar = toolbar

	def moveTBToTop(self):
		"""
		Moves toolbar to top of screen
		"""
		toolbar = self.ui.toolBar
		self.removeToolBar(toolbar)
		self.addToolBar(Qt.TopToolBarArea, toolbar)
		toolbar.show()
		self.ui.toolBar = toolbar

	def updateColors(self, tguim: dict, apimColors: dict):
		"""
		Updates the accent colors. Necessary for colors to persist through loading projects and closing/opening Facile.

		:param tguim: the dictionary of color settings for the tguim
		:type tguim: dict
		:param apimColors: the dictionary of color settings for the apim
		:type apimColors: dict
		"""

		self.ui.targetGUIModelView.updateColors(tguim['Base Color'], tguim['Is Flat'])
		self.updateAPIMColors(apimColors)

