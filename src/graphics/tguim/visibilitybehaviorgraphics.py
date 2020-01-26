"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This module contains the VBGraphics class.
"""

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QPainter, QPen, Qt, QColor, QBrush
from PySide2.QtWidgets import QGraphicsItem
import data.statemachine as sm


class VBGraphics(QGraphicsItem):
	def __init__(self, dataVisibilityBehavior: 'VisibilityBehavior', parent: 'TScene'):
		"""
		Construct the VBGraphics class.
		'src' means the source component, the one triggering the vb.
		'dest' means the destination component, the one receiving and affected by the vb.

		:param dataVisibilityBehavior: get the data of a VisibilityBehavior
		:type dataVisibilityBehavior: VisibilityBehavior
		:param parent: The parent of the visibility behavior (This will always be the scene)
		:type parent: TScene
		:return: None
		:rtype: NoneType
		"""
		QGraphicsItem.__init__(self)
		self._dataVB = dataVisibilityBehavior
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self._srcComponentCenterPoint = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect().center()
		self._destComponentCenterPoint = self._dataVB.getDestComponent().getGraphicsItem().boundingRect().center()
		parent.addItem(self)
		self._boundingRect = None
	
	def boundingRect(self):
		"""
		This pure virtual function defines the outer bounds of the item as a rectangle.

		:return: create the bounding of the item
		:rtype: QRectF
		"""
		if self._boundingRect:
			return self._boundingRect
		
		leftCornerX = min(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x(),
		                  self._dataVB.getDestComponent().getGraphicsItem().scenePos().x())
		leftCornerY = min(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y(),
		                  self._dataVB.getDestComponent().getGraphicsItem().scenePos().y())
		width = abs(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x()
		            - self._dataVB.getDestComponent().getGraphicsItem().scenePos().x())
		height = abs(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y()
		             - self._dataVB.getDestComponent().getGraphicsItem().scenePos().y())
		return QRectF(leftCornerX, leftCornerY, width, height)
	
	def paint(self, painter: QPainter, option, widget):
		"""
		Paints the contents of the visibilitybehavior. Override the parent paint function.
		Only renders the visibility behavior if the configuration variable, showBehaviors, is true.
		
		:param painter: Use a Qpainter object.
		:type painter: QPainter
		:param option: It provides style options for the item.
		:type option: QStyleOptionGraphicsItem
		:param widget: QWidget
		:type widget: It points to the widget that is being painted on; or make it = None.
		:return: None
		:rtype: NoneType
		"""
		# Only draw visibility behaviors if "Show Visibility Behaviors" action is checked in the View drop down.
		if sm.StateMachine.instance.configVars.showBehaviors:
			arrowColor = QColor(255, 200, 50)

			pen = QPen(arrowColor)
			if self.isSelected():
				pen.setStyle(Qt.DashDotLine)
				arrowColor = QColor(255, 0, 0)
			else:
				pen.setStyle(Qt.SolidLine)
				arrowColor = QColor(255, 200, 50)

			pen.setWidth(10)
			painter.setPen(pen)

      lengthSrcNodeSrcEdgeList = len(self._dataVB.getSrcComponent().getSrcVisibilityBehaviors())
      lengthDesNodeDesEdgeList = len(self._dataVB.getDestComponent().getDestVisibilityBehaviors())
      heightSrcNode = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect(
        withMargins=False).height()
      heightDesNode = self._dataVB.getDestComponent().getGraphicsItem().boundingRect(
        withMargins=False).height()
      widthDesNode = self._dataVB.getDestComponent().getGraphicsItem().boundingRect(
        withMargins=False).width()
      # This is the index(+1 avoid 0 in calculation) of the edge at the SourceNode's edgeSrcList
      srcNodeIndex = self._dataVB.getSrcComponent().getSrcVisibilityBehaviors().index(
        self._dataVB) + 1
      # This is the index of the edge at the DesNode's _edgeDesList
      desNodeIndex = self._dataVB.getDestComponent().getDestVisibilityBehaviors().index(
        self._dataVB) + 1

      # ComponentGraphics.MARGIN = 20
      x1 = self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x() + 20  # x does not change, stay at the left most of the node
      y1 = self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y() + (
        heightSrcNode / (lengthSrcNodeSrcEdgeList + 1)) * srcNodeIndex
      x2 = self._dataVB.getDestComponent().getGraphicsItem().scenePos().x() + widthDesNode + 20
      y2 = self._dataVB.getDestComponent().getGraphicsItem().scenePos().y() + (
        heightDesNode / (lengthDesNodeDesEdgeList + 1)) * desNodeIndex

      # build the path and arrowhead
      path, leftInTrue, pathBoundingRect = self.buildPath(x1, x2, y1, y2)
      arrowHead, arrowHeadBoundingRect = self.buildArrowHead(x1, x2, y1, y2, leftInTrue)

      brTLx = min(pathBoundingRect.topLeft().x(), arrowHeadBoundingRect.topLeft().x())
      brTLy = min(pathBoundingRect.topLeft().y(), arrowHeadBoundingRect.topLeft().y())
      brBLx = min(pathBoundingRect.bottomLeft().x(), arrowHeadBoundingRect.bottomLeft().x())
      brBLy = max(pathBoundingRect.bottomLeft().y(), arrowHeadBoundingRect.bottomLeft().y())
      brTRx = max(pathBoundingRect.topRight().x(), arrowHeadBoundingRect.topRight().x())
      brHeight = brBLy - brTLy
      brWidth = brTRx - brTLx
      self._boundingRect = QRectF(brTLx, brTLy, brWidth, brHeight)

      #painter.drawRect(self.boundingRect())
      painter.drawPath(path)
      painter.drawPath(arrowHead)
      painter.fillPath(arrowHead, QBrush(arrowColor))

	def buildArrowHead(self, x1, x2, y1, y2, leftInTrue):
		# draw the arrow head
		aSize = 20
		if leftInTrue:
			arrowHead = QPainterPath()
			arrowHead.moveTo(x2 + aSize, y2)
			arrowHead.lineTo(x2 - aSize, y2 - aSize)
			arrowHead.lineTo(x2 - aSize, y2 + aSize)
			arrowHead.lineTo(x2 + aSize, y2)
		else:
			arrowHead = QPainterPath()
			arrowHead.moveTo(x2 - aSize, y2)
			arrowHead.lineTo(x2 + aSize, y2 - aSize)
			arrowHead.lineTo(x2 + aSize, y2 + aSize)
			arrowHead.lineTo(x2 - aSize, y2)
		
		boundingRect = arrowHead.boundingRect()
		
		return arrowHead, boundingRect

	
	def buildPath(self, x1, x2, y1, y2):
		"""
		This function is used to build the path for the visibility behavior.
		It has some basic arrow routing algorithm:
		
		1. src is at right, dest is at left, just cubic to it
		#. src is at left, dest is at right
		
			a. y is almost the same, cubic to it
			#. distance is bigger than 1/3 * root.width, go around the root component
			
					i. src is higher than dest, go around from the top
					#. bb src is lower than dest, go around from the bottom
					
			#. horizontal distance is smaller than 1/3 * root.width, zigzag to it
			
		.. todo::
			Improve on the algorithm (add collision detector)
		
		:param x1: the x coordinate for the src component
		:type x1: float
		:param x2: the x coordinate for the dest component
		:type x2: float
		:param y1: the y coordinate for the src component
		:type y1: float
		:param y2: the x coordinate for the dest component
		:type y2: float
		:return path: return the path of the visibility behavior
		:rtype path: QPainterPath
		"""
		
		baseComponent = self.getOneComponentDownRoot()
		baseComponentWidth = baseComponent.getGraphicsItem().boundingRect(withMargins=False).width()
		baseComponentHeight = baseComponent.getGraphicsItem().boundingRect(withMargins=False).height()
		path = QPainterPath()
		
		#TODO: If the component is the root component, VBGraphics may overlap with other components easily.FIX IT
		if x1 > x2:
			path.moveTo(x1, y1)
			path.cubicTo(x1 + 100, y1 + 100, x2 - 200, y2 - 200, x2, y2)
			leftInTrue = False
		elif abs(y2 - y1) < 50:
			path.moveTo(x1, y1)
			path.cubicTo(x1 + 100, y1 + 100, x2 - 200, y2 - 200, x2, y2)
			leftInTrue = True
		elif (x2 - x1) < (1/3 * baseComponentWidth):
			path.moveTo(x1, y1)
			path.lineTo(x1 - 200, y1)
			path.lineTo(x1 - 200, y2)
			path.lineTo(x2, y2)
			leftInTrue = True
		elif (x2 - x1) > (1/3 * baseComponentWidth) and y1 <= y2:
			path.moveTo(x1, y1)
			path.lineTo(baseComponent.getGraphicsItem().scenePos().x() - x1/3, y1)
			path.lineTo(baseComponent.getGraphicsItem().scenePos().x() - x1/3,
			            baseComponent.getGraphicsItem().scenePos().y() - y1/3)
			path.lineTo(baseComponentWidth + x1, baseComponent.getGraphicsItem().scenePos().y() - y1/3)
			path.lineTo(baseComponentWidth + x1, y2)
			path.lineTo(x2, y2)
			leftInTrue = False
		elif (x2 - x1) > (1/3 * baseComponentWidth) and y1 > y2:
			path.moveTo(x1, y1)
			path.lineTo(baseComponent.getGraphicsItem().scenePos().x() - x1/3, y1)
			path.lineTo(baseComponent.getGraphicsItem().scenePos().x() - x1/3,
			            baseComponentHeight + y1/3)
			path.lineTo(baseComponentWidth + x1, baseComponentHeight + y1/3)
			path.lineTo(baseComponentWidth + x1, y2)
			path.lineTo(x2, y2)
			leftInTrue = False
		else:
			#exception, then fix it
			path.moveTo(x1, y1)
			path.lineTo(x1, 30)
			path.lineTo(x2, 30)
			path.lineTo(x2, y2)
			leftInTrue = False
		
		boundingRect = path.boundingRect()
		
		return path, leftInTrue, boundingRect
	
	def getOneComponentDownRoot(self):
		"""
		This function is used to locate the base component of the program.
		
		:return: the component with id = 2; the base component for the program; the component that is one step down of the root component
		:rtype: Component
		"""
		possibleRoot = self._dataVB.getSrcComponent()
		
		while possibleRoot.getParent().getParent() is not None:
			possibleRoot = possibleRoot.getParent()
		
		return possibleRoot
	
	def shape(self):
		lengthSrcNodeSrcEdgeList = len(self._dataVB.getSrcComponent().getSrcVisibilityBehaviors())
		lengthDesNodeDesEdgeList = len(self._dataVB.getDestComponent().getDestVisibilityBehaviors())
		heightSrcNode = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect(
			withMargins=False).height()
		heightDesNode = self._dataVB.getDestComponent().getGraphicsItem().boundingRect(
			withMargins=False).height()
		widthDesNode = self._dataVB.getDestComponent().getGraphicsItem().boundingRect(
			withMargins=False).width()
		# This is the index(+1 avoid 0 in calculation) of the edge at the SourceNode's edgeSrcList
		srcNodeIndex = self._dataVB.getSrcComponent().getSrcVisibilityBehaviors().index(
			self._dataVB) + 1
		# This is the index of the edge at the DesNode's _edgeDesList
		desNodeIndex = self._dataVB.getDestComponent().getDestVisibilityBehaviors().index(
			self._dataVB) + 1

		# ComponentGraphics.MARGIN = 20
		x1 = self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x() + 20  # x does not change, stay at the left most of the node
		y1 = self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y() + (
			heightSrcNode / (lengthSrcNodeSrcEdgeList + 1)) * srcNodeIndex
		x2 = self._dataVB.getDestComponent().getGraphicsItem().scenePos().x() + widthDesNode + 20
		y2 = self._dataVB.getDestComponent().getGraphicsItem().scenePos().y() + (
			heightDesNode / (lengthDesNodeDesEdgeList + 1)) * desNodeIndex

		path = self.buildPath(x1, x2, y1, y2)

		return path

