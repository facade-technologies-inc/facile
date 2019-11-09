
from data.tguim.entity import Entity


class Component(Entity):


	def __init__(self, parent=None, name=""):
		super().__init__()
		# GuiComponent.count += 1
		# self._id = GuiComponent.count
		self._parent = parent
		self._children = []
		if parent is not None:
			parent.addChild(self)

		#self._nodeItem = NodeItem(self, self.getParentNodeItem())
		self._name = name
		self._isDeleted = False
		# Add self to the dictionary of guiComponents in the tree.
		#TODO: add guiComponentToken.
	
	# def getId(self):
	# 	return self._id

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
	
	# def getParentNodeItem(self):
	# 	if self._parent is None:
	# 		return None
	# 	else:
	# 		return self._parent.getNodeItem()

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
