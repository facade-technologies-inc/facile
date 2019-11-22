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
    def __init__(self, dataVisibilityBehavior: 'VisibilityBehavior'):
        """
        Construct the VBGraphics class.
        'src' means the source component, the one triggering the vb.
        'dest' means the destination component, the one receiving and affected by the vb.

        :param dataVisibilityBehavior: get the data of a VisibilityBehavior
        :type dataVisibilityBehavior: VisibilityBehavior
        :return None
        :rtype NoneType
        """
        QGraphicsItem.__init__(self)
        self._dataVB = dataVisibilityBehavior
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self._srcComponentCenterPoint = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect().center()
        self._destComponentCenterPoint = self._dataVB.getDestComponent().getGraphicsItem().boundingRect().center()

    def boundingRect(self):
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.

        :return create the bounding of the item
        :rtype QRectF
        """
        leftCornerX = min(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x(),
                          self._dataVB.getDestComponent().getGraphicsItem().scenePos().x())
        leftCornerY = min(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y(),
                          self._dataVB.getDestComponent().getGraphicsItem().scenePos().y())
        width = abs(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x()
                    - self._dataVB.getDestComponent().getGraphicsItem().scenePos().x())
        height = abs(self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y()
                     - self._dataVB.getDestComponent().getGraphicsItem().scenePos().y())
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
        heightSrcNode = self._dataVB.getSrcComponent().getGraphicsItem().boundingRect(withMargins=False).height()
        heightDesNode = self._dataVB.getDestComponent().getGraphicsItem().boundingRect(withMargins=False).height()
        widthDesNode = self._dataVB.getDestComponent().getGraphicsItem().boundingRect(withMargins=False).width()
        # This is the index(+1 avoid 0 in calculation) of the edge at the SourceNode's edgeSrcList
        srcNodeIndex = self._dataVB.getSrcComponent().getSrcVisibilityBehaviors().index(self._dataVB) + 1
        # This is the index of the edge at the DesNode's _edgeDesList
        desNodeIndex = self._dataVB.getDestComponent().getDestVisibilityBehaviors().index(self._dataEdge) + 1

        x1 = self._dataVB.getSrcComponent().getGraphicsItem().scenePos().x() #x does not change, stay at the left most of the node
        y1 = self._dataVB.getSrcComponent().getGraphicsItem().scenePos().y() + (heightSrcNode / (lengthSrcNodeSrcEdgeList + 1)) * srcNodeIndex
        x2 = self._dataVB.getDestComponent().getGraphicsItem().scenePos().x() + widthDesNode
        y2 = self._dataVB.getDestComponent().getGraphicsItem().scenePos().y() + (heightDesNode / (lengthDesNodeDesEdgeList + 1)) * desNodeIndex

        # painter.drawLine(x1, y1, x2, y2)
        path = QPainterPath()
        path.moveTo(x1, y1)
        path.cubicTo(x1+100, y1+100, x2-200, y2-200, x2, y2)
        painter.drawPath(path)