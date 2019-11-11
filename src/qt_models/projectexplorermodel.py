"""
/------------------------------------------------------------------------------\
|                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
|------------------------------------------------------------------------------|
|                                                                              |
|    Copyright [2019] Facade Technologies Inc.                                 |
|    All Rights Reserved.                                                      |
|                                                                              |
| NOTICE:  All information contained herein is, and remains the property of    |
| Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
| and technical concepts contained herein are proprietary to Facade            |
| Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
| Patents, patents in process, and are protected by trade secret or copyright  |
| law.  Dissemination of this information or reproduction of this material is  |
| strictly forbidden unless prior written permission is obtained from Facade   |
| Technologies Inc.                                                            |
|                                                                              |
\------------------------------------------------------------------------------/

This is module contains the Qt model for the project explorer.

"""

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt, Signal, QItemSelection
from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior
from data.apim.actionpipeline import ActionPipeline


class ProjectExplorerModel(QAbstractItemModel):
	"""
	This class is the Qt model that gets loaded into the project explorer view in Facile.
	It has the following hierarchy:
	
	== Target GUI ==
		== GUI Components ==
			component-1
				component-2
				component-3
					component-4
					component-5
				component-6
					component-7
			component-8
				component-9
			component-10
		== Visibility Behaviors ==
			visibility-behavior-1
				from-component
				to-component
			visibility-behavior-2
				from-component
				to-component
			visibility-behavior-3
				from-component
				to-component
	== Action Pipelines ==
		action-pipeline-1
			action-pipeline-2
				action-pipeline-3
			action-pipeline-4
		action-pipeline-5
		action-pipeline-6
		
	The internal pointer of the model indexes can be
		- str (for a label)
		- Component
		- Visibility Behavior
		- Action Pipeline
		- tuple (see below)
		
	If the internal pointer is a tuple, it will take the following format
		- index 0 (required) contains the data to be shown in the index - either a str or Component
		- index 1 (required) contains the parent data.
		- index 2 (optional) contains the parent's row.
	"""
	
	componentSelected = Signal(Component)
	behaviorSelected = Signal(VisibilityBehavior)
	pipelineSelected = Signal(ActionPipeline)
	
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
		"""
		This exception should be thrown when an invalid label is found in the model.
		"""
		
		def __init__(self, msg: str) -> 'InvalidLabelException':
			"""
			Constructs an InvalidLabelException object
			
			:param msg: The message to be carried in the exception
			:type msg: str
			"""
			Exception.__init__(self, msg)
			
	class UnsupportedTypeException(Exception):
		"""
		This exception should be thrown when an unsupported type is carried in a QModelIndex
		"""
		
		def __init__(self, msg: str) -> 'UnsupportedTypeException':
			"""
			Constructs an UnsupportedTypeException object
			
			:param msg: The message to be carried in the exception
			:type msg: str
			"""
			Exception.__init__(self, msg)
			
	class InvalidSelectionException(Exception):
		"""
		This exception should be thrown when an a selection is illegal
		"""
		
		def __init__(self, msg: str) -> 'InvalidSelectionException':
			"""
			Constructs an InvalidSelectionException object

			:param msg: The message to be carried in the exception
			:type msg: str
			"""
			Exception.__init__(self, msg)
	#################################################
	#           END EXCEPTION DEFINITIONS           #
	#################################################

	def __init__(self, project: 'Project') -> 'ProjectExplorerModel':
		"""
		Constructs a ProjectExplorerModel exception
		
		:param project: A Facile project object.
		:type project: Project
		"""
		QAbstractItemModel.__init__(self)
		self._project = project
	
	def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
		"""
		Gets a model index given the parent index, row, and column.
		
		:param row: the index of the rowth child of "parent".
		:type row: int
		:param column: the column of the index to be created.
		:type column: int
		:param parent: the parent of the index to be created.
		:type parent: QModelIndex
		:return: the model index with the given parent, row, and column.
		:rtype: QModelIndex
		"""
		
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
					return self.createIndex(row, column, (ProjectExplorerModel.NO_BEHAVIORS_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL, 0))
				
				return self.createIndex(row, column, self._project.getTargetGUIModel().getNthBehavior(row))
			
			elif parentData == ProjectExplorerModel.PIPELINE_LABEL:
				# TODO: replace this once action pipelines are implemented
				return self.createIndex(row, column, (ProjectExplorerModel.NO_PIPELINES_LABEL, parentData, 1))
			
			else:
				raise ProjectExplorerModel.InvalidLabelException("Unsupported data string: {}".format(parentData))
			
		elif isinstance(parentData, Component):
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
		"""
		Creates a model index for the parent of the given index.
		
		:param index: the index to get the parent of.
		:type index: QModelIndex
		:return: The parent index of the index provided.
		:rtype: QModelIndex
		"""
		if not index.isValid():
			return QModelIndex()

		data = index.internalPointer()
		if isinstance(data, str):
			if data in (ProjectExplorerModel.TARGET_GUI_LABEL, ProjectExplorerModel.PIPELINE_LABEL):
				return QModelIndex()
	
			elif data in (ProjectExplorerModel.COMPONENT_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL):
				return self.createIndex(0, 0, ProjectExplorerModel.TARGET_GUI_LABEL)
			
		elif isinstance(data, Component):
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
			
			elif isinstance(innerData, Component):
				return self.createIndex(data[1].getRow(), 0, data[1])
			
		else:
			raise ProjectExplorerModel.UnsupportedTypeException("Unsupported data type in index: {}".format(type(data)))

	def rowCount(self, parent: QModelIndex) -> int:
		"""
		Get the number of rows for a given index.
		
		:param parent: the index to get the number of rows in.
		:type parent: QModelIndex
		:return: The number of rows (children) underneath the given index.
		:rtype: int
		"""
		if not parent.isValid():
			return 2

		data = parent.internalPointer()
		if isinstance(data, str):
			if data == ProjectExplorerModel.TARGET_GUI_LABEL:
				return 2
	
			elif data == ProjectExplorerModel.COMPONENT_LABEL:
				return max(1, self._project.getTargetGUIModel().getRoot().getNumChildren())
	
			elif data == ProjectExplorerModel.BEHAVIOR_LABEL:
				return max(1, len(self._project.getTargetGUIModel().getVisibilityBehaviors()))
	
			elif data == ProjectExplorerModel.PIPELINE_LABEL:
				# TODO: replace this once action pipelines are implemented
				return 1
			
		elif isinstance(data, Component):
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
		"""
		Gets the number of columns on the next level of a given index.
		In our case, there will always be 2 columns.
		
		:param parent: The index of which to get the number of columns under.
		:type parent: QModelIndex
		:return: the number of columns under the given index.
		:rtype: int
		"""
		return 2

	def flags(self, index: QModelIndex) -> Qt.ItemFlags:
		"""
		Get the flags associated with the given index
		
		:param index: the index to get the flags for
		:type index: QModelIndex
		:return: The flags with a given index
		:rtype: Qt.ItemFlags
		"""
		if not index.isValid():
			return Qt.NoItemFlags

		else:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable

	def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> str:
		"""
		Gets the data associated with a specific index and the specific role.
		
		:param index: The index to get the data from
		:type index: QModelIndex
		:param role: The role to use to get the data.
		:type role: Qt.ItemDataRole
		:return: The data for the given role
		:rtype: str
		"""
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
		
		elif isinstance(data, Component):
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
				
			if isinstance(innerData, Component):
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
		
	def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.DisplayRole) -> str:
		"""
		Gets the header data.
		
		:param section: either the row or the column depending on the orientation.
		:type section: int
		:param orientation: Qt.Horizontal for header on top or Qt.Vertical for header on the left
		:type orientation: Qt.Orientation
		:param role: the role to use to get the data.
		:type role: Qt.ItemDataRole
		:return: the data
		;rtype: str
		"""
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return ["Name", "Description"][section]

	def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
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

				elif isinstance(data, Component):
					self.componentSelected.emit(data)
				
				elif isinstance(data, VisibilityBehavior):
					self.behaviorSelected.emit(data)
					
				elif isinstance(data, ActionPipeline):
					self.pipelineSelected.emit(data)
					
				elif isinstance(data, tuple):
					if isinstance(data[0], Component):
						self.componentSelected.emit(data[0])
			else:
				raise ProjectExplorerModel.InvalidSelectionException("Multiple row selection is not supported")