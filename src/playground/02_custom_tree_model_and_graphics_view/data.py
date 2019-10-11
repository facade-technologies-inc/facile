
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
	
	def __init__(self, parent = None):
		TreeNode.count+=1
		self._id = TreeNode.count
		self._parent = parent
		self._children = []
		if parent != None:
			parent.addChild(self)
		
		self._nodeItem = NodeItem(self, self.getParentNodeItem())
			
	def getID(self):
		return self._id
	
	def getChildren(self):
		return self._children
	
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
			
	def addChild(self, child):
		self._children.append(child)
		
	def getNthChild(self, n):
		if len(self._children) > n:
			return self._children[n]
		return None
	
	def getRow(self):
		if self._parent == None:
			return 0
		return self._parent.getChildren().index(self)
		
		
	def __repr__(self):
		return str(self._id)
		
		
if __name__ == "__main__":
	root = TreeNode()
	a = TreeNode(root)
	b = TreeNode(root)
	c = TreeNode(root)
	d = TreeNode(a)
	e = TreeNode(a)
	f = TreeNode(d)
	g = TreeNode(b)
	
	tree = Tree(root)
	
	print(tree.depthFirstTraversal())
	print(tree.breadthFirstTraversal())
	