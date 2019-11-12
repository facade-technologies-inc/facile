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

This module contains the componentView class.
"""

import math
from PySide2.QtCore import QRectF, QPointF, QSizeF, QLineF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt, QPainter
from PySide2.QtWidgets import QSplitter, QTreeView
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide2.QtCore import Signal
from PySide2.QtCore import QItemSelectionModel
from data.tguim.component import Component

class ComponentView(QGraphicsItem):
    """
    This class displays an individual GUI component in the target gui,
    based on the component class.
    """
    penWidth = 1.0
    textHeight = 30
    topMargin = 10
    bottomMargin = 10
    leftMargin = 10
    rightMargin = 10
    baseWidth = 400

    def __init__(self, dataComponent: Component, parent = None):
        """
        Constructs a componentview object

        :param dataComponent: Component
        :param parent: parent ComponentView
        """

        QGraphicsItem.__init__(self, parent)
        self._dataComponent = dataComponent
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.

        :return: QRectF
        """

        if self._dataComponent.isDeleted():
            # TODO: need _isDeleted & isDeleted() function in data class. e.g. set _isDeleted = true in remove() function
            return QRectF(-1,-1,4,4)

        id = self._dataComponent.getId()
        numDescendants = self._dataComponent.getNumDescendants() # used to calculate height
        maxDepth = self._dataComponent.getMaxDepth() # used to calculate width
        offsetFromParentTop = ComponentView.topMargin + ComponentView.textHeight #used to calculate y offset from parent.
        siblings = self._dataComponent.getSiblings()
        siblingDepths = [maxDepth]
        for sibling in siblings:
            if sibling is self._dataComponent:
                break
            offsetFromParentTop += (sibling.getNumDescendants()+1) * (ComponentView.topMargin + ComponentView.textHeight + ComponentView.bottomMargin)

        for sibling in siblings:
            siblingDepths.append(sibling.getMaxDepth())
        maxDepth = max(siblingDepths)

        totalHeight = (numDescendants + 1) * (ComponentView.textHeight + ComponentView.topMargin + ComponentView.bottomMargin)
        totalWidth = ComponentView.baseWidth + maxDepth*(ComponentView.leftMargin + ComponentView.rightMargin)

        yPos = -(totalHeight/2) - ComponentView.penWidth/2 + offsetFromParentTop
        xPos = -(totalWidth / 2) - ComponentView.penWidth / 2

        if self._dataComponent.getParent() is not None:
            parentBounding = self.parentItem().boundingRect()
            yPos = parentBounding.y() + offsetFromParentTop - ComponentView.penWidth/2
            xPos = parentBounding.x() + ComponentView.leftMargin - ComponentView.penWidth/2

        return QRectF(xPos, yPos, totalWidth + ComponentView.penWidth, totalHeight + ComponentView.penWidth)


    def shape(self):
        """
        Determine the shape of the graphics item

        :return: QPainterPath
        """

        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        """
        Paints the contents of the component. Override the parent paint function

        :param painter: QPainter
        :param option: QStyleOptionGraphicsItem
        :param widget: QWidget
        :return: None
        """

        if self._dataComponent.isDeleted():
            painter.setBrush(QColor(255,255,255,0))
            painter.setPen(QColor(255,255,255,0))
            return painter.drawRect(0,0,1,1)

        pen = QPen(QColor(100, 200, 255, int(255 / 10)))
        if self.isSelected():
            pen.setStyle(Qt.DashDotLine)
            pen.setColor(QColor(255,0,0))
        else:
            pen.setStyle(Qt.SolidLine)
            pen.setColor(QColor(0,0,0))
        painter.setPen(pen)

        # set background color:
        painter.setBrush(QColor(100, 200, 255, int(255/10)))

        id = self._dataComponent.getId()
        boundingRect = self.boundingRect()
        x = int(boundingRect.x()) + ComponentView.penWidth/2
        y = int(boundingRect.y()) + ComponentView.penWidth/2
        width = int(boundingRect.width()) - ComponentView.penWidth
        height = int(boundingRect.height()) - ComponentView.penWidth
        painter.drawRoundedRect(int(x+ComponentView.leftMargin), int(y+ComponentView.topMargin), int(width - ComponentView.leftMargin - ComponentView.rightMargin), int(height - ComponentView.topMargin - ComponentView.bottomMargin), 5, 5)
        painter.drawText(int(x+ComponentView.leftMargin*1.5), int(y+ComponentView.topMargin+30), "Component {}: {}".format(self._dataComponent.getId(), self._dataComponent.getName()))
        # TODO: _dataComponent.getProperties().getName? instead of _dataComponent.getName()

    def mousePressEvent(self, event):
        """
        This event handler is implemented to receive mouse press events for this item.

        :param event: QGraphicsSceneMouseEvent
        :return: None
        """
        self.setSelected(True)
        self.scene().emitItemSelected(self._dataComponent.getId())

    def triggerSceneUpdate(self):
        """
        Update the scene.

        :return: None
        """
        self.scene().invalidate(self.scene().sceneRect(), QGraphicsScene.ItemLayer)

    def __repr__(self):
        """
        Returns the componentView id as a string.

        :return: str
        """
        return "Component: {}".format(self._dataComponent.getId())