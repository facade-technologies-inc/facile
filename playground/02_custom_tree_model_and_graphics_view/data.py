
from PySide2.QtWidgets import QGraphicsScene
from view import NodeItem, MyTreeScene
from model import MyTreeModel

class Tree:
	def __init__(self, root):
		self._root = None
		self._model = MyTreeModel(self)
		self._scene = MyTreeScene(self)
		self.setRoot(root)
		
	def getRoot(self):
		if self._root.isDeleted():
			return None
		return self._root
	
	def setRoot(self, newRoot):
		if self._root is None:
			self._root = newRoot
		elif self._root.isDeleted():
			self._root = newRoot
		self._scene.addItem(newRoot.getNodeItem())
	
	def getNode(self, id):
		workTodo = []
		workTodo.append(self._root)
		while len(workTodo) > 0:
			curWork = workTodo.pop(-1)
			if curWork.getID() == id:
				return curWork
			for child in curWork.getChildren():
				workTodo.append(child)
		return None
	
	def getModel(self):
		return self._model
	
	def getScene(self):
		return self._scene
		
	def depthFirstTraversal(self):
		order = []
		workTodo = []
		workTodo.append(self._root)
		while len(workTodo) > 0:
			curWork = workTodo.pop(-1)
			for child in curWork.getChildren()[::-1]:
				workTodo.append(child)
			order.append(curWork.getID())
			
		return order
	
	def breadthFirstTraversal(self):
		order = []
		workTodo = []
		workTodo.append(self._root)
		while len(workTodo) > 0:
			curWork = workTodo.pop(0)
			for child in curWork.getChildren():
				workTodo.append(child)
			order.append(curWork.getID())
		
		return order

class TreeNode:
	
	count = 0
	
	def __init__(self, parent = None, name=""):
		TreeNode.count+=1
		self._id = TreeNode.count
		self._parent = parent
		self._children = []
		if parent != None:
			parent.addChild(self)
		
		self._nodeItem = NodeItem(self, self.getParentNodeItem())
		self._name = name
		self._isDeleted = False
			
	def getID(self):
		return self._id
	
	def isDeleted(self):
		return self._isDeleted
	
	def getName(self):
		return self._name
	
	def getChildren(self):
		return self._children
	
	def getSiblings(self):
		if self.getParent() is None:
			return [self]
		else:
			return self.getParent().getChildren()
	
	def childCount(self):
		return len(self._children)
	
	def getParent(self):
		return self._parent
	
	def getParentNodeItem(self):
		if self._parent is None:
			return None
		else:
			return self._parent.getNodeItem()
		
	def getPathFromRoot(self):
		path = [(self, self.getRow())]
		possibleRoot = self.getParent()
		while possibleRoot is not None:
			path.append((possibleRoot, possibleRoot.getRow()))
			possibleRoot = possibleRoot.getParent()
		return path
	
	def getNodeItem(self):
		return self._nodeItem
	
	def getNthChild(self, n):
		if len(self._children) > n:
			return self._children[n]
		return None
	
	def getNumDescendants(self):
		numDescendants = 0
		
		if len(self.getChildren()) == 0:
			return 0
		
		for child in self.getChildren():
			numDescendants += 1
			numDescendants += child.getNumDescendants()
			
		return numDescendants
	
	def getMaxDepth(self, curDepth=1):
		maxDepth = [curDepth]
		
		for child in self.getChildren():
			maxDepth.append(child.getMaxDepth(curDepth+1))
			
		return max(maxDepth)
	
	def getRow(self):
		if self._parent == None:
			return 0
		return self._parent.getChildren().index(self)
			
	def addChild(self, child, pos=0):
		self._children.insert(pos, child)
		
	def setName(self, name):
		self._name = name
		
	def remove(self):
		
		scene = self.getNodeItem().scene()
		
		self._isDeleted = True
		siblings = self.getSiblings()
		oldParent = self._parent
		self._parent = None
		siblings.remove(self)
		
		scene.removeItem(self._nodeItem)
		
		if oldParent:
			oldParent.getNodeItem().triggerSceneUpdate()
	def __repr__(self):
		return str(self._id)
