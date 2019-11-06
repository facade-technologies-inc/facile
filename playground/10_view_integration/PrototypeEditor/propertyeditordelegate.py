from PySide2.QtWidgets import QItemDelegate, QStyledItemDelegate, QStyle, QLineEdit, QSpinBox, QCheckBox, QDoubleSpinBox
from data import Property, Properties
import model

class PropertyEditorDelegate(QStyledItemDelegate):
        """ A subclass that allows us to render our QTreeView and editing the Model"""

        def createEditor(self, parent, option, index):
            """ Creates the widget used to change data from the model and can be
            reimplemented to customize editing behavior"""
            data = index.internalPointer()

            if type(data) == Property:
                if index.column() == 1:
                    t = data.getType()
                    if t == str:
                        return QLineEdit(parent)
                    elif t == int:
                        return QSpinBox(parent)
                    elif t == bool:
                        # TODO: Make the bool character more optimal
                        return QCheckBox(parent)
                    elif t == float:
                        return QDoubleSpinBox(parent)
                    else:
                        #TODO:Handle drop down menus later
                        pass
            return QStyledItemDelegate.createEditor(self, parent, option, index)


        def setEditorData(self, editor, index):
            """ Provides the widget with data to manipulate."""
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
                        # TODO: Make the bool character more optimal
                        editor.setChecked(value)
                    elif t == float:
                        editor.setValue(value)
                    else:
                        # TODO:Handle drop down menus later
                        pass

        def setModelData(self, editor, model, index):
            """ Returns updated data to the model"""
            data = index.internalPointer()

            if type(data) == Property:

                if index.column() == 1:
                    t = data.getType()
                    if t == str:
                        data.setValue(editor.text())
                    elif t == int:
                        data.setValue(editor.value())
                    elif t == bool:
                        # TODO: Make the bool character more optimal
                        data.setValue(editor.isChecked())
                    elif t == float:
                        data.setValue(editor.value())
                    else:
                        # TODO:Handle drop down menus later
                        pass

