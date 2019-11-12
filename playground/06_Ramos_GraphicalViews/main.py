
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
	h = TreeNode(d, name="h button")
	i = TreeNode(d, name="i button")
	j = TreeNode(i, name="j button")
	k = TreeNode(j, name="k button")
	l = TreeNode(k, name="l button")
	m = TreeNode(k, name="m button")
	n = TreeNode(k, name="n button")
	o = TreeNode(n, name="o button")
	p = TreeNode(a, name="p button")
	q = TreeNode(p, name="q button")
	r = TreeNode(q, name="r button")

	edgeOne = Edge(a, f)
	a.addSourceEdge(edgeOne)
	f.addDesEdge(edgeOne)
	edgeTwo = Edge(a, g)
	a.addSourceEdge(edgeTwo)
	g.addDesEdge(edgeTwo)
	edgeThree = Edge(a, b)
	a.addSourceEdge(edgeThree)
	b.addDesEdge(edgeThree)
	edgeFour = Edge(r, b)
	r.addSourceEdge(edgeFour)
	b.addDesEdge(edgeFour)
	# edgeFive = Edge(root, f)
	# root.addSourceEdge(edgeFive)
	# f.addDesEdge(edgeFive)

	tree = Tree(root)
	
	# Create the views to display and edit the tree
	widget = MyView(tree)
	widget.show()
	sys.exit(app.exec_())