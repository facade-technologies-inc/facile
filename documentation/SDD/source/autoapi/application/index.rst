:orphan:

:mod:`application`
==================

.. py:module:: application

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

   This file contains the Application class - an alternative to pywinauto's Application class that builds off of
   pywinauto's Desktop class.



Module Contents
---------------


.. py:class:: Application(backend: str = 'uia')

   ..
      Bases: :class:`pywinauto.Desktop`

   Inheritance Hierarchy:

   .. inheritance-diagram:: application.Application

   This class is an alternative to pywinauto's Application class that will detect windows in all of an application's
   processes.

   To use:
           process = psutil.Popen(["path/to/target/application.exe", ...], stdout=PIPE)
           app = Application(backend="uia")
           app.setProcess(process)
           appWindows = app.windows()

   Constructs an Application instance

   :param backend: the accessibility technology to use to deconstruct the target GUI.
   :type backend: str
   :return: None
   :rtype: NoneType

   .. method:: setProcess(self, process: psutil.Process)


      Sets the application's process. This method should be called directly after the Application object is
      instantiated

      :param process: the target application's main process
      :type process: psutil.Process
      :return: None
      :rtype: NoneType


   .. method:: getPIDs(self)


      Gets the target application's main process ID and all child process IDs.

      :return: list of all process IDs belonging to the target application.
      :rtype: list[int]


   .. method:: windows(self)


      Gets all windows which belong to the target application and child processes.

      :return: list of windows that belong to the target application and it's children processes
      :type: list[pywinauto.application.WindowSpecification]


   .. method:: getStartTime(self)


      Gets the time that the Application instance was created as an int.

      :return: The time that the Application instance was created.
      :rtype: int



.. data:: desktop
   

   

