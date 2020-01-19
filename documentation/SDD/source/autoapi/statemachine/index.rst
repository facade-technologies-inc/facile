:orphan:

:mod:`statemachine`
===================

.. py:module:: statemachine

.. autoapi-nested-parse::

   ..
           /------------------------------------------------------------------------------ |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
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



Module Contents
---------------


.. py:class:: StateMachine(facileView, curState: State = State.WAIT_FOR_PROJECT)

   This is an event-driven state machine. The state machine has a "tick" method
   which takes in an event. Depending on the current state and the event, the
   next event is decided. and some code associated with that state is executed.

   .. note::
           As Facile grows, this class will too, so it's important to keep the
           code clean and modular as much as possible.

   Constructs a State Machine object.

   :param facileView: The main GUI of Facile.
   :type facileView: FacileView
   :param curState: The initial state to start out at. Default to waiting for project.
   :type curState: State

   .. py:class:: State

      ..
         Bases: :class:`enum.Enum`

      .. attribute:: WAIT_FOR_PROJECT
         

         

      .. attribute:: MODEL_MANIPULATION
         

         

      .. attribute:: ADDING_VB
         

         

      .. attribute:: EXPLORATION
         

         


   .. py:class:: Event

      ..
         Bases: :class:`enum.Enum`

      .. attribute:: UPDATE
         

         

      .. attribute:: FACILE_OPENED
         

         

      .. attribute:: PROJECT_OPENED
         

         

      .. attribute:: START_EXPLORATION
         

         

      .. attribute:: STOP_EXPLORATION
         

         

      .. attribute:: ADD_VB_CLICKED
         

         

      .. attribute:: COMPONENT_CLICKED
         

         

      .. attribute:: START_APP
         

         

      .. attribute:: STOP_APP
         

         


   .. py:class:: ExplorationMode

      ..
         Bases: :class:`enum.Enum`

      .. attribute:: AUTO
         

         

      .. attribute:: MANUAL
         

         


   .. method:: tick(self, event: Event, *args, **kwargs)


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


   .. method:: _state_WAIT_FOR_PROJECT(self, event: Event, previousState: State, *args, **kwargs)


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


   .. method:: _state_MODEL_MANIPULATION(self, event: Event, previousState: State, *args, **kwargs)


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


   .. method:: _state_ADDING_VB(self, event: Event, previousState: State, *args, **kwargs)


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


   .. method:: _state_EXPLORATION(self, event: Event, previousState: State, *args, **kwargs)


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


   .. method:: addBehaviorClicked(self)


      This method triggers the ADD_VB_CLICKED event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: componentClicked(self, component: Component)


      This method triggers the COMPONENT_CLICKED event in the state machine.

      :param component: The component that was clicked.
      :type component: Component
      :return: None
      :rtype: NoneType


   .. method:: facileOpened(self)


      This method triggers the FACILE_OPENED event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: projectOpened(self, project: Project)


      This method sets the project and triggers the PROJECT_OPENED event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: startExploration(self, mode)


      This method triggers the START_EXPLORATION event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: stopExploration(self)


      This method triggers the STOP_EXPLORATION event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: startApp(self)


      This method triggers the STOP_EXPLORATION event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: stopApp(self)


      This method triggers the STOP_EXPLORATION event in the state machine

      :return: None
      :rtype: NoneType


   .. method:: update(self)


      This method triggers the UPDATE event in the state machine

      :return: None
      :rtype: NoneType



