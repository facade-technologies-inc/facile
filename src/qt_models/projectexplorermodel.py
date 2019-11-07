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
		internalPointer = ret.internalPointer()
		if isinstance(internalPointer, str):
			print("{} {} {}".format(ret.row(), ret.column(), internalPointer))
		else:
			print("{} {} {}".format(ret.row(), ret.column(), ret.internalPointer()[1]))
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
	
	MODEL = 0
	PATH = 1
	
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
	
	@debug
	def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
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
				model = self._componentsModel
			elif data == ProjectExplorerModel.BEHAVIOR_LABEL:
				model = self._behaviorsModel
			elif data == ProjectExplorerModel.PIPELINE_LABEL:
				model = self._apiModel
			else:
				raise ProjectExplorerModel.InvalidLabelException("Unsupported data string: {}".format(data))
			
			return self.createIndex(row, column, (model, [row]))
			
		elif isinstance(data, tuple):
			model = data[ProjectExplorerModel.MODEL]
			path = data[ProjectExplorerModel.PATH] + [row]
			
			if model not in (self._componentsModel, self._behaviorsModel, self._apiModel):
				raise ProjectExplorerModel.UnknownModelException("Unsupported model: {}".format(data.model()))
			
			return self.createIndex(row, column, (model, path))
		
		else:
			raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(data)))
		
	def parent(self, index: QModelIndex) -> QModelIndex:
		if not index.isValid():
			return QModelIndex()

		data = index.internalPointer()
		if isinstance(data, str):
			if data in (ProjectExplorerModel.TARGET_GUI_LABEL, ProjectExplorerModel.PIPELINE_LABEL):
				return QModelIndex()
	
			elif data in (ProjectExplorerModel.COMPONENT_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL):
				return self.createIndex(0, 0, ProjectExplorerModel.TARGET_GUI_LABEL)
			
		elif isinstance(data, tuple):
			model = data[ProjectExplorerModel.MODEL]
			path = data[ProjectExplorerModel.PATH][:-1]
			
			if model not in (self._componentsModel, self._behaviorsModel, self._apiModel):
				raise ProjectExplorerModel.UnknownModelException("Unsupported model: {}".format(data.model()))
			
			parent = ProjectExplorerModel.getInternalModelIndex(model, path)
			
			if not parent.isValid():
				if data.model() is self._componentsModel:
					label = ProjectExplorerModel.COMPONENT_LABEL
					row = ProjectExplorerModel.COMPONENT_ROW
				elif data.model() is self._behaviorsModel:
					label = ProjectExplorerModel.BEHAVIOR_LABEL
					row = ProjectExplorerModel.BEHAVIOR_ROW
				elif data.model() is self._apiModel:
					label = ProjectExplorerModel.PIPELINE_LABEL
					row = ProjectExplorerModel.PIPELINE_ROW
				return self.createIndex(row, 0, label)
			
			return self.createIndex(path[-1], 0, (model, path))

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
			
		elif isinstance(data, tuple):
			model = data[ProjectExplorerModel.MODEL]
			path = data[ProjectExplorerModel.PATH]
			print(type(model), type(path))
			internalIndex = ProjectExplorerModel.getInternalModelIndex(model, path)
			return model.rowCount(internalIndex)
			
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
				
		elif isinstance(data, tuple):
			model = data[ProjectExplorerModel.MODEL]
			path = data[ProjectExplorerModel.PATH]
			internalIndex = ProjectExplorerModel.getInternalModelIndex(model, path, column = index.column())
			return model.data(internalIndex, role)
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

	@staticmethod
	def getInternalModelIndex(internalModel, path, column=0):
		curIndex = QModelIndex() #Start with root
		for i in range(path):
			row = path[i]
			if i == len(path) - 1:
				col = column
			else:
				col = 0
				
			if internalModel.rowCount(curIndex) <= row:
				raise Exception("Bad path")
			if internalModel.columnCount(curIndex) <= col:
				raise Exception("Bad path")
				
			curIndex = internalModel.index(row, col, curIndex)
			
		return curIndex
			