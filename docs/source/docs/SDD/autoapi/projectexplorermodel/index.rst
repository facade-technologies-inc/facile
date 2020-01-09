:orphan:

:mod:`projectexplorermodel`
===========================

.. py:module:: projectexplorermodel

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

   This module contains the Qt model for the project explorer.



Module Contents
---------------


.. py:class:: ProjectExplorerModel(project: Project, view: QTreeView)

   Bases: :class:`PySide2.QtCore.QAbstractItemModel`
   .. inheritance-diagram:: projectexplorermodel.ProjectExplorerModel

   This class is the Qt model that gets loaded into the project explorer view in Facile.

   Constructs a ProjectExplorerModel exception

   :param project: A Facile project object.
   :type project: Project

   .. py:class:: LeafIndex(me: object, parent: object, parentIndex: int = None)

      This class holds the information for a QModelIndex as well as its parent and the row of the parent.
      If a QModelIndex holds this object as its internal pointer, the QModelIndex will have no children.

      Constructs a LeafIndex object.

      :param me: The data for a QModelIndex.
      :type me: object
      :param parent: The data for the parent QModelIndex.
      :type parent: object
      :param parentIndex: The row of the parent.
      :type parentIndex: int

      .. method:: getData(self)


         Gets the internal data of the current index.

         :return: the data for the current index.
         :rtype: object


      .. method:: getParent(self)


         Gets the internal data of the parent index.

         :return: the data for the parent index.
         :rtype: object


      .. method:: getParentIndex(self)


         Gets the row of the parent.

         :return: the row of the parent
         :rtype: int


      .. method:: __eq__(self, other: LeafIndex)


         Determine if 2 LeafIndex objects are equal.
         2 LeafIndex objects are equal if they have all the same data.

         :param other: the other leaf index to compare to.
         :type other: LeafIndex
         :return: True if they're equal, False otherwise
         :rtype: bool


      .. method:: __ne__(self, other: LeafIndex)


         Determine if 2 LeafIndex objects are not equal. This is the inverse of the __eq__ function

         :param other: the other leaf index to compare to.
         :type other: LeafIndex
         :return: False if they're equal, True otherwise
         :rtype: bool


      .. method:: __hash__(self)


         Get the Hash for a LeafIndex object. LeafIndex objects with all of the same data will have the same hash.

         :return: The hash of the LeafIndex object
         :rtype: int



   .. attribute:: componentSelected
      

      

   .. attribute:: behaviorSelected
      

      

   .. attribute:: pipelineSelected
      

      

   .. attribute:: TARGET_GUI_LABEL
      :annotation: = Target GUI

      

   .. attribute:: COMPONENT_LABEL
      :annotation: = GUI Components

      

   .. attribute:: BEHAVIOR_LABEL
      :annotation: = Visibility Behaviors

      

   .. attribute:: PIPELINE_LABEL
      :annotation: = Action Pipelines

      

   .. attribute:: NO_COMPONENTS_LABEL
      :annotation: = No GUI Components Yet.

      

   .. attribute:: NO_BEHAVIORS_LABEL
      :annotation: = No Visibility Behaviors Yet.

      

   .. attribute:: NO_PIPELINES_LABEL
      :annotation: = No Action Pipelines Yet.

      

   .. attribute:: TARGET_GUI_ROW
      :annotation: = 0

      

   .. attribute:: COMPONENT_ROW
      :annotation: = 0

      

   .. attribute:: BEHAVIOR_ROW
      :annotation: = 1

      

   .. attribute:: PIPELINE_ROW
      :annotation: = 1

      

   .. attribute:: MODEL
      :annotation: = 0

      

   .. attribute:: PATH
      :annotation: = 1

      

   .. method:: index(self, row: int, column: int, parent: QModelIndex)


      Gets a model index given the parent index, row, and column.

      :param row: the index of the rowth child of "parent".
      :type row: int
      :param column: the column of the index to be created.
      :type column: int
      :param parent: the parent of the index to be created.
      :type parent: QModelIndex
      :return: the model index with the given parent, row, and column.
      :rtype: QModelIndex


   .. method:: parent(self, index: QModelIndex)


      Creates a model index for the parent of the given index.

      :param index: the index to get the parent of.
      :type index: QModelIndex
      :return: The parent index of the index provided.
      :rtype: QModelIndex


   .. method:: rowCount(self, parent: QModelIndex)


      Get the number of rows for a given index.

      :param parent: the index to get the number of rows in.
      :type parent: QModelIndex
      :return: The number of rows (children) underneath the given index.
      :rtype: int


   .. method:: columnCount(self, parent: QModelIndex)


      Gets the number of columns on the next level of a given index.
      In our case, there will always be 2 columns.

      :param parent: The index of which to get the number of columns under.
      :type parent: QModelIndex
      :return: the number of columns under the given index.
      :rtype: int


   .. method:: flags(self, index: QModelIndex)


      Get the flags associated with the given index

      :param index: the index to get the flags for
      :type index: QModelIndex
      :return: The flags with a given index
      :rtype: Qt.ItemFlags


   .. method:: data(self, index: QModelIndex, role: Qt.ItemDataRole)


      Gets the data associated with a specific index and the specific role.

      :param index: The index to get the data from
      :type index: QModelIndex
      :param role: The role to use to get the data.
      :type role: Qt.ItemDataRole
      :return: The data for the given role
      :rtype: str or NoneType


   .. method:: headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.DisplayRole)


      Gets the header data.

      :param section: either the row or the column depending on the orientation.
      :type section: int
      :param orientation: Qt.Horizontal for header on top or Qt.Vertical for header on the left
      :type orientation: Qt.Orientation
      :param role: the role to use to get the data.
      :type role: Qt.ItemDataRole
      :return: the data
      :rtype: str


   .. method:: selectionChanged(self, selected: QItemSelection, deselected: QItemSelection)


      Run this slot when an index is selected. This slot will emit the following 3 signals depending on what was
      selected: componentSelected, behaviorSelected, pipelineSelected
              
      :param selected: The new selection
      :type selected: QItemSelection
      :param deselected: The old selection
      :type deselected: QItemSelection
      :return: None
      :rtype: NoneType


   .. method:: registerAndCreateIndex(self, row, col, data)


      Keep a reference to the internal data of all QModelIndex objects. This allows us to avoid memory access errors.
      Without storing a reference to the internal data, the python objects go out of scope and become garbage
      collected.

      This method also creates a QModelIndex and returns it

      :param row: the row of the QModelIndex to create.
      :type row: int
      :param col: the column of the QModelIndex to create.
      :type col: int
      :param data: The object stored inside of the QModelIndex.
      :type data: object
      :return: The created QModelIndex
      :rtype: QModelIndex


   .. method:: selectComponent(self, component: Component)


      Selects a component in the project explorer by expanding all parents recursively.

      :param component: The component to select
      :type component: Component
      :return: None
      :rtype: NoneType


   .. method:: selectBehavior(self, visibilityBehavior: VisibilityBehavior)


      Select a visibility behavior in the project explorer.

      :param visibilityBehavior: The visibility behavior to select.
      :type visibilityBehavior: VisibilityBehavior
      :return: None
      :rtype: NoneType



