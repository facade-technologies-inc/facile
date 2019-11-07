from PySide2.QtGui import QStandardItem
from PySide2.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt, Signal

# TODO: Remove this once we have the actual models from the target GUI model and the the api model
def pop_standard_model(model):
    for i in range(3):
        parent1 = QStandardItem('Family {}. Some long status text for sp'.format(i))
        parent2 = QStandardItem("Family details")
        for j in range(3):
            child1 = QStandardItem('Child {}'.format(i*3+j))
            child2 = QStandardItem('Some details')
            parent1.appendRow([child1, child2])
        model.appendRow([parent1, parent2])

def debug(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print("{} {} {} {}".format(ret.row(), ret.column(), ret.data(), ret.internalPointer()))
        return ret
    
    return wrapper
    

class ProjectExplorerModel(QAbstractItemModel):
    """
    This class is used to access multiple models as one. It will primarily be used as the model in the Project Explorer.
    
    How it works:
        References to multiple other models are stored as attributes of this class.
        
        Each index in this model will either be carrying a string (which acts as a label), or a reference to an index
        from one of the inner models.
        
        The indexes from the inner models are converted to QPersistentModelIndexes so that we can store them in indexes
        of this model.
        
        We have to store references to the QPersistentModelIndexes so Python's the garbage collector doesn't delete them
        too early. This requires managing references to indexes as they are created because we don't want to store
        infinite indexes.
    """
    componentSelected = Signal(object)
    behaviorSelected = Signal(object)
    pipelineSelected = Signal(object)
    
    TARGET_GUI_LABEL = "Target GUI"
    COMPONENT_LABEL = "GUI Components"
    BEHAVIOR_LABEL = "Visibility Behaviors"
    PIPELINE_LABEL = "Action Pipelines"
    
    TARGET_GUI_ROW = 0
    COMPONENT_ROW = 0
    BEHAVIOR_ROW = 1
    PIPELINE_ROW = 1
    
    #################################################
    #          BEGIN EXCEPTION DEFINITIONS          #
    #################################################
    class InvalidLabelException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)
            
    class UnknownModelException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)
            
    class UnsupportedTypeException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)
            
    class InvalidSelectionException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)
    #################################################
    #           END EXCEPTION DEFINITIONS           #
    #################################################

    def __init__(self, componentsModel, behaviorsModel, apiModel):
        QAbstractItemModel.__init__(self)
        self._componentsModel = componentsModel
        self._behaviorsModel = behaviorsModel
        self._apiModel = apiModel
        
        self._labelIndexes = {
            ProjectExplorerModel.TARGET_GUI_LABEL: [None, None],
            ProjectExplorerModel.COMPONENT_LABEL:  [None, None],
            ProjectExplorerModel.BEHAVIOR_LABEL:   [None, None],
            ProjectExplorerModel.PIPELINE_LABEL:   [None, None]
        }
        
        # Storing references to all persistent indexes so they don't go out of scope and get deleted.
        # This is terribly inefficient and will eat up RAM with big projects or even with projects that are
        # open for a while.
        #
        #TODO: Figure out a more memory-efficient way to keep the persistent model indexes from going out of scope and getting deleted.
        # possible solutions:
        #   1) periodically remove persistent indexes that aren't needed anymore.
        #   2) use a data structure (possibly custom) that removes irrelevant persistent indexes.
        self._persistentIndexes = []
    
    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        #print("index: {} {} {}".format(parent.row(), parent.column(), parent.data()))
        # print(len(self._persistentIndexes))
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        # If the parent is the ghost root, return an index with the appropriate string.
        if not parent.isValid():
            if row == ProjectExplorerModel.TARGET_GUI_ROW:
                return self.createIndex(row, column, ProjectExplorerModel.TARGET_GUI_LABEL)
            elif row == ProjectExplorerModel.PIPELINE_ROW:
                return self.createIndex(row, column, ProjectExplorerModel.PIPELINE_LABEL)
            else:
                return QModelIndex()

        data = parent.internalPointer()
        
        # If the parent index holds a string, we'll be returning an index that holds either another string
        # or a top-level index of a sub-model.
        if isinstance(data, str):
            if data == ProjectExplorerModel.TARGET_GUI_LABEL:
                if row == ProjectExplorerModel.COMPONENT_ROW:
                    return self.createIndex(row, column, ProjectExplorerModel.COMPONENT_LABEL)
                elif row == ProjectExplorerModel.BEHAVIOR_ROW:
                    return self.createIndex(row, column, ProjectExplorerModel.BEHAVIOR_LABEL)
                else:
                    return QModelIndex()
    
            elif data == ProjectExplorerModel.COMPONENT_LABEL:
                internalModel = self._componentsModel
            elif data == ProjectExplorerModel.BEHAVIOR_LABEL:
                internalModel = self._behaviorsModel
            elif data == ProjectExplorerModel.PIPELINE_LABEL:
                internalModel = self._apiModel
            else:
                raise ProjectExplorerModel.InvalidLabelException("Unsupported data string: {}".format(data))

            pi = QPersistentModelIndex(internalModel.index(row, column, QModelIndex()))
            self.registerPersistentIndex(pi)
            return self.createIndex(row, column, pi)

        # if the parent index is holding another index, we'll determine which model the inner index belongs to
        # and query that model for another index. We'll wrap the index that the inner model returns in another
        # index for our model.
        elif isinstance(data, QPersistentModelIndex):
            if data.model() not in (self._componentsModel, self._behaviorsModel, self._apiModel):
                raise ProjectExplorerModel.UnknownModelException("Unsupported model: {}".format(data.model()))

            pi = QPersistentModelIndex(data.model().index(row, column, data))
            self.registerPersistentIndex(pi)
            return self.createIndex(row, column, pi)
        
        else:
            raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(data)))
            
    @debug
    def parent(self, index: QModelIndex) -> QModelIndex:
        #print("parent: {} {} {}".format(index.row(), index.column(), index.data()))
        # TODO: Fix runtimewarning. Returning none instead of QModelIndex
        if not index.isValid():
            return QModelIndex()

        data = index.internalPointer()
        if isinstance(data, str):
            if data in (ProjectExplorerModel.TARGET_GUI_LABEL, ProjectExplorerModel.PIPELINE_LABEL):
                return QModelIndex()
    
            elif data in (ProjectExplorerModel.COMPONENT_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL):
                return self.createIndex(0, 0, ProjectExplorerModel.TARGET_GUI_LABEL)
            
        elif isinstance(data, QPersistentModelIndex):
            
            if data.model() not in (self._componentsModel, self._behaviorsModel, self._apiModel):
                raise ProjectExplorerModel.UnknownModelException("Unsupported model: {}".format(data.model()))
            
            parent = data.model().parent(data)

            if not parent.isValid():
                if data.model() is self._componentsModel:
                    label = ProjectExplorerModel.COMPONENT_LABEL
                    row = 0
                elif data.model() is self._behaviorsModel:
                    label = ProjectExplorerModel.BEHAVIOR_LABEL
                    row = 1
                elif data.model() is self._apiModel:
                    label = ProjectExplorerModel.PIPELINE_LABEL
                    row = 1
                return self.createIndex(row, 0, label)
            
            pi = QPersistentModelIndex(parent)
            self.registerPersistentIndex(pi)
            return self.createIndex(parent.row(), 0, pi)

        else:
            raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(data)))

    def rowCount(self, parent: QModelIndex) -> int:
        if not parent.isValid():
            return 2

        data = parent.internalPointer()
        if isinstance(data, str):
            if data == ProjectExplorerModel.TARGET_GUI_LABEL:
                return 2
    
            elif data == ProjectExplorerModel.COMPONENT_LABEL:
                return self._componentsModel.rowCount(QModelIndex())
    
            elif data == ProjectExplorerModel.BEHAVIOR_LABEL:
                return self._behaviorsModel.rowCount(QModelIndex())
    
            elif data == ProjectExplorerModel.PIPELINE_LABEL:
                return self._apiModel.rowCount(QModelIndex())
            
        elif isinstance(data, QPersistentModelIndex):
            if self._componentsModel is data.model():
                return self._componentsModel.rowCount(data)
    
            elif self._behaviorsModel is data.model():
                return self._behaviorsModel.rowCount(data)
    
            elif self._apiModel is data.model():
                return self._apiModel.rowCount(data)
            
        else:
            raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(data)))

    def columnCount(self, parent: QModelIndex) -> int:
        return 2

    def flags(self, index: QModelIndex) -> int:
        if not index.isValid():
            return Qt.NoItemFlags

        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable 

    def data(self, index: QModelIndex, role: int) -> str:
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
    
            elif self._apiModel is data.model():
                return self._apiModel.data(data, role)
            
        else:
            raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(data)))
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return ["Name", "Description"][section]

    def onSelectionChanged(self, selected, deselected):
        listSelected = selected.indexes()

        if len(listSelected) > 0:
            rows = set()
            for i in listSelected:
                rows.add(i.row())
            if len(rows) == 1:
                index = listSelected[0]
                data = index.internalPointer()

                if isinstance(data, str):
                    return None

                elif isinstance(data, QPersistentModelIndex):
                
                    if self._componentsModel is data.model():
                        self.componentSelected.emit(data.internalPointer())
            
                    elif self._behaviorsModel is data.model():
                        self.behaviorSelected.emit(data.internalPointer())
            
                    elif self._apiModel is data.model():
                        self.pipelineSelected.emit(data.internalPointer())

            else:
                raise ProjectExplorerModel.InvalidSelectionException("Multiple row selection is not supported")

    def registerPersistentIndex(self, pi: QPersistentModelIndex) -> bool:
        self._persistentIndexes.append(pi)
        return False
