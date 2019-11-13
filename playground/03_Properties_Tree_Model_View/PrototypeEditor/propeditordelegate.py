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

from PySide2.QtWidgets import QItemDelegate, QStyledItemDelegate, QStyle, QLineEdit, QSpinBox, QCheckBox, QDoubleSpinBox
from property import Property
from PySide2.QtCore import QRect
from propeditormodel import PropModel


class PropertyEditorDelegate(QStyledItemDelegate):
    """
    A subclass that allows us to render our QTreeView and editing the Model
    """

    # TODO: Make the bool character more optimal by only showing the check box without "true/false" strings
    # TODO: Support for Enums
    # TODO: Support for Lists

    def createEditor(self, parent: object, option: object, index: object) -> object:
        """
        Creates the widget used to change data from the model and can be
        reimplemented to customize editing behavior

        :param parent: Parent of the editor.
        :type parent: object
        :param option: Option of the editor.
        :type option: object
        :param index: Index of the editor.
        :type index: object
        :return: Editor for PropModel
        :rtype: QObject
        """
        data = index.internalPointer()

        if type(data) == Property:
            if index.column() == 1:
                t = Property.getType()
                if t == str:
                    return QLineEdit(parent)
                elif t == int:
                    return QSpinBox(parent)
                elif t == bool:
                    return QCheckBox(parent)
                elif t == float:
                    return QDoubleSpinBox(parent)
                else:
                    pass
        return QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor: object, index: object) -> None:
        """
        Provides the widget with data to manipulate.

        :param editor: Editor that will be set for certain data structures.
        :type editor: object
        :param index: Index of the editor.
        :type index: object
        :return: None
        :rtype: NoneType
        """
        data = index.internalPointer()

        if type(data) == Property:
            value = Property.getValue()
            if index.column() == 1:
                t = Property.getType()
                if t == str:
                    editor.setText(value)
                elif t == int:
                    editor.setValue(value)
                elif t == bool:
                    editor.setChecked(value)
                elif t == float:
                    editor.setValue(value)
                else:
                    pass

    def setModelData(self, editor: object, PropModel: classmethod, index: object) -> None:
        """
        Returns updated data to the model

        :param editor: Editor that will be set for certain data structures.
        :type editor: object
        :param PropModel: The model that our delegate will render.
        :type PropModel: class method
        :param index: Index of the editor.
        :type index: object
        :return: None
        :rtype: NoneType
        """
        data = index.internalPointer()

        if type(data) == Property:

            if index.column() == 1:
                t = Property.getType()
                if t == str:
                    Property.setValue(editor.text())
                elif t == int:
                    Property.setValue(editor.value())
                elif t == bool:
                    Property.setValue(editor.isChecked())
                elif t == float:
                    Property.setValue(editor.value())
                else:
                    pass
