:orphan:

:mod:`propeditordelegate`
=========================

.. py:module:: propeditordelegate

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

   This module contains the PropertyEditorDelegate() Class.



Module Contents
---------------


.. py:class:: PropertyEditorDelegate

   Bases: :class:`PySide2.QtWidgets.QStyledItemDelegate`
   .. inheritance-diagram:: propeditordelegate.PropertyEditorDelegate

   A subclass that allows us to render our QTreeView and editing the Model

   .. method:: getCheckBoxRect(self, option: QStyleOptionViewItem)


      Get rect for checkbox centered in option.rect.

      :param option: Option for the rectangle.
      :type option: QStyleOptionViewItem
      :return: Constructs a null rectangle for the checkbox.
      :rtype: QRect


   .. method:: paint(self, painter: QStylePainter, option: QStyleOptionViewItem, index: QModelIndex)


      Paint a checkbox without the label.

      :param painter: This draws the widget.
      :type painter: QStylePainter
      :param option: Option for the style of checkbox.
      :type option: QStyleOptionViewItem
      :param index: Index for the painted checkbox.
      :type index: QModelIndex
      :return: None
      :rtype: NoneType


   .. method:: createEditor(self, parent: QModelIndex, option: QStyleOptionViewItem, index: QModelIndex)


      Creates the widget used to change data from the model and can be
      reimplemented to customize editing behavior

      :param parent: Parent of the editor.
      :type parent: QModelIndex
      :param option: Option of the editor.
      :type option: QStyleOptionViewItem
      :param index: Index of the editor.
      :type index: QModelIndex
      :return: Editor for PropModel
      :rtype: QWidget


   .. method:: editorEvent(self, event: QEvent, model: PropModel, option: QStyleOptionViewItem, index: QModelIndex)


      Change the data in the model and the state of the checkbox
      if the user presses the left mouse button or presses
      Key_Space or Key_Select and this cell is editable. Otherwise do nothing.

      :param event: The event that will take place to trigger the editor Event.
      :type event: QEvent
      :param model: The model that our delegate will render.
      :type model: PropModel
      :param option: Option for the kind've event that takes place.
      :type option: QStyleOptionViewItem
      :param index: Index of the events.
      :type index: QModelIndex
      :return: true if the given editor is a valid QWidget and the given event is handled; otherwise returns false.
      :rtype: bool


   .. method:: setEditorData(self, editor: QWidget, index: QModelIndex)


      Provides the widget with data to manipulate.

      :param editor: Editor that will be set for certain data structures.
      :type editor: QWidget
      :param index: Index of the editor.
      :type index: QModelIndex
      :return: None
      :rtype: NoneType


   .. method:: setModelData(self, editor: QWidget, model: PropModel, index: QModelIndex)


      Returns updated data to the model

      :param editor: Editor that will be set for certain data structures.
      :type editor: QWidget
      :param model: The model that our delegate will render.
      :type model: PropModel
      :param index: Index of the editor.
      :type index: QModelIndex
      :return: None
      :rtype: NoneType



