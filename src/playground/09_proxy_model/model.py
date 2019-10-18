from PySide2.QtGui import QStandardItem
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt

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
    def __init__(self,componentsModel,behaviorsModel,apiModulesModel):
        QAbstractItemModel.__init__(self)
        self._componentsModel = componentsModel
        self._behaviorsModel = behaviorsModel
        self._apiModulesModel = apiModulesModel
      

    def index(self,row,column,parent):
        if not self.hasIndex(row,column,parent):
            return QModelIndex()

        if not parent.isValid():
            if column != 0:
                return QModelIndex()
            elif row == 0:
                return self.createIndex(row,column,"Target GUI")

            elif row == 1:
                return self.createIndex(row,column,"API Modules")

            else:
                return QModelIndex()

        if self._componentsModel.checkIndex(parent):
            return self._componentsModel.index(row,column,parent)

        elif self._behaviorsModel.checkIndex(parent):
            return self._behaviorsModel.index(row,column,parent)

        elif self._apiModulesModel.checkIndex(parent):
            return self._apiModulesModel.index(row,column,parent)
            

        data = parent.internalPointer()
       

        if data == "Target GUI":
            if column != 0:
                return QModelIndex()
            elif row == 0:
                return self.createIndex(row,column, "Components")
            elif row == 1:
                return self.createIndex(row,column, "Behaviors")
            else:
                return QModelIndex()

        elif data == "API Modules":
            return self._apiModulesModel.index(row,column,QModelIndex())

        elif data == "Components":
            return self._componentsModel.index(row,column,QModelIndex())

        elif data == "Behaviors":
            return self._behaviorsModel.index(row,column,QModelIndex())




    def parent(self,index):
        if not index.isValid():
            return QModelIndex()

        if self._componentsModel.checkIndex(index):
            parent = self._componentsModel.parent(index)
            if not parent.isValid():
                return self.createIndex(0,0,"Components")
            else:
                return parent

        elif self._behaviorsModel.checkIndex(index):
            parent = self._behaviorsModel.parent(index)
            if not parent.isValid():
                return self.createIndex(0,0,"Behaviors")
            else:
                return parent

        elif self._apiModulesModel.checkIndex(index):
            parent = self._apiModulesModel.parent(index)
            if not parent.isValid():
                return self.createIndex(0,0,"API Modules")
            else:
                return parent

        data = index.internalPointer()

        if data == "Target GUI" or data == "API Modules":
            return QModelIndex()

        elif data == "Components" or data == "Behaviors":
            return self.createIndex(0,0,"Target GUI")

        


    def rowCount(self,parent):
        if not parent.isValid():
            return 2

        if self._componentsModel.checkIndex(parent):
            return self._componentsModel.rowCount(parent)

        elif self._behaviorsModel.checkIndex(parent):
            return self._behaviorsModel.rowCount(parent)

        elif self._apiModulesModel.checkIndex(parent):
            return self._apiModulesModel.rowCount(parent)

        data = parent.internalPointer()

        if data == "Target GUI":
            return 2

        elif data == "Components":
            return self._componentsModel.rowCount(QModelIndex())

        elif data == "Behaviors":
            return self._behaviorsModel.rowCount(QModelIndex())

        elif data == "API Modules":
            return self._apiModulesModel.rowCount(QModelIndex())

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

        elif self._componentsModel.checkIndex(index):
            return self._componentsModel.data(index,role)

        elif self._behaviorsModel.checkIndex(index):
            return self._behaviorsModel.data(index,role)

        elif self._apiModulesModel.checkIndex(index):
            return self._apiModulesModel.data(index,role)
        
        data = index.internalPointer()
        col = index.column()

        if col != 0:
            return None

        else:
            return data



    def headerData(self,section,orientation,role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ["Name", "Description"][section]







   
        