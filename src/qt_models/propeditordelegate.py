"""
/------------------------------------------------------------------------------\
|                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
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
"""

from enum import Enum

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QModelIndex, QRect, QEvent
from PySide2.QtWidgets import QStyleOptionViewItem, QStylePainter
from PySide2.QtWidgets import QStyledItemDelegate, QLineEdit, QSpinBox, \
	QCheckBox, QDoubleSpinBox, QWidget, QComboBox

from data.property import Property
from qt_models.propeditormodel import PropModel


class PropertyEditorDelegate(QStyledItemDelegate):
	"""
	A subclass that allows us to render our QTreeView and editing the Model
	"""
	
	def getCheckBoxRect(self, option: QStyleOptionViewItem) -> QRect:
		"""
		Get rect for checkbox centered in option.rect.

		:param option: Option for the rectangle.
		:type option: QStyleOptionViewItem
		:return: Constructs a null rectangle for the checkbox.
		:rtype: QRect
		"""
		check_box_style_option = QtWidgets.QStyleOptionButton()
		check_box_rect = QtWidgets.QApplication.style().subElementRect(
			QtWidgets.QStyle.SE_CheckBoxIndicator,
			check_box_style_option, None)
		check_box_point = QtCore.QPoint(option.rect.x() +
		                                check_box_rect.width() / 2,
		                                option.rect.y() +
		                                option.rect.height() / 2 -
		                                check_box_rect.height() / 2)
		return QRect(check_box_point, check_box_rect.size())
	
	def paint(self, painter: QStylePainter, option: QStyleOptionViewItem,
	          index: QModelIndex) -> None:
		"""
		Paint a checkbox without the label.

		:param painter: This draws the widget.
		:type painter: QStylePainter
		:param option: Option for the style of checkbox.
		:type option: QStyleOptionViewItem
		:param index: Index for the painted checkbox.
		:type index: QModelIndex
		:return: None
		:rtype: NoneType
		"""
		if index.column() == 1 and isinstance(index.internalPointer(),
		                                      Property) and index.internalPointer().getType() == bool:
			checked = index.internalPointer().getValue()
			check_box_style_option = QtWidgets.QStyleOptionButton()
			
			if (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
				check_box_style_option.state |= QtWidgets.QStyle.State_Enabled
			else:
				check_box_style_option.state |= QtWidgets.QStyle.State_ReadOnly
			
			if checked:
				check_box_style_option.state |= QtWidgets.QStyle.State_On
			else:
				check_box_style_option.state |= QtWidgets.QStyle.State_Off
			
			check_box_style_option.rect = self.getCheckBoxRect(option)
			check_box_style_option.state |= QtWidgets.QStyle.State_Enabled
			QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_CheckBox,
			                                           check_box_style_option, painter)
		else:
			QStyledItemDelegate.paint(self, painter, option, index)
	
	def createEditor(self, parent: QModelIndex, option: QStyleOptionViewItem,
	                 index: QModelIndex) -> QWidget:
		"""
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
		"""
		data = index.internalPointer()
		if index.column() == 1 and isinstance(data, Property) and data.getType() == bool:
			return None

		if type(data) == Property:
			if index.column() == 1:
				t = data.getType()
				if t == str:
					return QLineEdit(parent)
				elif t == int:
					return QSpinBox(parent)
				elif t == bool:
					return QCheckBox(parent)
				elif t == float:
					return QDoubleSpinBox(parent)
				elif issubclass(t, Enum):
					editor = QComboBox(parent)
					for i, option in enumerate(t):
						editor.addItem(option.name, option)
					return editor
				else:
					pass
		return QStyledItemDelegate.createEditor(self, parent, option, index)
	
	def editorEvent(self, event: QEvent, model: 'PropModel', option: QStyleOptionViewItem,
	                index: QModelIndex) -> bool:
		"""
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
		:return: Returns true if the given editor is a valid QWidget
		and the given event is handled; otherwise returns false.
		:rtype: bool
		"""
		event.type()
		if not (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
			return False
		
		data = index.internalPointer()
		if index.column() != 1 or not isinstance(data, Property) or data.getType() != bool:
			return QStyledItemDelegate.editorEvent(self, event, model, option, index)
		
		# Do not change the checkbox-state
		if event.type() == QEvent.MouseButtonPress:
			return False
		if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
			if event.button() != QtCore.Qt.LeftButton or not self.getCheckBoxRect(option).contains(
				event.pos()):
				return False
			if event.type() == QEvent.MouseButtonDblClick:
				return True
		elif event.type() == QEvent.KeyPress:
			if event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Select:
				return False
		else:
			return False
		
		# Change the checkbox-state
		checkbox = QCheckBox('temp')
		checkbox.setChecked(not data.getValue())
		self.setModelData(checkbox, model, index)
		return True
	
	def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
		"""
		Provides the widget with data to manipulate.

		:param editor: Editor that will be set for certain data structures.
		:type editor: QWidget
		:param index: Index of the editor.
		:type index: QModelIndex
		:return: None
		:rtype: NoneType
		"""
		data = index.internalPointer()
		
		if type(data) == Property:
			value = data.getValue()
			if index.column() == 1:
				t = data.getType()
				if t == str:
					editor.setText(value)
				elif t == int:
					editor.setValue(value)
				elif t == bool:
					editor.setChecked(value)
				elif t == float:
					editor.setValue(value)
				elif issubclass(t, Enum):
					pass  # TODO: set combo box default data
				else:
					pass
	
	def setModelData(self, editor: QWidget, model: 'PropModel', index: QModelIndex) -> None:
		"""
		Returns updated data to the model

		:param editor: Editor that will be set for certain data structures.
		:type editor: QWidget
		:param model: The model that our delegate will render.
		:type model: PropModel
		:param index: Index of the editor.
		:type index: QModelIndex
		:return: None
		:rtype: NoneType
		"""
		data = index.internalPointer()
		
		if type(data) == Property:
			if index.column() == 1:
				t = data.getType()
				if t == str:
					data.setValue(editor.text())
				elif t == int:
					data.setValue(editor.value())
				elif t == bool:
					data.setValue(editor.isChecked())
				elif t == float:
					data.setValue(editor.value())
				elif issubclass(t, Enum):
					data.setValue(editor.currentData())
				else:
					pass
