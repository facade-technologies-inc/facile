:orphan:

:mod:`newprojectdialog`
=======================

.. py:module:: newprojectdialog

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

   This module contains the code for the new project dialog.



Module Contents
---------------


.. py:class:: NewProjectDialog(parent: QWidget = None)

   ..
      Bases: :class:`PySide2.QtWidgets.QDialog`

   Inheritance Hierarchy:

   .. inheritance-diagram:: newprojectdialog.NewProjectDialog

   This class is used to create a new project from scratch. It is a dialog that pops up
   and prompts the user to enter information about the project to be created.

   When the user enters information, the information will be checked for validity.
   If any information is not valid, the project will not be created and error messages will appear.

   Constructs a NewProjectDialog object.

   :param parent: the widget to nest this dialog inside of. If None, this dialog will be a window.
   :type parent: PySide2.QtWidgets.QWidget
   :return: The constructed new project dialog object.
   :rtype: NewProjectDialog

   .. attribute:: projectCreated
      

      

   .. method:: _browseProjectFolders(self)


      Opens a file dialog when the user clicks on the "..." button to choose a project directory.

      The user will only be able to select folders, and when a folder is selected, the value will
      be placed into the read-only text editor to the left. The user should not select a directory
      where a project already exists.

      :return: None
      :rtype: NoneType


   .. method:: _browseApplicationFile(self)


      Opens a file dialog when the user clicks on the "..." button to choose a target application.

      The dialog that pops up doesn't restrict what file the user selects, but before creating the
      project, the file will be checked for correct bitness, and to make sure that it's an executable file.
      The path to the file will be placed into the read-only text editor to the left.

      :return: None
      :rtype: NoneType


   .. method:: _onBackendChecked(self, checkedButton: QRadioButton)


      Unchecks all of the backend radio buttons except the button that was passed in.

      If the button that was passed in is anything but the "other" button, clear the
      text field next to the "other" radio button.

      :param checkedButton: The radio button that was just clicked.
      :type checkedButton: QRadioButton
      :return: None
      :rtype: NoneType


   .. method:: accept(self)


      This method is called when the user clicks the "OK" button.

      It will validate all of the user's input and show error messages if
      any information is invalid.

      :emits: projectCreated if a project was successfully created
      :return: None
      :rtype: NoneType



