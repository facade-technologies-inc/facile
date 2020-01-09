:orphan:

:mod:`observer`
===============

.. py:module:: observer

.. autoapi-nested-parse::

   ..
       /------------------------------------------------------------------------------    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
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

   This module contains the Observer class, which watches the target GUI for changes.



Module Contents
---------------


.. py:class:: Observer(processID: int, backend: str = 'uia')

   Bases: :class:`PySide2.QtCore.QThread`
   .. inheritance-diagram:: observer.Observer

   The observer continually traverses the target GUI and notifies when new components are found.
   It maintains a tree of super tokens to determine whether a component has already been found or not.

   To use:
           process = psutil.Popen(["C:\Program Files\Notepad++\notepad++.exe"])
           observer = Observer(process.pid, 'uia')
           observer.newSuperToken.connect(targetGUIModel.addSuperToken)
           observer.start()

   Constructs an Observer. The target application must already be started before constructing the Observer.

   :raises: NoSuchProcess
   :raises: AccessDenied
   :param processID: The ID of the process to watch.
   :type processID: int
   :return: None
   :rtype: NoneType

   .. attribute:: newSuperToken
      

      

   .. attribute:: ignoreTypes
      

      

   .. method:: loadSuperTokens(self, tguim: TargetGuiModel)


      Loads existing super tokens into the observer to avoid duplication of super tokens.

      This method will iterate over all components in the target GUI model and extract the
      SuperToken references. It will build the simple of super tokens internally using
      dictionaries.

      This method is vital because when a new observer is created, it needs to know about
      existing super tokens to avoid duplication.

      .. note::
              This method should be run in Facile's main thread BEFORE the observer is played.

      :param tguim: The target GUI model to load the super tokens from.
      :type tguim: TargetGuiModel
      :return: None
      :rtype: NoneType


   .. method:: run(self)


      DO NOT CALL THIS METHOD. This method is run in a new thread when the start() method is called.

      :return: the exit code of the thread which should be 0.
      :rtype: int


   .. method:: createToken(timeStamp: datetime, component: pywinauto.base_wrapper.BaseWrapper)
      :staticmethod:


      Create a token from a pywinauto control.

      :raises: Token.CreationException

      :param timeStamp: The time that the application instance was created.
      :type timeStamp: datetime
      :param component: A pywinauto control from the target GUI.
      :type component: pywinauto.base_wrapper
      :return: The token that was created from the pywinauto control.
      :rtype: Token


   .. method:: matchToSuperToken(self, token: Token, parentSuperToken: SuperToken)


      Gets the SuperToken that best matches the given token.

      The parentSuperToken is necessary in the case that a new SuperToken is created. In this
      case, both the new SuperToken and its parent will be carried in the newSuperToken signal
      which will be emitted.

      Having the parent super token also allows us to reduce the search space when finding the
      matched SuperToken.

      :param token: The token to find a SuperToken match with.
      :type token: Token
      :param parentSuperToken: The parent of the SuperToken that will be matched with the token.
      :type parentSuperToken: SuperToken
      :return: The SuperToken that gets matched to the provided token.
      :rtype: SuperToken


   .. method:: setPlaying(self, status: bool)


      Sets the running flag.
      :param status: True if running, False if not.
      :type status: bool
      :return: None
      :rtype: NoneType


   .. method:: isPlaying(self)


      Gets the running status.
      :return: True if running, False if not.
      :rtype: bool


   .. method:: play(self)


      Runs the Observer.

      :return: True if the observer is running, False otherwise.
      :rtype: bool


   .. method:: pause(self)


      Stops the Observer.

      :return: True if the observer is running, False otherwise.
      :rtype: bool


   .. method:: getPID(self)


      Gets the Process ID of the process that is being watched by the observer

      :return: The process ID of the process that the observer is watching.
      :rtype: int



