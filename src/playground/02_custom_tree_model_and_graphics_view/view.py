from PySide2.QtCore import QRectF
from PySide2.QtWidgets import QSplitter, QTreeView
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem


class MyTreeScene(QGraphicsScene):
	def __init__(self, dataTree):
		QGraphicsScene.__init__(self)
		self._dataTree = dataTree
		
	def getData(self):
		return self._dataTree


class NodeItem(QGraphicsItem):
	
	def __init__(self, node, parent = None):
		QGraphicsItem.__init__(self, parent)
		self._dataNode = node
		self.setFlag(QGraphicsItem.ItemIsMovable)

	def boundingRect(self):
		penWidth = 1.0
		id = self._dataNode.getID()
		return QRectF(-20 - penWidth / 2, -20*(id+1)*3 - penWidth / 2, 500 + penWidth, 40 + penWidth)
		
	def paint(self, painter, option, widget):
		id = self._dataNode.getID()
		painter.drawRoundedRect(-20, -20*(id+1)*3, 500, 40, 5, 5)
		painter.drawText(-5, -20*(id+1)*3+30, "Node {}: {}".format(self._dataNode.getID(), self._dataNode.getName()))
		
		
		
class MyView(QSplitter):
	def __init__(self, dataTree):
		QSplitter.__init__(self)
		self._graphicsView = QGraphicsView()
		self._treeView = QTreeView()
		
		self.addWidget(self._graphicsView)
		self.addWidget(self._treeView)
	
		self._treeView.setModel(dataTree.getModel())
		self._graphicsView.setScene(dataTree.getScene())