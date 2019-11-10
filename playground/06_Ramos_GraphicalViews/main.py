
import sys
from PySide2.QtWidgets import QApplication
from view import MyView
from data import Tree, TreeNode, Edge


if __name__ == "__main__":
	app = QApplication()
	
	# Create the tree structure
	root = TreeNode(name="Target GUI Model")
	a = TreeNode(root, name="Window 1")
	b = TreeNode(root, name="Window 2")
	c = TreeNode(root, name="Window 3")
	d = TreeNode(a, name="Component 1")
	e = TreeNode(a, name="Quit Button")
	f = TreeNode(d, name="Login Button")
	g = TreeNode(b, name="Submit Button")
	h = TreeNode(d, name="another button")
	i = TreeNode(d, name="another button")
	j = TreeNode(i, name="another button")
	k = TreeNode(j, name="another button")
	l = TreeNode(k, name="another button")
	m = TreeNode(k, name="another button")
	n = TreeNode(k, name="another button")
	o = TreeNode(n, name="another button")
	p = TreeNode(a, name="another button")
	q = TreeNode(p, name="another button")
	r = TreeNode(q, name="another button")

	edgeOne = Edge(a, f)
	a.addSourceEdge(edgeOne)
	f.addDesEdge(edgeOne)
	# edgeTwo = Edge(c, d)
	# c.addSourceEdge(edgeTwo)
	# d.addDesEdge(edgeTwo)
	# edgeThree = Edge(e, f)
	# e.addSourceEdge(edgeThree)
	# f.addDesEdge(edgeThree)
	# edgeFour = Edge(g, h)
	# g.addSourceEdge(edgeFour)
	# h.addDesEdge(edgeFour)
	# edgeFive = Edge(root, f)
	# root.addSourceEdge(edgeFive)
	# f.addDesEdge(edgeFive)

	tree = Tree(root)
	
	# Create the views to display and edit the tree
	widget = MyView(tree)
	widget.show()
	sys.exit(app.exec_())