from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt
from PySide2.QtWidgets import QSplitter, QTreeView
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide2.QtCore import Signal
from PySide2.QtCore import QItemSelectionModel


class MyTreeScene(QGraphicsScene):
	
	itemSelected = Signal(int)
	
	def __init__(self, dataTree):
		QGraphicsScene.__init__(self)
		self._dataTree = dataTree
		
		# This line is important because it affects how the scene is updated.
		# The NoIndex index method tells the scene to traverse all items when drawing
		# which is less efficient than using a binary space partitioning tree, but is
		# better for dynamic scenes because no items will be missed in the repaint.
		self.setItemIndexMethod(QGraphicsScene.NoIndex)
		
	def getData(self):
		return self._dataTree
			
	def emitItemSelected(self, id):
		self.itemSelected.emit(id)


class NodeItem(QGraphicsItem):
	penWidth = 1.0
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
		
		if self._dataNode.isDeleted():
			return QRectF(-1,-1,4,4)
		
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
		
		yPos = -(totalHeight/2) - NodeItem.penWidth/2 + offsetFromParentTop
		xPos = -(totalWidth / 2) - NodeItem.penWidth / 2
		
		if self._dataNode.getParent() is not None:
			parentBounding = self.parentItem().boundingRect()
			yPos = parentBounding.y() + offsetFromParentTop - NodeItem.penWidth/2
			xPos = parentBounding.x() + NodeItem.leftMargin - NodeItem.penWidth/2
			
		return QRectF(xPos, yPos, totalWidth + NodeItem.penWidth, totalHeight + NodeItem.penWidth)
		
	
	def shape(self):
		path = QPainterPath()
		path.addRect(self.boundingRect())
		return path
		
	def paint(self, painter, option, widget):
		
		
		
		if self._dataNode.isDeleted():
			painter.setBrush(QColor(255,255,255,0))
			painter.setPen(QColor(255,255,255,0))
			return painter.drawRect(0,0,1,1)
		
		pen = QPen(QColor(100, 200, 255, 255 / 10))
		if self.isSelected():
			pen.setStyle(Qt.DashDotLine)
			pen.setColor(QColor(255,0,0))
		else:
			pen.setStyle(Qt.SolidLine)
			pen.setColor(QColor(0,0,0))
		painter.setPen(pen)
		
		# set background color:
		painter.setBrush(QColor(100, 200, 255, 255/10))
		
		id = self._dataNode.getID()
		boundingRect = self.boundingRect()
		x = int(boundingRect.x()) + NodeItem.penWidth/2
		y = int(boundingRect.y()) + NodeItem.penWidth/2
		width = int(boundingRect.width()) - NodeItem.penWidth
		height = int(boundingRect.height()) - NodeItem.penWidth
		painter.drawRoundedRect(x+NodeItem.leftMargin, y+NodeItem.topMargin, width - NodeItem.leftMargin - NodeItem.rightMargin, height - NodeItem.topMargin - NodeItem.bottomMargin, 5, 5)
		painter.drawText(x+NodeItem.leftMargin*1.5, y+NodeItem.topMargin+30, "Node {}: {}".format(self._dataNode.getID(), self._dataNode.getName()))
		
	def mousePressEvent(self, event):
		self.setSelected(True)
		self.scene().emitItemSelected(self._dataNode.getID())
			
	def triggerSceneUpdate(self):
		self.scene().invalidate(self.scene().sceneRect(), QGraphicsScene.ItemLayer)
			
	def __repr__(self):
		return "NodeItem: {}".format(self._dataNode.getID())
	
		
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
		self._dataTree = dataTree
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
		
		self._addBtn.clicked.connect(self.onAddBtnClicked)
		self._removeBtn.clicked.connect(self.onRemoveBtnClicked)
		dataTree.getScene().itemSelected.connect(self.onGraphicsItemSelected)
		
	def onAddBtnClicked(self):
		model = self._dataTree.getModel()
		treeViewSelectionModel = self._views.getTreeView().selectionModel()
		model.insertRow(0, treeViewSelectionModel.selectedIndexes())
		
	def onRemoveBtnClicked(self):
		model = self._dataTree.getModel()
		treeViewSelectionModel = self._views.getTreeView().selectionModel()
		model.removeRowOfIndex(treeViewSelectionModel.selectedIndexes())
		
	def onGraphicsItemSelected(self, id):
		model = self._dataTree.getModel()
		treeViewSelectionModel = self._views.getTreeView().selectionModel()
		selectedIndex = model.indexFromID(id)
		treeViewSelectionModel.select(selectedIndex, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
		self._views.getTreeView().setCurrentIndex(selectedIndex)