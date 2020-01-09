:orphan:

:mod:`explorer`
===============

.. py:module:: explorer

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
       
   This module contains the Explorer class, which explores the target GUI.



Module Contents
---------------


.. py:class:: Explorer(processID: int, backend: str = 'uia')

   Bases: :class:`PySide2.QtCore.QThread`
   .. inheritance-diagram:: explorer.Explorer

   The explorer class makes use of recursive functions to break down the target gui into its smallest components,
   and then clicking on every clickable component as well as prompting the user for input on any textfields.

   Initializes explorer.

   :param processID: process ID of target application
   :type processID: int
   :param backend: type of backend to use: either uia or win32
   :type backend: str

   .. attribute:: ignoreTypes
      

      

   .. method:: run(self)


      Called when thread is started

      :return: the exit code
      :rtype: int


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


      Runs the Explorer.

      :return: True if the observer is running, False otherwise.
      :rtype: bool


   .. method:: pause(self)


      Stops the Explorer.

      :return: True if the observer is running, False otherwise.
      :rtype: bool



