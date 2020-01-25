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

This module contains the StateMachine class which dictates which operations can
be done in Facile at any given time.
"""

import json
from enum import Enum, auto

from PySide2.QtCore import Slot, QTimer
from PySide2.QtGui import QStandardItem, QStandardItemModel, Qt
from PySide2.QtWidgets import QGraphicsScene

import data.tguim.visibilitybehavior as vb
from gui.facilegraphicsview import FacileGraphicsView
from qt_models.propeditordelegate import PropertyEditorDelegate
from data.configvars import ConfigVars


class StateMachine:
	"""
	This is an event-driven state machine. The state machine has a "tick" method
	which takes in an event. Depending on the current state and the event, the
	next event is decided. and some code associated with that state is executed.
	
	Because only one state machine will exist at a time, it's relatively safe to
	keep the instance in a static variable that can be accessed anywhere in Facile.
	However, this means that the state machine shouldn't be stored anywhere long-term
	except in the FacileView - maybe not even there. To access the StateMachine
	instance, use the following:
	
	.. code-block:: python
		
		import data.statemachine as sm
		state_machine = sm.StateMachine.instance
	
	.. note::
		As Facile grows, this class will too, so it's important to keep the
		code clean and modular as much as possible.
	"""
	
	class State(Enum):
		WAIT_FOR_PROJECT = auto()
		MODEL_MANIPULATION = auto()
		ADDING_VB = auto()
		EXPLORATION = auto()
	
	class Event(Enum):
		UPDATE = auto()
		FACILE_OPENED = auto()
		PROJECT_OPENED = auto()
		START_EXPLORATION = auto()
		STOP_EXPLORATION = auto()
		ADD_VB_CLICKED = auto()
		COMPONENT_CLICKED = auto()
		START_APP = auto()
		STOP_APP = auto()
	
	class ExplorationMode(Enum):
		AUTO = auto()
		MANUAL = auto()
		
	# We can get the State machine instance from anywhere in the code using StateMachine.instance
	# NOTE: This is not supposed to act as a Singleton because we make new state machines
	#       whenever we open new project.
	instance = None
	
	def __init__(self, facileView, curState: State = State.WAIT_FOR_PROJECT):
		"""
		Constructs a State Machine object.
		
		:param facileView: The main GUI of Facile.
		:type facileView: FacileView
		:param curState: The initial state to start out at. Default to waiting for project.
		:type curState: State
		"""
		
		# used to enable/disable parts of GUI and access project and models.
		self.view = facileView
		self._project = None
		
		# used to create visibility behaviors
		self.vbComponents = []
		
		# used to determine exploration type
		self.explorationType = None
		
		self.curState = curState
		self.stateHandlers = {
			StateMachine.State.WAIT_FOR_PROJECT: self._state_WAIT_FOR_PROJECT,
			StateMachine.State.MODEL_MANIPULATION: self._state_MODEL_MANIPULATION,
			StateMachine.State.ADDING_VB: self._state_ADDING_VB,
			StateMachine.State.EXPLORATION: self._state_EXPLORATION
		}

		# Initialize configuration variables (that affect what gets displayed in the Facile GUI)
		self.configVars = ConfigVars()

		StateMachine.instance = self
	
	def tick(self, event: Event, *args, **kwargs) -> None:
		"""
		This function is responsible for determining the next state of Facile when
		an event takes place. If the state of Facile changes in response to the
		event, the state handler of the new state will be called.
		
		.. note::
			The state doesn't have to be changed to something different for the
			state handler to be called. The next state can be set to the current
			state to call the state handler again.
			
		.. note::
			This method mostly handles state transitions. It's best to keep the
			work of the state in the state handlers to maintain code modularity.
		
		:param event: The event that triggered the tick to occur
		:type event: StateMachine.Event
		:param args: Any arguments that should be passied into this method.
		:type args: list
		:param kwargs: Any keyword arguments that should be passed into this method.
		:type kwargs: dict
		:return: None
		:rtype: NoneType
		"""
		nextState = None
		
		# If an update event takes place, we just force the state handler to run again.
		if event == StateMachine.Event.UPDATE:
			nextState = self.curState
		
		# If the app was just started, we don't want to change the state, but we do want to
		# enable/disable the controls.
		elif event == StateMachine.Event.START_APP:
			self.view.ui.actionStart_App.setEnabled(False)
			self.view.ui.actionStop_App.setEnabled(True)
			self.view.appWatcher.start()
			if self.curState == StateMachine.State.MODEL_MANIPULATION:
				self.view.ui.actionManualExplore.setEnabled(True)
				self.view.ui.actionAutoExplore.setEnabled(True)
		
		# If the app was just terminated, we must leave the exploration state if we're in it and
		# we will toggle the app controls
		elif event == StateMachine.Event.STOP_APP:
			self.view.ui.actionStart_App.setEnabled(True)
			self.view.ui.actionStop_App.setEnabled(False)
			self.view.ui.actionManualExplore.setEnabled(False)
			self.view.ui.actionAutoExplore.setEnabled(False)
			if self.curState == StateMachine.State.EXPLORATION:
				nextState = StateMachine.State.MODEL_MANIPULATION
		
		
		# When Facile is opened, wait for a project to be opened
		elif event == StateMachine.Event.FACILE_OPENED:
			nextState = StateMachine.State.WAIT_FOR_PROJECT
		
		# When a propject is opened, allow the user to manipulate the models.
		elif event == StateMachine.Event.PROJECT_OPENED:
			nextState = StateMachine.State.MODEL_MANIPULATION
		
		# When the "Add Behavior" button is clicked, only go into the ADDING_VB state if we're
		# currently in the MODEL_MANIPULATION state.
		elif event == StateMachine.Event.ADD_VB_CLICKED:
			self.vbComponents = []
			if self.curState == StateMachine.State.ADDING_VB:
				nextState = StateMachine.State.MODEL_MANIPULATION
			
			if self.curState == StateMachine.State.MODEL_MANIPULATION:
				nextState = StateMachine.State.ADDING_VB
		
		# When a component is clicked, if we are in the ADDING_VB state, record the click. Once two
		# clicked components have been detected, create a visibility behavior and go to the
		# MODEL_MANIPULATION state.
		elif event == StateMachine.Event.COMPONENT_CLICKED:
			if self.curState == StateMachine.State.ADDING_VB:
				self.vbComponents.append(args[0])
				if len(self.vbComponents) == 1:
					nextState = StateMachine.State.ADDING_VB
				elif len(self.vbComponents) == 2:
					srcComp = self.vbComponents[0]
					destComp = self.vbComponents[1]
					tguim = self._project.getTargetGUIModel()
					newVB = vb.VisibilityBehavior(tguim, srcComp, destComp)
					self.view._project.getTargetGUIModel().addVisibilityBehavior(newVB)
					self.view.ui.projectExplorerView.update()
					self.view.ui.projectExplorerView.model().selectBehavior(newVB)
					nextState = StateMachine.State.MODEL_MANIPULATION
		
		
		# If the user has initiated exploration and the target application is running, go into the
		# EXPLORATION
		elif event == StateMachine.Event.START_EXPLORATION:
			if (self.curState == StateMachine.State.MODEL_MANIPULATION or
				self.curState == StateMachine.State.EXPLORATION):
				if self._project.getProcess():
					nextState = StateMachine.State.EXPLORATION
				else:
					self.view.info("To Start exploration, you must\n" \
					               "first be running the target application.")
					self.view.ui.actionManualExplore.setChecked(False)
					self.view.ui.actionAutoExplore.setChecked(False)
		
		# If we've been requested to stop exploration and we're in the exploration state, go to the
		# MODEL_MANIPULATION state
		elif event == StateMachine.Event.STOP_EXPLORATION:
			if self.curState == StateMachine.State.EXPLORATION:
				nextState = StateMachine.State.MODEL_MANIPULATION
		
		# Advance to the next state
		if nextState is not None:
			self.stateHandlers[nextState](event, self.curState, *args, **kwargs)
			print("State Change:", self.curState.name, "->", nextState.name)
			self.curState = nextState
	
	############################################################################
	# State Handlers - 1 for each state. Called when entering state.
	############################################################################
	def _state_WAIT_FOR_PROJECT(self, event: Event, previousState: State, *args, **kwargs) -> None:
		"""
		This is the state handler for the WAIT_FOR_PROJECT state.
		
		This method is responsible for completing the GUI setup. It should only be called once ever.
		
		:param event: The event that caused entrance to this state
		:type event: Event
		:param previousState: The state visited prior to entering this state.
		:type previousState: State
		:param args: Any additional arguments needed for this state.
		:type args: list
		:param kwargs: Any additional keyword arguments needed for this state.
		:type kwargs: dict
		:return: None
		:rtype: NoneType
		"""
		# Just for simpler code in this function.
		v = self.view
		ui = self.view.ui
		
		v.setProject(None)
		
		# Set up the GUI
		ui.tempView.hide()
		ui.targetGUIModelView = FacileGraphicsView()
		ui.apiModelView = FacileGraphicsView()
		ui.viewSplitter.addWidget(ui.targetGUIModelView)
		ui.viewSplitter.addWidget(ui.apiModelView)
		
		# create blank model to show that no project is open.
		blankProjectExplorer = QStandardItemModel()
		blankProjectExplorer.setHorizontalHeaderLabels([""])
		label = QStandardItem("No project is open.")
		label.setFlags(Qt.NoItemFlags)
		blankProjectExplorer.appendRow([label])
		ui.projectExplorerView.setModel(blankProjectExplorer)
		
		# create blank model to show that no item is selected.
		blankPropertiesModel = QStandardItemModel()
		blankPropertiesModel.setHorizontalHeaderLabels([""])
		label = QStandardItem("No model item is selected.")
		label.setFlags(Qt.NoItemFlags)
		blankPropertiesModel.appendRow([label])
		ui.propertyEditorView.setModel(blankPropertiesModel)
		
		# Create Timer for detecting app termination
		def tick() -> None:
			if not self._project.getProcess():
				self.view.appWatcher.stop()
				self.view.onStopAppTriggered(confirm=False)
		
		self.view.appWatcher = QTimer(self.view)
		self.view.appWatcher.timeout.connect(tick)
		self.view.appWatcher.setInterval(500)
		
		# Create actions for recent projects
		try:
			import data.project as proj
			recentProjects = proj.Project.getRecents(limit=10)
		except json.JSONDecodeError as e:
			ui.menuRecent_Projects.addAction("Error loading recent projects.")
		else:
			if len(recentProjects) == 0:
				ui.menuRecent_Projects.addAction("No recent projects.")
			else:
				for proj in recentProjects[:10]:
					action = ui.menuRecent_Projects.addAction(proj)
					action.triggered.connect(v.onOpenRecentProject)

		# Connecting the configVars' change signal to logic that will update the TGUIM View
		self.configVars.updateTGUIMView.connect(lambda: v.ui.targetGUIModelView.scene().invalidate(
			v.ui.targetGUIModelView.scene().sceneRect(), QGraphicsScene.ItemLayer))

		# Sync actions to their associated configuration variables (configVars).
		ui.actionShow_Behaviors.setChecked(self.configVars.showBehaviors)
		ui.actionShow_Token_Tags.setChecked(self.configVars.showTokenTags)

		# Connect Facile's actions (At least all of the ones that are static)
		ui.actionFrom_Scratch.triggered.connect(v.onNewProjectFromScratchTriggered)
		ui.actionFrom_Existing_Project.triggered.connect(v.onNewProjectFromExistingTriggered)
		ui.actionOpen_Project.triggered.connect(v.onOpenProjectTriggered)
		ui.actionSave_Project.triggered.connect(v.onSaveProjectTriggered)
		ui.actionSave_as.triggered.connect(v.onSaveProjectAsTriggered)
		ui.actionManage_Project.triggered.connect(v.onManageProjectTriggered)
		ui.actionAutoExplore.triggered.connect(v.onAutomaticExploration)
		ui.actionManualExplore.triggered.connect(v.onManualExploration)
		ui.actionAdd_Behavior.triggered.connect(v.onAddBehaviorTriggered)
		ui.actionStart_App.triggered.connect(v.onStartAppTriggered)
		ui.actionStop_App.triggered.connect(lambda: v.onStopAppTriggered(confirm=True))
		ui.actionShow_Behaviors.triggered.connect(self.configVars.setShowBehaviors)
		ui.actionShow_Token_Tags.triggered.connect(self.configVars.setShowTokenTags)

		# Disable actions
		ui.actionSave_Project.setEnabled(False)
		ui.actionSave_as.setEnabled(False)
		ui.actionAutoExplore.setEnabled(False)
		ui.actionManualExplore.setEnabled(False)
		ui.actionDetailed_View.setEnabled(False)
		ui.actionShow_Behaviors.setEnabled(False)
		ui.actionShow_Token_Tags.setEnabled(False)
		ui.actionAdd_Behavior.setEnabled(False)
		ui.actionStart_App.setEnabled(False)
		ui.actionStop_App.setEnabled(False)
		ui.actionManage_Project.setEnabled(False)
	
	def _state_MODEL_MANIPULATION(self, event: Event, previousState: State, *args,
	                              **kwargs) -> None:
		"""
		This is the state handler for the MODEL_MANIPULATION state.

		:param event: The event that caused entrance to this state
		:type event: Event
		:param previousState: The state visited prior to entering this state.
		:type previousState: State
		:param args: Any additional arguments needed for this state.
		:type args: list
		:param kwargs: Any additional keyword arguments needed for this state.
		:type kwargs: dict
		:return: None
		:rtype: NoneType
		"""
		# Just for simpler code in this function.
		v = self.view
		ui = self.view.ui
		p = self.view._project
		
		if event == StateMachine.Event.PROJECT_OPENED:
			v.setWindowTitle("Facile - " + self._project.getMainProjectFile())
			# p.save()
			p.addToRecents()
			p.getTargetGUIModel().getScene().itemSelected.connect(v.onItemSelected)
			p.getTargetGUIModel().getScene().itemBlink.connect(v.onItemBlink)
			p.getTargetGUIModel().dataChanged.connect(lambda: ui.projectExplorerView.update())
			projectExplorerModel = v._project.getProjectExplorerModel(ui.projectExplorerView)
			ui.projectExplorerView.setModel(projectExplorerModel)
			ui.projectExplorerView.selectionModel().selectionChanged.connect(v.onProjectExplorerIndexSelected)
			ui.projectExplorerView.setContextMenuPolicy(Qt.CustomContextMenu)
			ui.projectExplorerView.customContextMenuRequested.connect(projectExplorerModel.onContextMenuRequested)
			ui.propertyEditorView.setItemDelegate(PropertyEditorDelegate())
			ui.targetGUIModelView.setScene(v._project.getTargetGUIModel().getScene())
			ui.actionStop_App.setEnabled(False)
			ui.actionStart_App.setEnabled(True)
			ui.actionManage_Project.setEnabled(True)
		
		if previousState == StateMachine.State.EXPLORATION:
			o = self._project.getObserver()
			e = self._project.getExplorer()
			if o: o.pause()
			if e: e.pause()
		
		if self._project.getProcess():
			ui.actionAutoExplore.setEnabled(True)
			ui.actionManualExplore.setEnabled(True)
			ui.actionStop_App.setEnabled(True)
			ui.actionStart_App.setEnabled(False)
		else:
			ui.actionManualExplore.setEnabled(False)
			ui.actionAutoExplore.setEnabled(False)
			ui.actionStop_App.setEnabled(False)
			ui.actionStart_App.setEnabled(True)
		
		ui.actionSave_Project.setEnabled(True)
		ui.actionSave_as.setEnabled(True)
		ui.actionDetailed_View.setEnabled(True)
		ui.actionShow_Behaviors.setEnabled(True)
		ui.actionShow_Token_Tags.setEnabled(True)
		ui.actionAdd_Behavior.setEnabled(True)
		ui.actionManualExplore.setChecked(False)
		ui.actionAutoExplore.setChecked(False)
	
	def _state_ADDING_VB(self, event: Event, previousState: State, *args, **kwargs) -> None:
		"""
		This is the state handler for the ADDING_VB state.

		:param event: The event that caused entrance to this state
		:type event: Event
		:param previousState: The state visited prior to entering this state.
		:type previousState: State
		:param args: Any additional arguments needed for this state.
		:type args: list
		:param kwargs: Any additional keyword arguments needed for this state.
		:type kwargs: dict
		:return: None
		:rtype: NoneType
		"""
		self.view.ui.actionAutoExplore.setEnabled(False)
		self.view.ui.actionManualExplore.setEnabled(False)
		self.view.ui.actionDetailed_View.setEnabled(True)
		self.view.ui.actionShow_Behaviors.setEnabled(True)
		self.view.ui.actionShow_Token_Tags.setEnabled(True)
		self.view.ui.actionAdd_Behavior.setEnabled(True)
		self.view.ui.actionStart_App.setEnabled(True)
		self.view.ui.actionStop_App.setEnabled(True)
	
	def _state_EXPLORATION(self, event: Event, previousState: State, *args, **kwargs) -> None:
		"""
		This is the state handler for the EXPLORATION state.

		:param event: The event that caused entrance to this state
		:type event: Event
		:param previousState: The state visited prior to entering this state.
		:type previousState: State
		:param args: Any additional arguments needed for this state.
		:type args: list
		:param kwargs: Any additional keyword arguments needed for this state.
		:type kwargs: dict
		:return: None
		:rtype: NoneType
		"""
		mode = kwargs["mode"]
		explorer = self._project.getExplorer()
		observer = self._project.getObserver()
		
		if mode == StateMachine.ExplorationMode.AUTO:
			explorer.play()
			observer.play()
		elif mode == StateMachine.ExplorationMode.MANUAL:
			explorer.pause()
			observer.play()
		
		self.view.ui.actionAutoExplore.setEnabled(True)
		self.view.ui.actionManualExplore.setEnabled(True)
		self.view.ui.actionDetailed_View.setEnabled(True)
		self.view.ui.actionShow_Behaviors.setEnabled(True)
		self.view.ui.actionShow_Token_Tags.setEnabled(True)
		self.view.ui.actionAdd_Behavior.setEnabled(False)
		self.view.ui.actionStart_App.setEnabled(False)
		self.view.ui.actionStop_App.setEnabled(True)
	
	############################################################################
	# Slots (Entry points for other parts of Facile)
	############################################################################
	@Slot()
	def addBehaviorClicked(self) -> None:
		"""
		This method triggers the ADD_VB_CLICKED event in the state machine
		
		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.ADD_VB_CLICKED)
	
	@Slot()
	def componentClicked(self, component: 'Component') -> None:
		"""
		This method triggers the COMPONENT_CLICKED event in the state machine.
		
		:param component: The component that was clicked.
		:type component: Component
		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.COMPONENT_CLICKED, component)
	
	@Slot()
	def facileOpened(self) -> None:
		"""
		This method triggers the FACILE_OPENED event in the state machine

		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.FACILE_OPENED)
	
	@Slot()
	def projectOpened(self, project: 'Project') -> None:
		"""
		This method sets the project and triggers the PROJECT_OPENED event in the state machine

		:return: None
		:rtype: NoneType
		"""
		self._project = project
		self.tick(StateMachine.Event.PROJECT_OPENED)
	
	@Slot()
	def startExploration(self, mode) -> None:
		"""
		This method triggers the START_EXPLORATION event in the state machine

		:return: None
		:rtype: NoneType
		"""
		if mode == StateMachine.ExplorationMode.AUTO:
			self.view.ui.actionManualExplore.setChecked(False)
		elif mode == StateMachine.ExplorationMode.MANUAL:
			self.view.ui.actionAutoExplore.setChecked(False)
			
		self.tick(StateMachine.Event.START_EXPLORATION, mode=mode)
	
	@Slot()
	def stopExploration(self):
		"""
		This method triggers the STOP_EXPLORATION event in the state machine

		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.STOP_EXPLORATION)
	
	@Slot()
	def startApp(self):
		"""
		This method triggers the STOP_EXPLORATION event in the state machine

		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.START_APP)
	
	@Slot()
	def stopApp(self):
		"""
		This method triggers the STOP_EXPLORATION event in the state machine

		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.STOP_APP)
	
	@Slot()
	def update(self):
		"""
		This method triggers the UPDATE event in the state machine

		:return: None
		:rtype: NoneType
		"""
		self.tick(StateMachine.Event.UPDATE)
