
from PySide2.QtWidgets import QGraphicsScene
from view import NodeItem, MyTreeScene
from model import MyTreeModel

class Tree:
	def __init__(self, root):
		self._root = root
		self._model = MyTreeModel(self)
		self._scene = MyTreeScene(self)
		self._scene.addItem(root.getNodeItem())
		
	def getRoot(self):
		return self._root
	
	def getNode(self, id):
		workTodo = []
		workTodo.append(self._root)
		while len(workTodo) > 0:
			curWork = workTodo.pop(-1)
			for child in curWork.getChildren():
				if child.getID() == id:
					return child
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
			
	def getID(self):
		return self._id
	
	def getName(self):
		return self._name
	
	def getChildren(self):
		return self._children
	
	def getSiblings(self):
		if self.getParent() is None:
			return []
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
		for child in self.getChildren():
			child.remove()
		siblings = self.getSiblings()
		self._parent = None
		if self in siblings:
			siblings.remove(self)
		self._nodeItem.scene().removeItem(self._nodeItem)
		
	def __repr__(self):
		return str(self._id)
		
		
if __name__ == "__main__":
	root = TreeNode(name="Target GUI Model")
	a = TreeNode(root, name="Window 1")
	b = TreeNode(root, name="Window 2")
	c = TreeNode(root, name="Window 3")
	d = TreeNode(a, name="Component 1")
	e = TreeNode(a, name="Quit Button")
	f = TreeNode(d, name="Login Button")
	g = TreeNode(b, name="Submit Button")
	
	tree = Tree(root)
	
	print(tree.depthFirstTraversal())
	print(tree.breadthFirstTraversal())
	