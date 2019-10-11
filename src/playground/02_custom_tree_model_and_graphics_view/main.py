
import sys
from PySide2.QtWidgets import QApplication
from view import MyView
from data import Tree, TreeNode

if __name__ == "__main__":
	app = QApplication()
	
	root = TreeNode()
	a = TreeNode(root)
	b = TreeNode(root)
	c = TreeNode(root)
	d = TreeNode(a)
	e = TreeNode(a)
	f = TreeNode(d)
	g = TreeNode(b)
	
	tree = Tree(root)
	
	widget = MyView(tree)
	widget.show()
	sys.exit(app.exec_())