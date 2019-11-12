import math
import weakref

from PySide2.QtCore import QRectF, QPointF, QSizeF, QLineF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt, QPainter
from PySide2.QtWidgets import QSplitter, QTreeView
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide2.QtCore import Signal
from PySide2.QtCore import QItemSelectionModel
from data import Tree, Edge

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



class EdgeItem(QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    def __init__(self, edgeData:Edge):
        QGraphicsItem.__init__(self)
        self._dataEdge = edgeData
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        leftCornerX = min(self._dataEdge.sourceCenterPoint.x(), self._dataEdge.destCenterPoint.x())
        leftCornerY = min(self._dataEdge.sourceCenterPoint.y(), self._dataEdge.destCenterPoint.y())
        width = abs(self._dataEdge.sourceCenterPoint.x() - self._dataEdge.destCenterPoint.x())
        height = abs(self._dataEdge.sourceCenterPoint.y() - self._dataEdge.destCenterPoint.y())
        return QRectF(leftCornerX, leftCornerY, width, height)

    def paint(self, painter:QPainter, option, widget):
        lengthSrcNodeSrcEdgeList = len(self._dataEdge.getSrcNode().getSourceEdges())
        lengthDesNodeDesEdgeList = len(self._dataEdge.getDesNode().getDestinationEdges())
        heightSrcNode = 2 * abs(self._dataEdge.getSrcNode().getNodeItem().boundingRect().y() - self._dataEdge.sourceCenterPoint.y())
        heightDesNode = 2 * abs(self._dataEdge.getDesNode().getNodeItem().boundingRect().y() - self._dataEdge.destCenterPoint.y())
        # This is the index(+1 avoid 0 in calculation) of the edge at the SourceNode's edgeSrcList
        srcNodeIndex = self._dataEdge.getSrcNode().getSourceEdges().index(self._dataEdge) + 1
        # This is the index of the edge at the DesNode's _edgeDesList
        desNodeIndex = self._dataEdge.getDesNode().getDestinationEdges().index(self._dataEdge) + 1

        x1 = self._dataEdge.getSrcNode().getNodeItem().boundingRect().x() #x does not change, stay at the left most of the node
        y1 = self._dataEdge.getSrcNode().getNodeItem().boundingRect().y() + (heightSrcNode / (lengthSrcNodeSrcEdgeList + 1)) * srcNodeIndex
        x2 = self._dataEdge.destCenterPoint.x() + (self._dataEdge.destCenterPoint.x() - self._dataEdge.getDesNode().getNodeItem().boundingRect().x())
        y2 = self._dataEdge.getDesNode().getNodeItem().boundingRect().y() + (heightDesNode / (lengthDesNodeDesEdgeList + 1)) * desNodeIndex

        painter.drawLine(x1,
                         y1,
                         x2,
                         y2)

        #ToDo: make the arrows distribute evenly on the edge.
        #Realize that when it shows in the main.py, all the edges are added. So I know how many edges are there when I paint.
        #It's not interactive yet - allowing user to add edge. So don't worry about that part. Just go static.
        #Then I could simply use the length of the list, calculate where should I put the arrow.
        #Paint it!


###########################################################
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