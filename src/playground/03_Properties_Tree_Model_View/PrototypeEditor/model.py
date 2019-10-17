from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
import data

class PropModel(QAbstractItemModel):
    def __init__(self, propData)
        self._propData = propData

    def index(self, row, column, parent):

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        #referencing category
        if not parent.isValid():
            internalData = propData.getCategories()[row]

        return QModelIndex()


