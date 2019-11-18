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

This module contains the ComponentGraphics class.
"""

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainterPath, QColor, QPen, Qt
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem


class ComponentGraphics(QGraphicsItem):
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

    def __init__(self, dataComponent: 'Component', rect: tuple = (), parent = None):
        """
        Constructs a componentview object

        :param dataComponent: Component
        :param parent: parent ComponentView
        """

        QGraphicsItem.__init__(self, parent)
        if parent is None:
            dataComponent.getModel().getScene().addItem(self)
            self.isRoot = True
        else:
            self.isRoot = False
        
        self._dataComponent = dataComponent
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
        self.rect = rect

    def boundingRect(self):
        """
        This pure virtual function defines the outer bounds of the item as a rectangle.

        :return: QRectF
        """
        return QRectF(self.rect[0], self.rect[1], self.rect[2] + ComponentGraphics.penWidth, self.rect[3] + ComponentGraphics.penWidth)

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
        """
        if self.isRoot or self.rect[2] == 0 and self.rect[3] == 0:
            painter.setPen(QPen(QColor(Qt.transparent)))
            painter.setBrush(QColor(Qt.transparent))
            return
        
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
        x = int(boundingRect.x()) + ComponentGraphics.penWidth/2
        y = int(boundingRect.y()) + ComponentGraphics.penWidth/2
        width = int(boundingRect.width()) - ComponentGraphics.penWidth
        height = int(boundingRect.height()) - ComponentGraphics.penWidth
        painter.drawRoundedRect(int(x+ComponentGraphics.leftMargin), int(y+ComponentGraphics.topMargin), int(width - ComponentGraphics.leftMargin - ComponentGraphics.rightMargin), int(height - ComponentGraphics.topMargin - ComponentGraphics.bottomMargin), 5, 5)

        category, name = self._dataComponent.getProperties().getProperty("Name")
        painter.drawText(int(x+ComponentGraphics.leftMargin*1.5), int(y+ComponentGraphics.topMargin+30), name.getValue())

    def mousePressEvent(self, event):
        """
        This event handler is implemented to receive mouse press events for this item.

        :param event: QGraphicsSceneMouseEvent
        """
        self.setSelected(True)
        self.scene().emitItemSelected(self._dataComponent.getId())

    def triggerSceneUpdate(self):
        """
        Update the scene.

        """
        self.scene().invalidate(self.scene().sceneRect(), QGraphicsScene.ItemLayer)

    def __repr__(self):
        """
        Returns the componentView id as a string.

        :return: str
        """
        return "Component: {}".format(self._dataComponent.getId())