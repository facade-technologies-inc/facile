:orphan:

:mod:`blinker`
==============

.. py:module:: blinker

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

   This module contains the blinker class which is used to relate the target GUI model
   to the actual target GUI.



Module Contents
---------------


.. py:class:: Blinker(pid: int, backend: str, superToken: SuperToken)

   ..
      Bases: :class:`PySide2.QtCore.QThread`

   Inheritance Hierarchy:

   .. inheritance-diagram:: blinker.Blinker

   The Blinker class is used to draw a box around a given element at a specified frequency for a small
   amount of time. Because the box sometimes disappears on its own, this can cause a blinking affect.

   Creates a blinker that will draw a box around the component represented by SuperToken periodically
   if the component can be found.

   :param pid: The id of the target application's process.
   :type pid: int
   :param backend: either "win32" or "uia" depending on target application.
   :type backend: str
   :param superToken: The supertoken that represents the component that we want to draw a box around.
   :return: None
   :retype: NoneType

   .. attribute:: componentNotFound
      

      

   .. attribute:: INTERVAL_MILLIS
      :annotation: = 250

      

   .. attribute:: DURATION_MILLIS
      :annotation: = 10000

      

   .. attribute:: colors
      :annotation: = ['red', 'green', 'blue']

      

   .. attribute:: curColorIdx
      :annotation: = 0

      

   .. method:: run(self)


      DO NOT CALL THIS METHOD!
      This method is called automatically when the start() method is called.

      This method searches for a Component in the target GUI by traversing
      :return: None
      :rtype: NoneType


   .. method:: initiateBlinkSequence(self, component: Component)


      Starts the blink sequence by setting timers and executing an event loop.

      NOTE: Because this function executes an event loop, it is blocking.

      :param component: The component to select.
      :type component: Component
      :return: None
      :rtype: NoneType


   .. method:: tick(self)


      Draws an outline around the component of interest.

      :return: None
      :rtype: NoneType


   .. method:: stop(self)


      Stops the blinker regardless of whether it was running or not.

      :return: None
      :rtype: NoneType



