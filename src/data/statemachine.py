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

This module contains the StateMachine class which dictates which operations can
be done in Facile at any given time.
"""

from enum import Enum, auto
from PySide2.QtCore import Slot
from PySide2.QtGui import QStandardItem, QStandardItemModel, Qt
from gui.facilegraphicsview import FacileGraphicsView
from data.project import Project
import json


class StateMachine:
    """
    This is an event-driven state machine. The statemachine has a "tick" method
    which takes in an event. Depending on the current state and the event, the
    next event is decided. and some code associated with that state is executed.
    
    NOTE: As Facile grows, this class will too, so it's important to keep the
    code clean and modular as much as possible.
    """
    
    class State(Enum):
        WAIT_FOR_PROJECT = auto()
        MODEL_MANIPULATION = auto()
        ADDING_VB = auto()
        EXPLORATION = auto()
        
    class Event(Enum):
        FACILE_OPENED = auto()
        PROJECT_OPENED = auto()
        START_EXPLORATION = auto()
        STOP_EXPLORATION = auto()
        ADD_VB_CLICKED = auto()
        COMPONENT_CLICKED = auto()
        
    class ExplorationMode(Enum):
        AUTO = auto()
        MANUAL = auto()
        
    def __init__(self, facileView, curState: State = State.WAIT_FOR_PROJECT):
        
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
        
    def tick(self, event: Event, *args, **kwargs) -> None:
        """
        This function is responsible for determining the next state of Facile when
        an event takes place. If the state of Facile changes in response to the
        event,
        :param event:
        :return:
        """
        nextState = None
        
        if event == StateMachine.Event.FACILE_OPENED:
            nextState = StateMachine.State.WAIT_FOR_PROJECT
        
        
        elif event == StateMachine.Event.PROJECT_OPENED:
            nextState = StateMachine.State.MODEL_MANIPULATION
        
        
        elif event == StateMachine.Event.ADD_VB_CLICKED:
            if self.curState == StateMachine.State.MODEL_MANIPULATION:
                nextState = StateMachine.State.ADDING_VB
                
                
        elif event == StateMachine.Event.COMPONENT_CLICKED:
            if self.curState == StateMachine.State.ADDING_VB:
                self.vbComponents.append(args[0])
                if len(self.vbComponents) == 1:
                    nextState = StateMachine.State.ADDING_VB
                elif len(self.vbComponents) == 2:
                    #TODO: add visibility behavior
                    # self.view._project.getTargetGUIModel().addVisibilityBehavior()
                    self.vbComponents = []
                    nextState = StateMachine.State.MODEL_MANIPULATION
              
                    
        elif event == StateMachine.Event.START_EXPLORATION:
            if (self.curState == StateMachine.State.MODEL_MANIPULATION or
                self.curState == StateMachine.State.EXPLORATION):
                if self._project.getProcess():
                    nextState = StateMachine.State.EXPLORATION
                else:
                    # TODO: warn that target app is not running
                    pass
                
        elif event == StateMachine.Event.STOP_EXPLORATION:
            nextState = StateMachine.State.MODEL_MANIPULATION
                
        
        if nextState is not None:
            self.stateHandlers[nextState](event, self.curState, *args, **kwargs)
            self.curState = nextState
        

    ############################################################################
    # State Handlers - 1 for each state. Called when entering state.
    ############################################################################
    def _state_WAIT_FOR_PROJECT(self, event: Event, previousState: State, *args, **kwargs) -> None:
        # Just for simpler code in this function.
        v = self.view
        ui = self.view.ui
        
        # Set up the GUI
        ui.tempView.hide()
        ui.targetGUIModelView = FacileGraphicsView()
        ui.apiModelView = FacileGraphicsView()
        ui.viewSplitter.addWidget(ui.targetGUIModelView)
        ui.viewSplitter.addWidget(ui.apiModelView)

        v.setProject(None)
        
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
        
        # Create actions for recent projects
        try:
            recentProjects = Project.getRecents(limit=10)
        except json.JSONDecodeError as e:
            ui.menuRecent_Projects.addAction("Error loading recent projects.")
        else:
            if len(recentProjects) == 0:
                ui.menuRecent_Projects.addAction("No recent projects.")
            else:
                for proj in recentProjects[:10]:
                    action = ui.menuRecent_Projects.addAction(proj)
                    action.triggered.connect(v.onOpenRecentProject)
        
        # Connect Facile's actions (At least all of the ones that are static)
        ui.actionFrom_Scratch.triggered.connect(v.onNewProjectFromScratchTriggered)
        ui.actionFrom_Existing_Project.triggered.connect(v.onNewProjectFromExistingTriggered)
        ui.actionOpen_Project.triggered.connect(v.onOpenProjectTriggered)
        ui.actionSave_Project.triggered.connect(v.onSaveProjectTriggered)
        ui.actionSave_as.triggered.connect(v.onSaveProjectAsTriggered)
        ui.actionManage_Project.triggered.connect(v.onManageProjectTriggered)
        ui.actionAutoExplore.triggered.connect(v.onAutomaticExploration)
        ui.actionManualExplore.triggered.connect(v.onManualExploration)
        
        # Disable actions
        ui.actionSave_Project.setEnabled(False)
        ui.actionSave_as.setEnabled(False)
        ui.actionAutoExplore.setEnabled(False)
        ui.actionManualExplore.setEnabled(False)
        ui.actionDetailed_View.setEnabled(False)
        ui.actionShow_Behaviors.setEnabled(False)
        ui.actionAdd_Behavior.setEnabled(False)
    
    def _state_MODEL_MANIPULATION(self, event: Event, previousState: State, *args, **kwargs) -> None:
        # Just for simpler code in this function.
        v = self.view
        ui = self.view.ui
        p = self.view._project
        
        if event == StateMachine.Event.PROJECT_OPENED:
            v.setWindowTitle("Facile - " + self._project.getMainProjectFile())
            p.save()
            p.addToRecents()
            p.getTargetGUIModel().getScene().itemSelected.connect(v.onItemSelected)
            p.getTargetGUIModel().dataChanged.connect(lambda: ui.projectExplorerView.update())
            ui.projectExplorerView.setModel(v._project.getProjectExplorerModel())
            ui.targetGUIModelView.setScene(v._project.getTargetGUIModel().getScene())
            p.startTargetApplication()  # TODO: Remove this once application controls exist
            
        if previousState == StateMachine.State.EXPLORATION:
            self._project.getObserver().pause()
            self._project.getExplorer().pause()
        
        ui.actionSave_Project.setEnabled(True)
        ui.actionSave_as.setEnabled(True)
        ui.actionAutoExplore.setEnabled(True)
        ui.actionManualExplore.setEnabled(True)
        ui.actionDetailed_View.setEnabled(True)
        ui.actionShow_Behaviors.setEnabled(True)
        ui.actionAdd_Behavior.setEnabled(True)
    
    def _state_ADDING_VB(self, event: Event, previousState: State, *args, **kwargs) -> None:
        self.view.ui.actionAutoExplore.setEnabled(False)
        self.view.ui.actionManualExplore.setEnabled(False)
        self.view.ui.actionDetailed_View.setEnabled(True)
        self.view.ui.actionShow_Behaviors.setEnabled(True)
        self.view.ui.actionAdd_Behavior.setEnabled(True)
    
    def _state_EXPLORATION(self, event: Event, previousState: State, *args, **kwargs) -> None:
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
        self.view.ui.actionAdd_Behavior.setEnabled(False)
        
        
    ############################################################################
    # Slots (Entry points for other parts of Facile)
    ############################################################################
    @Slot()
    def addBehaviorClicked(self):
        self.tick(StateMachine.Event.ADD_VB_CLICKED)
        
    @Slot()
    def componentClicked(self, componentId: int):
        self.tick(StateMachine.Event.COMPONENT_CLICKED, componentId)
        
    @Slot()
    def facileOpened(self):
        self.tick(StateMachine.Event.FACILE_OPENED)
        
    @Slot()
    def projectOpened(self, project):
        self._project = project
        self.tick(StateMachine.Event.PROJECT_OPENED)
        
    @Slot()
    def startExploration(self, mode):
        self.tick(StateMachine.Event.START_EXPLORATION, mode=mode)
        
    @Slot()
    def stopExploration(self):
        self.tick(StateMachine.Event.STOP_EXPLORATION)
