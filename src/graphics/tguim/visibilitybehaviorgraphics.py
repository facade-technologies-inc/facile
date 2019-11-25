"""
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
from PySide2.QtGui import QPainterPath, QPainter
from PySide2.QtWidgets import QGraphicsItem


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
		:return None
		:rtype NoneType
		"""
		QGraphicsItem.__init__(self)
		self._dataVB = dataVisibilityBehavior
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self._srcComponentCenterPoint = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect().center()
		self._destComponentCenterPoint = self._dataVB.getDestComponent().getGraphicsItem().boundingRect().center()
		parent.addItem(self)
	
	def boundingRect(self):
		"""
		This pure virtual function defines the outer bounds of the item as a rectangle.

		:return create the bounding of the item
		:rtype QRectF
		"""
		leftCornerX = min(self._srcComponentCenterPoint.x(), self._destComponentCenterPoint.x())
		leftCornerY = min(self._srcComponentCenterPoint.y(), self._destComponentCenterPoint.y())
		width = abs(self._srcComponentCenterPoint.x() - self._destComponentCenterPoint.x())
		height = abs(self._srcComponentCenterPoint.y() - self._destComponentCenterPoint.y())
		return QRectF(leftCornerX, leftCornerY, width, height)
	
	def paint(self, painter:QPainter, option, widget):
		"""
		Paints the contents of the visibilitybehavior. Override the parent paint function

		:param painter: Use a Qpainter object.
		:type painter: QPainter
		:param option: It provides style options for the item.
		:type option: QStyleOptionGraphicsItem
		:param widget: QWidget
		:type widget: It points to the widget that is being painted on; or make it = None.
		:return None
		:rtype NoneType
		"""
		
		lengthSrcNodeSrcEdgeList = len(self._dataVB.getSrcComponent().getSrcVisibilityBehaviors())
		lengthDesNodeDesEdgeList = len(self._dataVB.getDestComponent().getDestVisibilityBehaviors())
		heightSrcNode = 2 * abs(self._dataVB.getSrcComponent().getGraphicsItem().boundingRect().y() - self._srcComponentCenterPoint.y())
		heightDesNode = 2 * abs(self._dataVB.getDestComponent().getGraphicsItem().boundingRect().y() - self._destComponentCenterPoint.y())
		# This is the index(+1 avoid 0 in calculation) of the edge at the SourceNode's edgeSrcList
		srcNodeIndex = self._dataVB.getSrcComponent().getSrcVisibilityBehaviors().index(self._dataVB) + 1
		# This is the index of the edge at the DesNode's _edgeDesList
		desNodeIndex = self._dataVB.getDestComponent().getDestVisibilityBehaviors().index(
			self._dataVB) + 1
		
		x1 = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect().x() #x does not change, stay at the left most of the node
		y1 = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect().y() + (heightSrcNode / (lengthSrcNodeSrcEdgeList + 1)) * srcNodeIndex
		x2 = self._destComponentCenterPoint.x() + (self._destComponentCenterPoint.x() - self._dataVB.getDestComponent().getGraphicsItem().boundingRect().x())
		y2 = self._dataVB.getDestComponent().getGraphicsItem().boundingRect().y() + (heightDesNode / (lengthDesNodeDesEdgeList + 1)) * desNodeIndex
		
		# painter.drawLine(x1, y1, x2, y2)
		path = QPainterPath()
		path.moveTo(x1, y1)
		path.cubicTo(x1+100, y1+100, x2-200, y2-200, x2, y2)
		painter.drawPath(path)