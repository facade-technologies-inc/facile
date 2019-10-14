from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QColor
from PySide2.QtWidgets import QSplitter, QTreeView
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide2.QtCore import Signal


class MyTreeScene(QGraphicsScene):
	
	itemSelected = Signal(int)
	
	def __init__(self, dataTree):
		QGraphicsScene.__init__(self)
		self._dataTree = dataTree
		
	def getData(self):
		return self._dataTree
	
	def forceUpdate(self):
		self.update()
		for view in self.views():
			view.update()
			
	def emitItemSelected(self, id):
		print("Item selected: {}".format(id))
		self.itemSelected.emit(id)


class NodeItem(QGraphicsItem):
	
	textHeight = 30
	topMargin = 10
	bottomMargin = 10
	leftMargin = 10
	rightMargin = 10
	
	baseWidth = 400
	
	def __init__(self, node, parent = None):
		QGraphicsItem.__init__(self, parent)
		self._dataNode = node
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		#self.setFlag(QGraphicsItem.ItemContainsChildrenInShape)
		

	def boundingRect(self):
		penWidth = 1.0
		id = self._dataNode.getID()
		numDescendants = self._dataNode.getNumDescendants() # used to calculate height
		maxDepth = self._dataNode.getMaxDepth() # used to calculate width
		offsetFromParentTop = NodeItem.topMargin + NodeItem.textHeight #used to calculate y offset from parent.
		siblings = self._dataNode.getSiblings()
		siblingDepths = [maxDepth]
		for sibling in siblings:
			if sibling is self._dataNode:
				break
			offsetFromParentTop += (sibling.getNumDescendants()+1) * (NodeItem.topMargin + NodeItem.textHeight + NodeItem.bottomMargin)
		
		for sibling in siblings:
			siblingDepths.append(sibling.getMaxDepth())
		maxDepth = max(siblingDepths)
		
		totalHeight = (numDescendants + 1) * (NodeItem.textHeight + NodeItem.topMargin + NodeItem.bottomMargin)
		totalWidth = NodeItem.baseWidth + maxDepth*(NodeItem.leftMargin + NodeItem.rightMargin)
		
		yPos = -(totalHeight/2) - penWidth/2 + offsetFromParentTop
		xPos = -(totalWidth / 2) - penWidth / 2
		#print(self._dataNode.getID())
		if self._dataNode.getParent() is not None:
			parentBounding = self.parentItem().boundingRect()
			yPos = parentBounding.y() + offsetFromParentTop - penWidth/2
			xPos = parentBounding.x() + NodeItem.leftMargin - penWidth/2
			
		return QRectF(xPos, yPos, totalWidth + penWidth, totalHeight + penWidth)
		
	
	def shape(self):
		path = QPainterPath()
		path.addRect(self.boundingRect())
		return path
		
	def paint(self, painter, option, widget):
		
		numD = (self._dataNode.getNumDescendants() + 1) * 0.3
		# set background color:
		painter.setBrush(QColor(100, 200, 255, 255/10))
		
		
		id = self._dataNode.getID()
		boundingRect = self.boundingRect()
		x = int(boundingRect.x())
		y = int(boundingRect.y())
		width = int(boundingRect.width())
		height = int(boundingRect.height())
		painter.drawRoundedRect(x+NodeItem.leftMargin, y+NodeItem.topMargin, width - NodeItem.leftMargin - NodeItem.rightMargin, height - NodeItem.topMargin - NodeItem.bottomMargin, 5, 5)
		painter.drawText(x+NodeItem.leftMargin*1.5, y+NodeItem.topMargin+30, "Node {}: {}".format(self._dataNode.getID(), self._dataNode.getName()))
		
	def mousePressEvent(self, event):
		self.setSelected(True)
		self.scene().emitItemSelected(self._dataNode.getID())
	
		
class TwoViews(QSplitter):
	def __init__(self, dataTree):
		QSplitter.__init__(self)
		self._graphicsView = QGraphicsView()
		self._treeView = QTreeView()
		
		self.addWidget(self._graphicsView)
		self.addWidget(self._treeView)
		
		self._treeView.setModel(dataTree.getModel())
		self._graphicsView.setScene(dataTree.getScene())
		
	def getTreeView(self):
		return self._treeView
		
class MyView(QWidget):
	def __init__(self, dataTree):
		QWidget.__init__(self)
		self._views = TwoViews(dataTree)
		self._addBtn = QPushButton("Add Node")
		self._removeBtn = QPushButton("Remove Node")
		self._mainLayout = QVBoxLayout()
		self._lowerLayout = QHBoxLayout()
		
		self.setLayout(self._mainLayout)
		self._mainLayout.addWidget(self._views)
		self._mainLayout.addLayout(self._lowerLayout)
		self._lowerLayout.addWidget(self._addBtn)
		self._lowerLayout.addWidget(self._removeBtn)
		
		self._addBtn.clicked.connect(lambda: dataTree.getModel().insertRow(0, self._views.getTreeView().selectionModel().selectedIndexes()))
		self._removeBtn.clicked.connect(lambda: dataTree.getModel().removeRowOfIndex(self._views.getTreeView().selectionModel().selectedIndexes()))
		