from PySide2.QtGui import QStandardItem
from PySide2.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt

def pop_standard_model(model):

    for i in range(3):
        parent1 = QStandardItem('Family {}. Some long status text for sp'.format(i))
        for j in range(3):
            child1 = QStandardItem('Child {}'.format(i*3+j))
            child2 = QStandardItem('row: {}, col: {}'.format(i, j+1))
            child3 = QStandardItem('row: {}, col: {}'.format(i, j+2))
            parent1.appendRow([child1, child2, child3])
        model.appendRow(parent1)

class MultipleProxyModel(QAbstractItemModel):
    """
    This class is used to access multiple models as one. It will primarily be used as the model in the Project Explorer.
    
    How it works:
        References to 3 other models are stored as attributes of this class.
        
        Each index in this model will either be carrying a string (which acts as a label), or a reference to an index from
        one of the inner models.
        
        The indexes from the inner models are converted to QPersistentModelIndexes so that we can store them in indexes of
        this model.
        
        We have to store references to the QPersistentModelIndexes so Python's the garbage collector doesn't delete them too
        early. This requires managing references to indexes as they are created because we don't want to store infinite indexes.
    """
    def __init__(self,componentsModel,behaviorsModel,apiModulesModel):
        QAbstractItemModel.__init__(self)
        self._componentsModel = componentsModel
        self._behaviorsModel = behaviorsModel
        self._apiModulesModel = apiModulesModel
        
        
        # Storing references to all persistent indexes so they don't go out of scope and get deleted.
        # This is terribly inefficient and will eat up RAM with big projects or even with projects that are
        # open for a while.
        #
        # TODO: Figure out a more memory-efficient way to keep the persistent model indexes from going out of scope and getting deleted.
        # possible solutions:
        #   1) periodically remove persistent indexes that aren't needed anymore.
        #   2) use a data structure (possibly custom) that removes irrelevant persistent indexes.
        self._persistentIndexes = []
      

    def index(self,row,column,parent):
        if not self.hasIndex(row,column,parent):
            return QModelIndex()

        # If the parent is the ghost root, return an index with the appropriate string.
        if not parent.isValid():
            if row == 0:
                return self.createIndex(row, column, "Target GUI")

            elif row == 1:
                return self.createIndex(row, column, "API Modules")

            else:
                return QModelIndex()

        data = parent.internalPointer()
        
        # If the parent index holds a string, we'll be returning an index that holds either another string
        # or a top-level index of a sub-model.
        if isinstance(data, str):
            if data == "Target GUI":
                if row == 0:
                    return self.createIndex(row, column, "Components")
                elif row == 1:
                    return self.createIndex(row, column, "Behaviors")
                else:
                    return QModelIndex()
    
            elif data == "Components":
                pi = QPersistentModelIndex(self._componentsModel.index(row, column, QModelIndex()))
                self._persistentIndexes.append(pi)
                return self.createIndex(row, column, pi)
    
            elif data == "Behaviors":
                pi = QPersistentModelIndex(self._behaviorsModel.index(row, column, QModelIndex()))
                self._persistentIndexes.append(pi)
                return self.createIndex(row, column, pi)
            
            elif data == "API Modules":
                pi = QPersistentModelIndex(self._apiModulesModel.index(row, column, QModelIndex()))
                self._persistentIndexes.append(pi)
                return self.createIndex(row, column, pi)
            
            else:
                raise Exception("Unsupported data string: {}".format(data))

        # if the parent index is holding another index, we'll determine which model the inner index belongs to
        # and query that model for another index. We'll wrap the index that the inner model returns in another
        # index for our model.
        elif isinstance(data, QPersistentModelIndex):
            print(data.model())
            
            if self._componentsModel is data.model():
                pi = QPersistentModelIndex(self._componentsModel.index(row, column, data))
                self._persistentIndexes.append(pi)
                return self.createIndex(row, column, pi)
    
            elif self._behaviorsModel is data.model():
                pi = QPersistentModelIndex(self._behaviorsModel.index(row, column, data))
                self._persistentIndexes.append(pi)
                return self.createIndex(row, column, pi)
    
            elif self._apiModulesModel is data.model():
                pi = QPersistentModelIndex(self._apiModulesModel.index(row, column, data))
                self._persistentIndexes.append(pi)
                return self.createIndex(row, column, pi)
            
            else:
                raise Exception("Unsupported model: {}".format(data.model()))
            
        else:
            raise Exception("Unsupported data type in index: {}".format(type(data)))
            
    def parent(self,index):
        if not index.isValid():
            return QModelIndex()

        data = index.internalPointer()
        if isinstance(data, str):
            if data == "Target GUI" or data == "API Modules":
                return QModelIndex()
    
            elif data == "Components" or data == "Behaviors":
                return self.createIndex(0, 0, "Target GUI")
            
        elif isinstance(data, QPersistentModelIndex):
            print(data.model())
            if self._componentsModel is data.model():
                parent = self._componentsModel.parent(data)
                if not parent.isValid():
                    return self.createIndex(0, 0, "Components")
                else:
                    pi = QPersistentModelIndex(parent)
                    self._persistentIndexes.append(pi)
                    return self.createIndex(parent.row(), parent.column(), pi)
    
            elif self._behaviorsModel is data.model():
                parent = self._behaviorsModel.parent(data)
                if not parent.isValid():
                    return self.createIndex(1,0,"Behaviors")
                else:
                    pi = QPersistentModelIndex(parent)
                    self._persistentIndexes.append(pi)
                    return self.createIndex(parent.row(), parent.column(), pi)
    
            elif self._apiModulesModel is data.model():
                parent = self._apiModulesModel.parent(data)
                if not parent.isValid():
                    return self.createIndex(1,0,"API Modules")
                else:
                    pi = QPersistentModelIndex(parent)
                    self._persistentIndexes.append(pi)
                    return self.createIndex(parent.row(), parent.column(), pi)
                
        else:
            raise Exception("Unsupported data type in index: {}".format(type(data)))

    def rowCount(self,parent):
        if not parent.isValid():
            return 2

        data = parent.internalPointer()
        if isinstance(data, str):
            if data == "Target GUI":
                return 2
    
            elif data == "Components":
                return self._componentsModel.rowCount(QModelIndex())
    
            elif data == "Behaviors":
                return self._behaviorsModel.rowCount(QModelIndex())
    
            elif data == "API Modules":
                return self._apiModulesModel.rowCount(QModelIndex())
            
        elif isinstance(data, QPersistentModelIndex):
            print(data.model())
            if self._componentsModel is data.model():
                return self._componentsModel.rowCount(data)
    
            elif self._behaviorsModel is data.model():
                return self._behaviorsModel.rowCount(data)
    
            elif self._apiModulesModel is data.model():
                return self._apiModulesModel.rowCount(data)
            
        else:
            raise Exception("Unsupported data type in index: {}".format(type(data)))

    def columnCount(self,parent):
        return 2

    def flags(self,index):
        if not index.isValid():
            return Qt.NoItemFlags

        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable 

    def data(self,index,role):
        if not index.isValid():
            return None

        elif role != Qt.DisplayRole:
            return None

        data = index.internalPointer()
        col = index.column()
        row = index.row()

        if isinstance(data, str):
            if col == 0:
                return data
            else:
                return None
                
        elif isinstance(data, QPersistentModelIndex):
            if self._componentsModel is data.model():
                return self._componentsModel.data(data,role)
    
            elif self._behaviorsModel is data.model():
                return self._behaviorsModel.data(data,role)
    
            elif self._apiModulesModel is data.model():
                return self._apiModulesModel.data(data,role)
            
        else:
            raise Exception("Unsupported data type in index: {}".format(type(data)))
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ["Name", "Description"][section]
