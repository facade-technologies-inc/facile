:orphan:

:mod:`propeditormodel`
======================

.. py:module:: propeditormodel

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

   This module contains the PropModel() class.



Module Contents
---------------


.. py:class:: PropModel(propData: object)

   Bases: :class:`PySide2.QtCore.QAbstractItemModel`
   .. inheritance-diagram:: propeditormodel.PropModel

   A subclass that allows us to show the Data through QTreeView.

   Constructs a model for the Property Editor.

   :param propData: The data from the properties.
   :type propData: object
   :return: The constructed model.
   :rtype: QObject

   .. method:: index(self, row: int, column: int, parent: QModelIndex)


      Purpose of this function is to return a QModelIndex that maps to the appropriate data

      :param row: Row of the index.
      :type row: int
      :param column: Column of the index.
      :type column: int
      :param parent: Parent of that row or column.
      :type parent: QModelIndex
      :return: The index for the data.
      :rtype: QModelIndex


   .. method:: parent(self, index: QModelIndex)


      Purpose of this function is to return the parent index of the index that is provided

      :param index: Index that is provided.
      :type index: QModelIndex
      :return: Returns the parent index of the index provided.
      :rtype: QModelIndex


   .. method:: columnCount(self, parent: QModelIndex)


      Purpose of this function is to return the number of columns for the children of a given parent

      :param parent: Parent will tell us our column count.
      :type parent: QModelIndex
      :return: Number of columns.
      :rtype: int


   .. method:: rowCount(self, parent: QModelIndex)


      Purpose of this function is to return the number of children of a given parent

      :param parent: Parent will tell us our column count.
      :type parent: QModelIndex
      :return: Number of rows.
      :rtype: int


   .. method:: data(self, index: QModelIndex, role: int)


      Purpose of this function is to retrieve data stored under the given role for the item referred to by the
      index

      :param index: Index that is provided.
      :type index: QModelIndex
      :param role: The given role for item referred.
      :type role: int
      :return: Data of the given role from index.
      :rtype: object


   .. method:: headerData(self, section: int, orientation: Qt.Orientation, role: int)


      This method is used for displaying the header data for 'the given role
      and orientation of that specific section.

      :param section: Specific section for the header data.
      :type section: int
      :param orientation: Given orientation for the header data.
      :type orientation: Qt.Orientation
      :param role: The given role for the header data.
      :type role: int
      :return: Model of header data.
      :rtype: object


   .. method:: traverse(self)


      This method is used for debugging by mimicking how a view might query the model for data.

      :return: None
      :rtype: NoneType


   .. method:: setData(self, index: QModelIndex, value: object, role: int)


      Purpose of this function is to set the role data for the index to value

      :param index: Index that is provided.
      :type index: QModelIndex
      :param value: Value that is set.
      :type value: object
      :param role: The given role data.
      :type role: int
      :return: Set data for index to a value.
      :rtype: bool


   .. method:: flags(self, index: QModelIndex)


      Purpose of this function is to determine what can be done with a given index

      :param index: Index that is provided.
      :type index: QModelIndex
      :return: Returns the item flags for the given index.
      :rtype: ItemFlags



