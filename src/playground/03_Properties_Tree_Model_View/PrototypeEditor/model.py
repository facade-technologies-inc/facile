from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtGui import QColor
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
                internalData = self._propData.getCategoryProperties(parentData)[row]

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
        return 2

    def rowCount(self, parent):
        """Purpose of this function is to return the number of children of a given parent"""
        if not parent.isValid():
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

        row = index.row()
        col = index.column()
        data = index.internalPointer()

        if role == Qt.DisplayRole:
            if data in self._propData.getCategories():
                if col == 0:
                    return data
                else:
                    return None
            else:
                col = index.column()
                if col == 0:
                    return data.getName()
                elif col == 1:
                    return str(data.getValue())
                else:
                    return None
                
        elif role == Qt.BackgroundRole:
            if data in self._propData.getCategories():
                return QColor(Qt.yellow)
            else:
                shade = row%2 * 25
                return QColor(100+shade, 150+shade, 200+shade)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ["Name","Value"][section]
        return None
    
    
    
    #########################################################################
    def traverse(self):
        """ This method is used for debugging by mimicing how a view might query the model for data."""
        parent = QModelIndex()
        work = [parent]
        
        while len(work) > 0:
            cur = work.pop()
            
            curRow = cur.row()
            curCol = cur.column()
            curData = self.data(cur, Qt.DisplayRole)
            if cur.isValid():
                print(curRow, curCol, curData)
                pass
                
            rows = self.rowCount(cur)
            cols = self.columnCount(cur)
            for r in range(rows):
                for c in range(cols):
                    work.append(self.index(r, c, cur))
        
    
        
















