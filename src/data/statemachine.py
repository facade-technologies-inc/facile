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
        PROJECT_OPENED = auto()
        EXPLORATION_SELECTED = auto()
        ADD_VB_CLICKED = auto()
        COMPONENT_CLICKED = auto()
        
    def __init__(self, facileView, curState: State = State.NO_PROJECT):
        
        # used to enable/disable parts of GUI and access project and models.
        self.view = facileView
        
        # used to create visibility behaviors
        self.vbComponents = []
        
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
        
        if event == StateMachine.Event.PROJECT_OPENED:
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
                    
        elif event == StateMachine.Event.EXPLORATION_SELECTED:
            if self.curState == StateMachine.State.MODEL_MANIPULATION:
                nextState = StateMachine.State.EXPLORATION
                
                
        #TODO: Handle more events
        
        if nextState is not None and nextState != self.curState:
            self.stateHandlers[nextState](self.curState)
            self.curState = nextState
        

    ############################################################################
    # State Handlers - 1 for each state. Called when entering state.
    ############################################################################
    def _state_WAIT_FOR_PROJECT(self, previousState: State) -> None:
        pass
    
    def _state_MODEL_MANIPULATION(self, previousState: State) -> None:
        pass
    
    def _state_ADDING_VB(self, previousState: State) -> None:
        pass
    
    def _state_EXPLORATION(self, previousState: State) -> None:
        pass
        
        
    ############################################################################
    # Slots (Entry points for other parts of Facile)
    ############################################################################
    @Slot()
    def addBehaviorClicked(self):
        self.tick(StateMachine.Event.ADD_VB_CLICKED)
        
    @Slot()
    def componentClicked(self, componentId: int):
        self.tick(StateMachine.Event.COMPONENT_CLICKED, componentId)
        
            
        