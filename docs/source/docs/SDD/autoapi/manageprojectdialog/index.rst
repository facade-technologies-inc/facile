:orphan:

:mod:`manageprojectdialog`
==========================

.. py:module:: manageprojectdialog

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

   This module contains the code for the manage project dialog.



Module Contents
---------------


.. data:: backends
   :annotation: = ['WIN32', 'UIA', 'Other']

   

.. py:class:: ManageProjectDialog(project: Project, parent: QWidget = None)

   Bases: :class:`PySide2.QtWidgets.QDialog`
   .. inheritance-diagram:: manageprojectdialog.ManageProjectDialog

   This class is used to create a new project from scratch. It is a dialog that pops up
   and prompts the user to enter information about the project to be created.

   When the user enters information, the information will be checked for validity.
   If any information is not valid, the project will not be created and error messages will appear.

   Constructs a ManageProjectDialog object.

   :param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
   :type parent: PySide2.QtWidgets.QWidget

   .. attribute:: projectCreated
      

      

   .. method:: accept(self)


      Called when the user clicks the "save" button.

      :return: None
      :rtype: NoneType


   .. method:: reject(self)


      Called when the user clicks the "close" button.

      :return: None
      :rtype: NoneType



