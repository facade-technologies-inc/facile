from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
import data

class PropModel(QAbstractItemModel):
    def __init__(self, propData):
        QAbstractItemModel.__init__(self)
        self._propData = propData

    def index(self, row, column, parent):
        """ Purpose of this function is to return a QModelIndex that maps to the appropriate data"""
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        #referencing category
        if not parent.isValid():
            internalData = self._propData.getCategories()[row]
        else:
            parentData = parent.internalPointer()
            if parentData in self._propData.getCategories():
                internalData = self._propData.getCategoryProperties(parentData)

            else:
                return QModelIndex()

        return self.createIndex(row, column, internalData)

    def parent(self, index):
        """Purpose of this function is to return the parent index of the index that is provided"""
        if not index.isValid():
            return QModelIndex()

        data = index.internalPointer()

        if data in self._propData.getCategories():
            return QModelIndex()

        category = self._propData.getPropertyCategory(data)

        return self.createIndex(self._propData.getCategoryIndex(category),0,category)

    def columnCount(self, parent):
        """Purpose of this function is to return the number of columns for the children of a given parent"""
        if not parent.isValid():
            return 2 #1

        parentData = parent.internalPointer()

        if parentData in self._propData.getCategories():
            return 2
        else:
            return 2 #0

    def rowCount(self, parent):
        """Purpose of this function is to return the number of children of a given parent"""
        if not parent.isValid():
            return 3
            numCategories = self._propData.getNumCategories()
            return numCategories

        parentData = parent.internalPointer()

        if parentData in self._propData.getCategories():
            return self._propData.getNumPropertiesInCategory(parentData)
        else:
            return 0

    def data(self, index, role):
        """Purpose of this function is to retrieve data stored under the given role for the item reffered to by the
        index """
        if not index.isValid():
            return QModelIndex()

        if not role != Qt.DisplayRole:
            return None

        row = index.row()
        col = index.column()
        data = index.internalPointer()

        if data in self._propData.getCategories():
            return data
        else:
            col = index.column()
            if col == 0:
                return data.getName()
            elif col == 1:
                return data.getValue()
            else:
                return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ["Name","Value"][section]
        return None
















