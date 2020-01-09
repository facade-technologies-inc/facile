:orphan:

:mod:`facileview`
=================

.. py:module:: facileview

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

   This module contains the FacileView class which is the main window of Facile.
   Much of Facile is joined together here.



Module Contents
---------------


.. py:class:: FacileView

   Bases: :class:`PySide2.QtWidgets.QMainWindow`
   .. inheritance-diagram:: facileview.FacileView

   FacileView is the main window for Facile.

   Constructs a FacileView object.

   :return: The new FacileView object
   :rtype: FacileView

   .. method:: setProject(self, project: Project)


      Sets the project object.

      :param project: The new Project object to set
      :type project: Project
      :return: None
      :rtype: NoneType


   .. method:: onSaveProjectAsTriggered(self)


      This slot is run when the user clicks "File -> Save As..."

      :return: None
      :rtype: NoneType


   .. method:: onSaveProjectTriggered(self)


      This slot is run when the user saves the current project in Facile

      :return: None
      :rtype: NoneType


   .. method:: onNewProjectFromScratchTriggered(self)


      This slot is run when the user elects to create a new project from scratch.

      A NewProjectDialog is opened that allows the user to specify the target application,
      description, location, etc.

      :return: None
      :rtype: NoneType


   .. method:: onNewProjectFromExistingTriggered(self)


      This slot is run when the user elects to create a new project from an existing one.
      A CopyProjectDialog is opened that allows the user to specify the new location, name, and description.

      :return: None
      :rtype: NoneType


   .. method:: onOpenRecentProject(self)


      This slot is run when the user selects to open a recent project.

      :return: None
      :rtype: NoneType


   .. method:: onOpenProjectTriggered(self)


      This slot is run when the user elects to open an existing project.

      A file dialog is open with the .fcl filter. Once the user selects a project, it will be loaded into Facile.

      :return: None
      :rtype: NoneType


   .. method:: onManageProjectTriggered(self)


      This slot is run when the user selects "file -> project settings"

      :return: None
      :rtype: NoneType


   .. method:: onAddBehaviorTriggered(self)


      This slot is run when the user selects "Add Behavior"

      :return: None
      :rtype: NoneType


   .. method:: onProjectExplorerIndexSelected(self, selected: QItemSelection, deselected: QItemSelection)


      This slot is called when an item is selected in the project explorer.

      :param selected: The newly selected items
      :type selected: QItemSelection
      :param deselected: The items that used to be selected.
      :type deselected: QItemSelection
      :return: None
      :rtype: NoneType


   .. method:: onStartAppTriggered(self)


      This slot is run when the user selects "Start App"

      :return: None
      :rtype: NoneType


   .. method:: onStopAppTriggered(self, confirm=True)


      This slot is run when the user selects "Stop App"

      :return: None
      :rtype: NoneType


   .. method:: onItemSelected(self, id: int)


      This slot will update the view when an item is selected.

      :return: None
      :rtype: NoneType


   .. method:: onItemBlink(self, id: int)


      Attempt to show an item in the GUI. Can only do this if the item is currently shown in
      the GUI.

      :param id: The ID of the component to show.
      :type id: int
      :return: None
      :rtype: NoneType


   .. method:: onManualExploration(self, checked: bool)


      Sets the exploration mode to be manual iff checked is True

      :param checked: if True, set the exploration mode to be manual. Else leave exploration.
      :type checked: bool
      :return: None
      :rtype: NoneType


   .. method:: onAutomaticExploration(self, checked: bool)


      Sets the exploration mode to be automatic iff checked is True

      :param checked: if True, set the exploration mode to automatic. Else leave exploration.
      :type checked: bool
      :return: None
      :rtype: NoneType


   .. method:: info(self, message: str)


      This function will show a box with a message that will fade in and then out.

      :param message: The message to show inside of the window
      :type message: str
      :return: None
      :rtype: NoneType



