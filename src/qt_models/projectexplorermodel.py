"""
..
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

This module contains the Qt model for the project explorer.

"""

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt, Signal, Slot, QItemSelection
from PySide2.QtCore import QItemSelectionModel, QPoint
from PySide2.QtGui import QIcon, QColor, QPixmap
from PySide2.QtWidgets import QTreeView

from data.apim.actionpipeline import ActionPipeline
from data.tguim.component import Component
from data.tguim.visibilitybehavior import VisibilityBehavior
import data.statemachine as sm
from qt_models.componentmenu import ComponentMenu

class ProjectExplorerModel(QAbstractItemModel):
	"""
	This class is the Qt model that gets loaded into the project explorer view in Facile.
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
	
	class LeafIndex:
		"""
		This class holds the information for a QModelIndex as well as its parent and the row of the parent.
		If a QModelIndex holds this object as its internal pointer, the QModelIndex will have no children.
		"""
		
		def __init__(self, me: object, parent: object, parentIndex: int = None) -> 'LeafIndex':
			"""
			Constructs a LeafIndex object.
			
			:param me: The data for a QModelIndex.
			:type me: object
			:param parent: The data for the parent QModelIndex.
			:type parent: object
			:param parentIndex: The row of the parent.
			:type parentIndex: int
			"""
			self._data = me
			self._parentData = parent
			self._parentIndex = parentIndex
		
		def getData(self):
			"""
			Gets the internal data of the current index.
			
			:return: the data for the current index.
			:rtype: object
			"""
			return self._data
		
		def getParent(self):
			"""
			Gets the internal data of the parent index.

			:return: the data for the parent index.
			:rtype: object
			"""
			return self._parentData
		
		def getParentIndex(self):
			"""
			Gets the row of the parent.
			
			:return: the row of the parent
			:rtype: int
			"""
			return self._parentIndex
		
		def __eq__(self, other: 'LeafIndex') -> bool:
			"""
			Determine if 2 LeafIndex objects are equal.
			2 LeafIndex objects are equal if they have all the same data.
			
			:param other: the other leaf index to compare to.
			:type other: LeafIndex
			:return: True if they're equal, False otherwise
			:rtype: bool
			"""
			if self.getData() != other.getData():
				return False
			elif self.getParent() != other.getParent():
				return False
			elif self.getParentIndex() != other.getParentIndex():
				return False
			else:
				return True
		
		def __ne__(self, other: 'LeafIndex') -> bool:
			"""
			Determine if 2 LeafIndex objects are not equal. This is the inverse of the __eq__ function
			
			:param other: the other leaf index to compare to.
			:type other: LeafIndex
			:return: False if they're equal, True otherwise
			:rtype: bool
			"""
			return not self.__eq__(other)
		
		def __hash__(self) -> int:
			"""
			Get the Hash for a LeafIndex object. LeafIndex objects with all of the same data will have the same hash.
			
			:return: The hash of the LeafIndex object
			:rtype: int
			"""
			return hash(frozenset((self._data, self._parentData, self._parentIndex)))
	
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
	
	def __init__(self, project: 'Project', view: QTreeView) -> 'ProjectExplorerModel':
		"""
		Constructs a ProjectExplorerModel exception
		
		:param project: A Facile project object.
		:type project: Project
		"""
		QAbstractItemModel.__init__(self)
		self._project = project
		self._view = view
		
		# Data structures that let us efficiently store references to internal data without hogging exorbitant amounts
		# of memory.
		self._registryCounter = 0
		self._forwardRegistry = {}
		self._backwardRegistry = {}
	
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
				return self.registerAndCreateIndex(row, column,
				                                   ProjectExplorerModel.TARGET_GUI_LABEL)
			
			elif row == ProjectExplorerModel.PIPELINE_ROW:
				return self.registerAndCreateIndex(row, column, ProjectExplorerModel.PIPELINE_LABEL)
			
			else:
				return QModelIndex()
		
		parentData = parent.internalPointer()
		if isinstance(parentData, str):
			if parentData == ProjectExplorerModel.TARGET_GUI_LABEL:
				if row == ProjectExplorerModel.COMPONENT_ROW:
					return self.registerAndCreateIndex(row, column,
					                                   ProjectExplorerModel.COMPONENT_LABEL)
				
				elif row == ProjectExplorerModel.BEHAVIOR_ROW:
					return self.registerAndCreateIndex(row, column,
					                                   ProjectExplorerModel.BEHAVIOR_LABEL)
				
				else:
					return QModelIndex()
			
			elif parentData == ProjectExplorerModel.COMPONENT_LABEL:
				if self._project.getTargetGUIModel().getRoot().childCount() == 0:
					return self.registerAndCreateIndex(row, column, ProjectExplorerModel.LeafIndex(
						ProjectExplorerModel.NO_COMPONENTS_LABEL, parentData, 0))
				
				return self.registerAndCreateIndex(row, column,
				                                   self._project.getTargetGUIModel().getRoot().getNthChild(
					                                   row))
			
			elif parentData == ProjectExplorerModel.BEHAVIOR_LABEL:
				if len(self._project.getTargetGUIModel().getVisibilityBehaviors()) == 0:
					return self.registerAndCreateIndex(row, column, ProjectExplorerModel.LeafIndex(
						ProjectExplorerModel.NO_BEHAVIORS_LABEL, parentData, 0))
				
				return self.registerAndCreateIndex(row, column,
				                                   self._project.getTargetGUIModel().getNthVisibilityBehavior(
					                                   row))
			
			elif parentData == ProjectExplorerModel.PIPELINE_LABEL:
				# TODO: replace this once action pipelines are implemented
				return self.registerAndCreateIndex(row, column, ProjectExplorerModel.LeafIndex(
					ProjectExplorerModel.NO_PIPELINES_LABEL, parentData, 1))
			
			else:
				raise ProjectExplorerModel.InvalidLabelException(
					"Unsupported data string: {}".format(parentData))
		
		elif isinstance(parentData, Component):
			return self.registerAndCreateIndex(row, column, parentData.getNthChild(row))
		
		elif isinstance(parentData, VisibilityBehavior):
			if row == 0:
				return self.registerAndCreateIndex(row, column, ProjectExplorerModel.LeafIndex(
					parentData.getSrcComponent(), parentData))
			
			if row == 1:
				return self.registerAndCreateIndex(row, column, ProjectExplorerModel.LeafIndex(
					parentData.getDestComponent(), parentData))
		
		elif isinstance(parentData, ActionPipeline):
			# TODO: replace this once action pipelines are implemented
			pass
		
		elif isinstance(parentData, ProjectExplorerModel.LeafIndex):
			# Should never get into here
			pass
		
		else:
			raise ProjectExplorerModel.UnsupportedTypeException(
				"Unsupported data type in index: {}".format(type(parentData)))
	
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
			
			elif data in (
				ProjectExplorerModel.COMPONENT_LABEL, ProjectExplorerModel.BEHAVIOR_LABEL):
				return self.registerAndCreateIndex(0, 0, ProjectExplorerModel.TARGET_GUI_LABEL)
			
			else:
				raise ProjectExplorerModel.InvalidLabelException(
					"Unsupported label: {}".format(data))
		
		elif isinstance(data, Component):
			parentComponent = data.getParent()
			if parentComponent is self._project.getTargetGUIModel().getRoot():
				return self.registerAndCreateIndex(0, 0, ProjectExplorerModel.COMPONENT_LABEL)
			
			else:
				return self.registerAndCreateIndex(parentComponent.getPositionInSiblings(), 0,
				                                   parentComponent)
		
		elif isinstance(data, VisibilityBehavior):
			return self.registerAndCreateIndex(1, 0, ProjectExplorerModel.BEHAVIOR_LABEL)
		
		elif isinstance(data, ActionPipeline):
			# TODO: replace this once action pipelines are implemented
			pass
		
		elif isinstance(data, ProjectExplorerModel.LeafIndex):
			innerData = data.getData()
			parentData = data.getParent()
			if isinstance(innerData, str):
				return self.registerAndCreateIndex(data.getParentIndex(), 0, parentData)
			
			elif isinstance(innerData, Component):
				visBehaviors = list(
					self._project.getTargetGUIModel().getVisibilityBehaviors().values())
				try:
					visBehaviorIdx = visBehaviors.index(parentData)
					return self.registerAndCreateIndex(visBehaviorIdx, 0, parentData)
				except:
					return QModelIndex()
			
			else:
				raise ProjectExplorerModel.UnsupportedTypeException(
					"Unsupported data type in LeafIndex: {}".format(innerData))
		
		else:
			raise ProjectExplorerModel.UnsupportedTypeException(
				"Unsupported data type in index: {}".format(type(data)))
	
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
				return max(1, self._project.getTargetGUIModel().getRoot().childCount())
			
			elif data == ProjectExplorerModel.BEHAVIOR_LABEL:
				return max(1, len(self._project.getTargetGUIModel().getVisibilityBehaviors()))
			
			elif data == ProjectExplorerModel.PIPELINE_LABEL:
				# TODO: replace this once action pipelines are implemented
				return 1
		
		elif isinstance(data, Component):
			return data.childCount()
		
		elif isinstance(data, VisibilityBehavior):
			return 2
		
		elif isinstance(data, ProjectExplorerModel.LeafIndex):
			return 0
		
		elif isinstance(data, ActionPipeline):
			# TODO: replace this once action pipelines are implemented
			pass
		
		else:
			raise ProjectExplorerModel.UnsupportedTypeException(
				"Unsupported data type in index: {}".format(type(data)))
	
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
		:rtype: str or NoneType
		"""
		if not index.isValid():
			return None
		
		elif role != Qt.DisplayRole and role != Qt.DecorationRole:
			return None

		if role == Qt.DecorationRole:
			focusIcon = QIcon()
			focusIcon.addPixmap(QPixmap(":/icon/resources/icons/office/reticle.png"), QIcon.Normal, QIcon.Off)
			return focusIcon
		
		data = index.internalPointer()
		col = index.column()
		row = index.row()

		if isinstance(data, str):
			if col == 0:
				return data
			else:
				return None

		elif isinstance(data, Component):
			category, name = data.getProperties().getProperty("Name")
			category, typeOf = data.getProperties().getProperty("Class Name")
			if col == 0:
				return name.getValue()
			elif col == 1:
				return typeOf.getValue()
			else:
				return None

		elif isinstance(data, VisibilityBehavior):
			if col == 0:
				return data.getProperties().getProperty("Name")[1].getValue()
			elif col == 1:
				description = "{} on {}".format(data.getProperties().getProperty("Reaction Type")[1].getValue().name,
												data.getProperties().getProperty("Trigger Action")[1].getValue())
				return description
			else:
				return None

		elif isinstance(data, ActionPipeline):
			if col == 0:
				return data.getName()
			elif col == 1:
				return data.getType()
			else:
				return None

		elif isinstance(data, ProjectExplorerModel.LeafIndex):
			innerData = data.getData()
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
						return innerData.getProperties().getProperty("Name")[1].getValue()
					else:
						return None

				if row == 1:
					if col == 0:
						return "To"
					elif col == 1:
						return innerData.getProperties().getProperty("Name")[1].getValue()
					else:
						return None
		
		else:
			raise ProjectExplorerModel.UnsupportedTypeException(
				"Unsupported data type in index: {}".format(type(data)))
	
	def headerData(self, section: int, orientation: Qt.Orientation,
	               role: Qt.ItemDataRole = Qt.DisplayRole) -> str:
		"""
		Gets the header data.
		
		:param section: either the row or the column depending on the orientation.
		:type section: int
		:param orientation: Qt.Horizontal for header on top or Qt.Vertical for header on the left
		:type orientation: Qt.Orientation
		:param role: the role to use to get the data.
		:type role: Qt.ItemDataRole
		:return: the data
		:rtype: str
		"""
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return ["Name", "Description"][section]
	
	@Slot()
	def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
		"""
		Run this slot when an index is selected. This slot will emit the following 3 signals depending on what was
		selected: componentSelected, behaviorSelected, pipelineSelected
			
		:param selected: The new selection
		:type selected: QItemSelection
		:param deselected: The old selection
		:type deselected: QItemSelection
		:return: None
		:rtype: NoneType
		"""
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
				
				elif isinstance(data, ProjectExplorerModel.LeafIndex):
					data = data.getData()
					if isinstance(data, Component):
						self.componentSelected.emit(data)
			else:
				raise ProjectExplorerModel.InvalidSelectionException(
					"Multiple row selection is not supported")
	
	def registerAndCreateIndex(self, row, col, data):
		"""
		Keep a reference to the internal data of all QModelIndex objects. This allows us to avoid memory access errors.
		Without storing a reference to the internal data, the python objects go out of scope and become garbage
		collected.
		
		This method also creates a QModelIndex and returns it
		
		:param row: the row of the QModelIndex to create.
		:type row: int
		:param col: the column of the QModelIndex to create.
		:type col: int
		:param data: The object stored inside of the QModelIndex.
		:type data: object
		:return: The created QModelIndex
		:rtype: QModelIndex
		"""
		if data in self._forwardRegistry.keys():
			id = self._forwardRegistry[data]
			data = self._backwardRegistry[id]
		else:
			self._registryCounter += 1
			self._forwardRegistry[data] = self._registryCounter
			self._backwardRegistry[self._registryCounter] = data
		
		return self.createIndex(row, col, data)
	
	def select(self, item):
		"""
		Selects a component, visibility behavior, or action pipeline. It will also refresh the
		index so that the text updates.
		
		:param item: the component, visibility behavior, or action pipeline to select
		:type ite: Component, VisibilityBehavior, or ActionPipeline
		:return: None
		:rtype: NoneType
		"""
		
		if type(item) == Component:
			self.selectComponent(item)
		elif type(item) == VisibilityBehavior:
			self.selectBehavior(item)
		elif type(item) == ActionPipeline:
			pass
		else:
			pass
	
	def selectComponent(self, component: 'Component') -> None:
		"""
		Selects a component in the project explorer by expanding all parents recursively.
		
		:param component: The component to select
		:type component: Component
		:return: None
		:rtype: NoneType
		"""
		path = component.getPathFromRoot()
		# remove ghost root
		path.pop()
		
		indexPath = [0, 0]
		
		cur = QModelIndex()
		cur = self.index(0, 0, cur)
		self._view.expand(cur)
		cur = self.index(0, 0, cur)
		self._view.expand(cur)
		while len(path) > 0:
			comp, idx = path.pop()
			cur = self.index(idx, 0, cur)
			self._view.expand(cur)
		
		qism = QItemSelectionModel
		f = qism.ClearAndSelect | qism.Current | qism.Rows
		self._view.selectionModel().select(cur, f)
		self._view.selectionModel().setCurrentIndex(cur, f)
	
	def selectBehavior(self, visibilityBehavior: 'VisibilityBehavior') -> None:
		"""
		Select a visibility behavior in the project explorer.
		
		:param visibilityBehavior: The visibility behavior to select.
		:type visibilityBehavior: VisibilityBehavior
		:return: None
		:rtype: NoneType
		"""
		cur = QModelIndex()
		cur = self.index(0, 0, cur)
		self._view.expand(cur)
		cur = self.index(1, 0, cur)
		self._view.collapse(cur)
		self._view.expand(cur)
		
		visBehaviors = list(self._project.getTargetGUIModel().getVisibilityBehaviors().values())
		visBehaviorIdx = visBehaviors.index(visibilityBehavior)
		cur = self.index(visBehaviorIdx, 0, cur)
		self._view.expand(cur)
		
		qism = QItemSelectionModel
		f = qism.ClearAndSelect | qism.Current | qism.Rows
		self._view.selectionModel().select(cur, f)
		self._view.selectionModel().setCurrentIndex(cur, f)

	def onContextMenuRequested(self, point: QPoint) -> None:
		"""
		This function is responsible for producing the context menu when an item is right-clicked
		in the project explorer.
		
		:param point: The point where the click occurred
		:type point: QPoint
		:return: None
		"""
		index = self._view.indexAt(point)
		data = index.internalPointer()
		
		if isinstance(data, ProjectExplorerModel.LeafIndex):
			data = data.getData()
		
		v = sm.StateMachine.instance.view
		if isinstance(data, Component):
			menu = ComponentMenu(data)
			menu.onBlink(lambda: v.onItemBlink(data.getId()))
			menu.prerequest()
			menu.exec_(self._view.viewport().mapToGlobal(point))
