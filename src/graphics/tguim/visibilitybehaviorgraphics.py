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
from PySide2.QtGui import QPainterPath, QPainter
from PySide2.QtWidgets import QGraphicsItem

from data.tguim.component import VisibilityBehavior


class VBGraphics(QGraphicsItem):
    def __init__(self, dataVisibilityBehavior: VisibilityBehavior):
        """
        Construct the VBGraphics class.
        'from' means the source component, the one triggering the vb.
        'to' means the destination component, the one receiving and affected by the vb.

        :param dataVisibilityBehavior: get the data of a VisibilityBehavior
        :type dataVisibilityBehavior: VisibilityBehavior
        """
        QGraphicsItem.__init__(self)
        self._dataVB = dataVisibilityBehavior
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self._fromComponentCenterPoint = self._dataVB.getFromComponent().getGraphicsItem().boundingRect().center()
        self._toComponentCenterPoint = self._dataVB.getToComponent().getGraphicsItem().boundingRect().center()
        # TODO: the last two declarations will work after Sean define _graphicsItem in his classes

    def boundingRect(self):
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.

        :return: create the bounding of the item
        :rtype: QRectF
        """
        leftCornerX = min(self._fromComponentCenterPoint.x(), self._toComponentCenterPoint.x())
        leftCornerY = min(self._fromComponentCenterPoint.y(), self._toComponentCenterPoint.y())
        width = abs(self._fromComponentCenterPoint.x() - self._toComponentCenterPoint.x())
        height = abs(self._fromComponentCenterPoint.y() - self._toComponentCenterPoint.y())
        return QRectF(leftCornerX, leftCornerY, width, height)

    def paint(self, painter:QPainter, option, widget):
        """
        Paints the contents of the component. Override the parent paint function
        Src = From, maybe change it later
        Des = To, maybe change it later
        TODO: ask Sean about his opinion on Src/From and Dest/To

        :param painter: QPainter
        :param option: QStyleOptionGraphicsItem
        :param widget: QWidget
        :return : None
        """

        # TODO: need getter of _fromVisibilityBehaviors and _toVisibilityBehaviors in Sean's class, so I can calculate the length of the list
        lengthSrcNodeSrcEdgeList = len(self._dataVB.getFromComponent().getFromVisibilityBehaviors())
        lengthDesNodeDesEdgeList = len(self._dataVB.getToComponent().getToVisibilityBehaviors())
        # TODO: still, need Sean to define _graphicsItem in his classes
        heightSrcNode = 2 * abs(self._dataVB.getFromComponent().getGraphicsItem().boundingRect().y() - self._fromComponentCenterPoint.y())
        heightDesNode = 2 * abs(self._dataVB.getToComponent().getGraphicsItem().boundingRect().y() - self._toComponentCenterPoint.y())
        # This is the index(+1 avoid 0 in calculation) of the edge at the SourceNode's edgeSrcList
        srcNodeIndex = self._dataVB.getFromComponent().getFromVisibilityBehaviors().index(self._dataVB) + 1
        # This is the index of the edge at the DesNode's _edgeDesList
        desNodeIndex = self._dataVB.getToComponent().getToVisibilityBehaviors().index(self._dataEdge) + 1

        x1 = self._dataVB.getFromComponent().getGraphicsItem().boundingRect().x() #x does not change, stay at the left most of the node
        y1 = self._dataVB.getFromComponent().getGraphicsItem().boundingRect().y() + (heightSrcNode / (lengthSrcNodeSrcEdgeList + 1)) * srcNodeIndex
        x2 = self._toComponentCenterPoint.x() + (self._toComponentCenterPoint.x() - self._dataVB.getToComponent().getGraphicsItem().boundingRect().x())
        y2 = self._dataVB.getToComponent().getGraphicsItem().boundingRect().y() + (heightDesNode / (lengthDesNodeDesEdgeList + 1)) * desNodeIndex

        # painter.drawLine(x1, y1, x2, y2)
        path = QPainterPath()
        path.moveTo(x1, y1)
        path.cubicTo(x1+100, y1+100, x2-200, y2-200, x2, y2)
        painter.drawPath(path)