from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt


class MyTreeModel(QAbstractItemModel):
	def __init__(self, dataTree):
		QAbstractItemModel.__init__(self)
		self._dataTree = dataTree
		
	def getDataTree(self):
		return self._dataTree
	
		
	################################
	# OVERWRITTEN ABSTRACT METHODS #
	################################
	
	def index(self, row, column, parent):
		# check to see if the index exists
		if not self.hasIndex(row, column, parent):
			return QModelIndex()
		
		if not parent.isValid():
			if row == 0:
				return self.createIndex(row, column, self._dataTree.getRoot())
			else:
				return QModelIndex()
		else:
			parentItem = parent.internalPointer()
			
		childItem = parentItem.getNthChild(row)
		if childItem is not None:
			return self.createIndex(row, column, childItem)
		else:
			return QModelIndex()
	
	def parent(self, index):
		if not index.isValid():
			return QModelIndex()
		
		childItem = index.internalPointer()
		parentItem = childItem.getParent()
		
		if parentItem is None:
			return QModelIndex()
		
		return self.createIndex(parentItem.getRow(), 0, parentItem)
	
	
	def columnCount(self, parent):
		return 2
	
	def rowCount(self, parent):
		#if parent.column() > 0:
		#   return 0
		if not parent.isValid():
			return 1
		else:
			parentItem = parent.internalPointer()
			
		return parentItem.childCount()
	
	def data(self, index, role):
		if not index.isValid():
			return None
		if role != Qt.DisplayRole:
			return None
		
		item = index.internalPointer()
		return [item.getID(), item.getName()][index.column()]
	
	def setData(self, index, value, role):
		if role != Qt.EditRole:
			return False
		
		if not index.isValid():
			return False
		
		if index.column() == 1:
			index.internalPointer().setName(value)
			index.internalPointer().getNodeItem().update()
			self.dataChanged.emit()
			return True
			
		else:
			return False
	
	def flags(self, index):
		if not index.isValid():
			return Qt.NoItemFlags
		
		# allow the user to edit the name of a node, but not the ID
		if index.column() == 1:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
		else:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable
	
	def headerData(self, section, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return ["ID", "Name"][section]
		
		return None
	
	def insertRow(self):
		self.beginInsertRows()
		self.endInsertRows()
		
	def removeRow(self):
		self.beginRemoveRows()
		self.endRemoveRows()