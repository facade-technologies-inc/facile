from PySide2.QtGui import QStandardItem
from PySide2.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt, Signal
from data.project import Project
from data.tguim.guicomponent import GUIComponent
from data.tguim.visibilitybehavior import VisibilityBehavior
from data.apim.actionpipeline import ActionPipeline

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

# TODO: Update this file once Sean integrates his code.


class ProjectExplorerModel(QAbstractItemModel):
	
	componentSelected = Signal(object)
	behaviorSelected = Signal(object)
	pipelineSelected = Signal(object)
	
	TARGET_GUI_LABEL = "Target GUI"
	COMPONENT_LABEL = "GUI Components"
	BEHAVIOR_LABEL = "Visibility Behaviors"
	PIPELINE_LABEL = "Action Pipelines"
	
	NO_COMPONENTS_LABEL = "No GUI Components Yet."
	NO_BEHAVIORS_LABEL = "No Visibility Behaviors Yet."
	NO_PIPELINES_LABEL = "No Action Pipelines Yet."
	
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
			
	class UnsupportedTypeException(Exception):
		def __init__(self, msg):
			Exception.__init__(self, msg)
			
	class InvalidSelectionException(Exception):
		def __init__(self, msg):
			Exception.__init__(self, msg)
	#################################################
	#           END EXCEPTION DEFINITIONS           #
	#################################################

	def __init__(self, project: Project) -> 'ProjectExplorerModel':
		QAbstractItemModel.__init__(self)
		self._project = project
	
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

		parentData = parent.internalPointer()
	
		# If the parent index holds a string, we'll be returning an index that holds either another string
		# or a top-level index of a sub-model.
		if isinstance(parentData, str):
			if parentData == ProjectExplorerModel.TARGET_GUI_LABEL:
				if row == ProjectExplorerModel.COMPONENT_ROW:
					return self.createIndex(row, column, ProjectExplorerModel.COMPONENT_LABEL)
				elif row == ProjectExplorerModel.BEHAVIOR_ROW:
					return self.createIndex(row, column, ProjectExplorerModel.BEHAVIOR_LABEL)
				else:
					return QModelIndex()
	
			elif parentData == ProjectExplorerModel.COMPONENT_LABEL:
				
				if self._project.getTargetGUIModel().getRoot().getNumChildren() == 0:
					return self.createIndex(row, column, (ProjectExplorerModel.NO_COMPONENTS_LABEL, ProjectExplorerModel.COMPONENT_LABEL, 0))
				return self.createIndex(row, column, self._project.getTargetGUIModel().getRoot().getNthChild(row))
			elif parentData == ProjectExplorerModel.BEHAVIOR_LABEL:
				
				if self._project.getTargetGUIModel().getNumVisibilityBehaviors() == 0:
					return self.createIndex(row, column, (ProjectExplorerModel.NO_BEHAVIORS_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL, q))
				return self.createIndex(row, column, self._project.getTargetGUIModel().getNthBehavior(row))
			elif parentData == ProjectExplorerModel.PIPELINE_LABEL:
				# TODO: replace this once action pipelines are implemented
				return self.createIndex(row, column, (ProjectExplorerModel.NO_PIPELINES_LABEL, parentData, 1))
			else:
				raise ProjectExplorerModel.InvalidLabelException("Unsupported data string: {}".format(parentData))
			
		elif isinstance(parentData, GUIComponent):
			
			return self.createIndex(row, column, parentData.getNthChild(row))
			
		elif isinstance(parentData, VisibilityBehavior):
			if row == 0:
				
				return self.createIndex(row, column, (parentData.getFromComponent(), parentData))
			if row == 1:
				
				return self.createIndex(row, column, (parentData.getToComponent(), parentData))
			
		elif isinstance(parentData, ActionPipeline):
			# TODO: replace this once action pipelines are implemented
			pass
			
		elif isinstance(parentData, tuple):
			# If the internal pointer is a tuple, it should have no children.
			pass
		
		else:
			raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(parentData)))
		
	def parent(self, index: QModelIndex) -> QModelIndex:
		if not index.isValid():
			return QModelIndex()

		data = index.internalPointer()
		if isinstance(data, str):
			if data in (ProjectExplorerModel.TARGET_GUI_LABEL, ProjectExplorerModel.PIPELINE_LABEL):
				return QModelIndex()
	
			elif data in (ProjectExplorerModel.COMPONENT_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL):
				return self.createIndex(0, 0, ProjectExplorerModel.TARGET_GUI_LABEL)
			
		elif isinstance(data, GUIComponent):
			
			parentComponent = data.getParent()
			
			if parentComponent is self._project.getTargetGUIModel().getRoot():
				return self.createIndex(0, 0, ProjectExplorerModel.COMPONENT_LABEL)
			else:
				
				return self.createIndex(parentComponent.getRow(), 0, parentComponent)
			
		elif isinstance(data, VisibilityBehavior):
			
			return self.createIndex(1, 0, ProjectExplorerModel.BEHAVIOR_LABEL)
		
		elif isinstance(data, ActionPipeline):
			# TODO: replace this once action pipelines are implemented
			pass
		
		elif isinstance(data, tuple):
			innerData = data[0]
			if isinstance(innerData, str):
				return self.createIndex(data[2], 0, data[1])
			
			elif isinstance(innerData, GUIComponent):
				# data[1] will be a visibility behavior
				
				return self.createIndex(data[1].getRow(), 0, data[1])
			
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
				return max(1, self._project.getTargetGUIModel().getRoot().getNumChildren())
	
			elif data == ProjectExplorerModel.BEHAVIOR_LABEL:
				return max(1, self._project.getTargetGUIModel().getNumVisibilityBehaviors())
	
			elif data == ProjectExplorerModel.PIPELINE_LABEL:
				# TODO: replace this once action pipelines are implemented
				return 1
			
		elif isinstance(data, GUIComponent):
			return data.getNumChildren()
		
		elif isinstance(data, VisibilityBehavior):
			return 2
		
		elif isinstance(data, tuple):
			return 0
			
		elif isinstance(data, ActionPipeline):
			# TODO: replace this once action pipelines are implemented
			pass
		
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
		
		elif isinstance(data, GUIComponent):
			if col == 0:
				return data.getName()
			elif col == 1:
				return data.getType()
			else:
				return None
		
		elif isinstance(data, VisibilityBehavior):
			if col == 0:
				return data.getName()
			elif col == 1:
				return data.getType()
			else:
				return None
		
		elif isinstance(data, ActionPipeline):
			if col == 0:
				return data.getName()
			elif col == 1:
				return data.getType()
			else:
				return None
			
		elif isinstance(data, tuple):
			innerData = data[0]
			if isinstance(innerData, str):
				if col == 0:
					return innerData
				else:
					return None
				
			if isinstance(innerData, GUIComponent):
				if row == 0:
					if col == 0:
						return "From"
					elif col == 1:
						return innerData.getName()
					else:
						return None
				if row == 1:
					if col == 0:
						return "To"
					elif col == 1:
						return innerData.getName()
					else:
						return None
		
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