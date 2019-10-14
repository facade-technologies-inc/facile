from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
import data

class MyTreeModel(QAbstractItemModel):
	def __init__(self, dataTree):
		QAbstractItemModel.__init__(self)
		self._dataTree = dataTree
		
	def getDataTree(self):
		return self._dataTree
	
		
	################################
	# OVERWRITTEN ABSTRACT METHODS #
	################################
	def indexFromID(self, id):
		self._dataTree.getNode(id)
		# not finished here
	
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
		l = [item.getID(), item.getName()]
		return l[index.column()]
	
	def setData(self, index, value, role):
		if role != Qt.EditRole:
			return False
		
		if not index.isValid():
			return False
		
		if index.column() == 1:
			index.internalPointer().setName(value)
			index.internalPointer().getNodeItem().update()
			self.dataChanged.emit(index, index, [])
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
	
	def insertRow(self, row, parent=QModelIndex()):
		if type(parent) == list:
			if len(parent) == 0:
				return False
			rows = set()
			for p in parent:
				rows.add(p.row())
			if len(rows) > 1:
				return False
			
			parent = parent[0]
			
		if not parent.isValid():
			return False
		
		self.beginInsertRows(parent, 0, 0)
		newNode = data.TreeNode(parent.internalPointer(), name="New Node")
		newNode.getNodeItem().update()
		self.endInsertRows()
		return True
		
	def removeRowOfIndex(self, indexes):
		if type(indexes) == list:
			if len(indexes) == 0:
				return False
			rows = set()
			for i in indexes:
				rows.add(i.row())
			if len(rows) > 1:
				return False
			
			index = indexes[0]
		
		if not index.isValid():
			return False
		
		self.beginRemoveRows(self.parent(index), index.row(), index.row())
		index.internalPointer().remove()
		self.endRemoveRows()
		return True