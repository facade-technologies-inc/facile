from PySide2.QtWidgets import QItemDelegate, QStyledItemDelegate, QStyle
import data
import model

class delegate(QStyledItemDelegate):
        """ A subclass that allows us to render our QTreeView and editing the Model"""
        def __init__(self, spinBox):
            QStyledItemDelegate.__init__(self)
            self._spinBox = spinBox

        def createEditor(self, parent, option, index):
            """ Creates the widget used to change data from the model and can be
            reimplemented to customize editing behavior"""
            if index.column() == 1:
                editor = self._spinBox
                editor.setMinimum(0)
                editor.sexMaximum(100)
                return editor
            else:
                return QStyledItemDelegate.createEditor(self, parent, option, index)

        def setEditorData(self, spinBox, index):
            """ Provides the widget with data to manipulate."""
            row = index.row()
            col = index.column()
            data = index.internalPointer()

            if data in self._spinBox.getCategories():
                if col == 1:
                    return spinBox.setValue(data)
                else:
                    return None

        def updateEditorGeometry(self, spinBox, option, index):
            """Ensures that the editor is displayed correctly with respect to the item view"""

        def setModelData(self, spinBox, model, index):
            """ Returns updated data to the model"""




