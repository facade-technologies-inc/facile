:orphan:

:mod:`copyprojectdialog`
========================

.. py:module:: copyprojectdialog

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

   This module contains the code for the copy project dialog.



Module Contents
---------------


.. py:class:: CopyProjectDialog(parent: QWidget = None, oldProject: Project = None)

   ..
      Bases: :class:`PySide2.QtWidgets.QDialog`

   Inheritance Hierarchy:

   .. inheritance-diagram:: copyprojectdialog.CopyProjectDialog

   This class is used to create a new project from an existing one. It is a dialog that pops up
   and prompts the user to enter information about the project to copy and the project to be created.

   When the user enters information, the information will be checked for validity.
   If any information is not valid, the project will not be created and error messages will appear.

   Constructs a CopyProjectDialog object.

   :param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
   :type parent: PySide2.QtWidgets.QWidget
   :param oldProject: The project to copy. If None, the user can select the location of an existing project.
   :type oldProject: Project

   .. attribute:: projectCreated
      

      

   .. method:: _setOldProject(self, oldProject: Project)


      Sets the existing project that will be copied and fills/enables the appropriate fields in the dialog.

      :param oldProject: The project to copy from
      :type oldProject: Project
      :return: None
      :rtype: NoneType


   .. method:: _setNewProjectURL(self, url: str)


      Fills the text of the new project's location field

      :param url: The path to the .fcl file of the existing project
      :type url: str
      :return: None
      :rtype: NoneType


   .. method:: _browseForExistingProject(self)


      Opens a file dialog when the user clicks on the existing project's "..." button to choose an
      existing .fcl file.

      :return: None
      :rtype: NoneType


   .. method:: _browseForNewProjectDir(self)


      Opens a file dialog when the user clicks on the new project's "..." button to choose the directory
      for the new project.

      The file dialog will only show folders. If the user selects a folder that already has a project in
      it, an error message will appear when the user tries to copy.

      :return: None
      :rtype: NoneType


   .. method:: accept(self)


      This method is called when the user clicks the "OK" button.

      It will validate all of the user's input and show error messages if
      any information is invalid.

      :emits: projectCreated if a project was successfully created
      :return: None
      :rtype: NoneType



