
import sys
from PySide2.QtWidgets import QApplication
from view import MyView
from data import Tree, TreeNode

if __name__ == "__main__":
	app = QApplication()
	
	root = TreeNode(name="Target GUI Model")
	a = TreeNode(root, name="Window 1")
	b = TreeNode(root, name="Window 2")
	c = TreeNode(root, name="Window 3")
	d = TreeNode(a, name="Component 1")
	e = TreeNode(a, name="Quit Button")
	f = TreeNode(d, name="Login Button")
	g = TreeNode(b, name="Submit Button")
	
	tree = Tree(root)
	
	widget = MyView(tree)
	widget.show()
	sys.exit(app.exec_())